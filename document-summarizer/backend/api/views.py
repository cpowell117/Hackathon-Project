from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import HttpResponse
import PyPDF2
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
import anthropic
import os
from dotenv import load_dotenv
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

CLAUDE_API_KEY = os.getenv('AT_KEY')

cached_json_data = {}

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    def post(self, request, *args, **kwargs):
        try:
            print("Received upload request")

            file = request.FILES.get('file')
            if not file:
                print("No file provided in request")
                return Response(
                    {'error': 'No file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            print("File received:", file.name)

            if file.content_type == 'application/pdf':
                text = self.extract_text_from_pdf(file)
            else:
                text = file.read().decode('utf-8')

            print("Extracted text:", text[:100]) 

            analysis = self.analyze_with_claude(text)

            cached_json_data['json'] = analysis['analytics_data']

            pdf_buffer = self.generate_pdf(analysis['analysis_text'])

            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="analysis.pdf"'

            print("PDF generation successful")
            return response

        except Exception as e:
            print("Error during file upload handling:", e)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def extract_text_from_pdf(self, pdf_file):
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''.join([page.extract_text() for page in reader.pages])
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")

    def analyze_with_claude(self, text):
        try:
            prompt = """
            Please analyze this document and provide:
            1. Executive Summary (2-3 sentences)
            2. Key Points (main ideas and findings)
            3. Detailed Analysis (important details and insights)
            4. Conclusions and Recommendations
            5. Quantitative Data for Analytics (structured data in JSON format) including:
               - Financial Performance (Revenue, Profit, Growth Rate)
               - Business Segment Breakdown
               - Strategic Initiative Impact
               - SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)

            Return the quantitative data formatted as JSON to facilitate chart creation.
            Format the response with clear headings and bullet points where appropriate.
            """
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": f"{prompt}\n\nDocument text:\n{text}"}],
                max_tokens=4000,
                temperature=0.5
            )
            print("Claude Response Text:", response.content[0].text)

            analysis_text = response.content[0].text
            analytics_data = self.parse_claude_json(analysis_text)

            return {"analysis_text": self.clean_analysis_text(analysis_text), "analytics_data": analytics_data}

        except anthropic.RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later.")
        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing text: {str(e)}")

    def parse_claude_json(self, response_text):
        import json
        try:
            # Here is a basic and hardcoded filter method to obtain the JSON
            start_index = response_text.find("```json")
            end_index = response_text.find("```", start_index + 7)

            if start_index == -1 or end_index == -1:
                raise Exception("No JSON data found between the expected markers")

            json_data = response_text[start_index + 7:end_index].strip()

            return json.loads(json_data)
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error extracting JSON from response: {str(e)}")

    def clean_analysis_text(self, analysis_text):
        cleaned_text = analysis_text.split("5. Quantitative Data (JSON format)")[0].strip()
        
        cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()

        return cleaned_text

    def generate_pdf(self, analysis_text):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        content = [Paragraph("Document Analysis Report", styles['Heading1']), Paragraph("<br/><br/>", styles['Normal'])]

        for line in analysis_text.split('\n'):
            if line.strip().upper() == line.strip():
                content.append(Paragraph(line.strip(), styles['Heading2']))
            else:
                content.append(Paragraph(line.strip(), styles['Normal']))

        doc.build(content)
        buffer.seek(0)
        return buffer

    def get_in_depth_analytics(self):
        if 'json' not in cached_json_data:
            raise Exception("No cached analytics data available.")
        return cached_json_data['json']


class InDepthAnalyticsView(APIView):
    def post(self, request):
        try:
            file_upload_view = FileUploadView()
            # Ths is for getting cached analytics from the last analysis in order to botain the JSON
            analytics_data = file_upload_view.get_in_depth_analytics()
            return Response(analytics_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
