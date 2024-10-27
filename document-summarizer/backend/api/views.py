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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

load_dotenv()

CLAUDE_API_KEY = os.getenv('AT_KEY')


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    def post(self, request, *args, **kwargs):
        try:
            print("Received upload request")
        
            # Check if file is present in request
            file = request.FILES.get('file')
            if not file:
                print("No file provided in request")
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            print("File received:", file.name)
        
            # Check file type
            if file.content_type == 'application/pdf':
                text = self.extract_text_from_pdf(file)
            else:
                text = file.read().decode('utf-8')

            print("Extracted text:", text[:100])  # Print first 100 characters of text for debugging

            # Analyze text with Claude API
            analysis = self.analyze_with_claude(text)

            # Generate PDF from analysis
            pdf_buffer = self.generate_pdf(analysis)

            # Prepare response with PDF download
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

            # Print the response text from Claude for debugging
            print("Claude Response Text:", response.content[0].text)

            # Parse JSON section from Claude's response for chart data
            analysis_text = response.content[0].text
            analytics_data = self.parse_claude_json(analysis_text)
            return {"analysis_text": analysis_text, "analytics_data": analytics_data}

        except anthropic.RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later.")
        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing text: {str(e)}")
        
    def parse_claude_json(self, response_text):
        import json
        try:
            # Attempt to extract JSON structure from Claude's response
            start_index = response_text.find("{")
            end_index = response_text.rfind("}") + 1
            json_data = response_text[start_index:end_index]
            return json.loads(json_data)
        except json.JSONDecodeError:
            raise Exception("Failed to parse JSON data from Claude's response.")

    def get_in_depth_analytics(self, analysis_text):
        # Mock structured analytics data here
        analytics_data = {
            "financial_performance": {
                "revenue": 10000,
                "profit": 2000,
                "growth_rate": 5.0
            },
            "business_segment_breakdown": [
                {"segment": "Gaming", "value": 5000},
                {"segment": "Data Center", "value": 3000},
                {"segment": "Professional Visualization", "value": 2000}
            ],
            "strategic_initiative_impact": [
                {"initiative": "AI Development", "impact": "High"},
                {"initiative": "Sustainable Tech", "impact": "Medium"}
            ],
            "swot_analysis": {
                "strengths": ["Strong brand", "High R&D investment"],
                "weaknesses": ["High operational costs"],
                "opportunities": ["Growing AI market"],
                "threats": ["Competitive market"]
            },
            "conclusion_recommendations": "Continue focusing on AI and sustainable technology."
        }
        return analytics_data

    def generate_pdf(self, analysis):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        content = [Paragraph("Document Analysis Report", styles['Heading1']), Paragraph("<br/><br/>", styles['Normal'])]
        
        for line in analysis.split('\n'):
            if line.strip().upper() == line.strip():
                content.append(Paragraph(line.strip(), styles['Heading2']))
            else:
                content.append(Paragraph(line.strip(), styles['Normal']))
        
        doc.build(content)
        buffer.seek(0)
        return buffer


class InDepthAnalyticsView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        file_upload_view = FileUploadView()
        analytics_data = file_upload_view.get_in_depth_analytics(text)
        return Response(analytics_data, status=status.HTTP_200_OK)
