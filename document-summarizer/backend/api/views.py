# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import PyPDF2

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')  # Get the uploaded file
        
        if file.content_type == 'application/pdf':
            text = self.extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')

        # Simulate Claude's summarization
        summary = self.summarize_text(text)
        
        return Response({'summary': summary})

    def extract_text_from_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)  # Updated to use PdfReader
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    def summarize_text(self, text):
        # Simulate Claude's response for now
        return f"Summary of the document: {text[:100]}..."  # Mock response for testing
