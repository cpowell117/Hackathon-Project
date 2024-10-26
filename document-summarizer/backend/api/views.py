# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import HttpResponse
from django.conf import settings
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import anthropic
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv('AT_KEY')

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if file.content_type == 'application/pdf':
                text = self.extract_text_from_pdf(file)
            else:
                text = file.read().decode('utf-8')

            analysis = self.analyze_with_claude(text)

            pdf_buffer = self.generate_pdf(analysis)

            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="analysis.pdf"'
            
            return response

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")

    def analyze_with_claude(self, text):
        """Analyze text using Claude API"""
        try:
            prompt = """
            Please analyze this document and provide:
            1. Executive Summary (2-3 sentences)
            2. Key Points (main ideas and findings)
            3. Detailed Analysis (important details and insights)
            4. Conclusions and Recommendations

            Format the response with clear headings and bullet points where appropriate.
            """

            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nDocument text:\n{text}"
                    }
                ],
                max_tokens=4000,
                temperature=0.5
            )
            
            return response.content[0].text

        except anthropic.RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later.")
        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing text: {str(e)}")

    def generate_pdf(self, analysis):
        """Generate PDF with analysis results"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        normal_style.wordWrap = 'CJK'
        
        content = []
        
        content.append(Paragraph("Document Analysis Report", title_style))
        content.append(Paragraph("<br/><br/>", normal_style))
        
        analysis_lines = analysis.split('\n')
        current_section = []
        
        for line in analysis_lines:

            if line.strip().upper() == line.strip() and line.strip():

                if current_section:
                    content.append(Paragraph('<br/>'.join(current_section), normal_style))
                    current_section = []
                content.append(Paragraph(line.strip(), heading_style))
            else:
                if line.strip():
                    if line.strip().startswith('•') or line.strip().startswith('-'):
                        line = f"    • {line.strip()[1:].strip()}"
                    current_section.append(line)
        
        if current_section:
            content.append(Paragraph('<br/>'.join(current_section), normal_style))
        
        doc.build(content)
        buffer.seek(0)
        return buffer