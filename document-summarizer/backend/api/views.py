# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import HttpResponse
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if file.content_type == 'application/pdf':
            text = self.extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')

        summary = self.summarize_text(text)

        pdf_buffer = self.generate_pdf(summary)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="summary.pdf"'
        
        return response

    def extract_text_from_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    def summarize_text(self, text):
        return f"Summary of the document: {text[:100]}..." 

    def generate_pdf(self, summary):
        buffer = BytesIO()

        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Document Summary:")
        p.drawString(100, 730, summary) 

        p.showPage()
        p.save()

        buffer.seek(0)

        return buffer
