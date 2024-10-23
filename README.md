# Hackathon-Project:

Document Summarization and Compliance Reports Application

This project is a web-based application that allows users to upload PDF or text documents, and receive a summarized version. The backend is powered by Django and Django REST Framework, and the frontend is built using React.

Features
- Document Upload: Users can upload PDF or text files.
- Mock AI Summarization: The backend extracts text from the document (using PyPDF2 for PDFs) and returns a mock summary for now.
- Frontend-Backend Integration: The frontend and backend communicate using Axios and Django REST Framework.

Prerequisites
- Python 3.x
- Node.js (for frontend development)
- npm (Node Package Manager)

Setup Instructions
Backend (Django) Setup
1. Clone the repository:

Copy the code bellow:
git clone https://github.com/yourusername document-summarization-app.git
cd document-summarization-app/backend

2. Create a virtual environment:

Copy the code bellow:
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# On Windows, use venv\Scripts\activate

3. Install the dependencies:

Copy the code bellow:
pip install django djangorestframework pypdf2 django-cors-headers

4. Add CORS support:

Add django-cors-headers to your INSTALLED_APPS and set it up in settings.py as follows:

Copy the code bellow:
# backend/settings.py

INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    'api',  # Your app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    # Other middleware...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Allow frontend on localhost
]

5. Run database migrations (although no database is used in this step, it's required for Django setup):

Copy the code bellow:
python manage.py migrate

6. Run the Django development server:

Copy the code bellow:
python manage.py runserver

The backend will now be running on http://localhost:8000.

Frontend (React) Setup
1. Navigate to the frontend folder:

Copy the code bellow:
cd ../document-summarizer

2. Install the required NPM dependencies:

Copy the code bellow:
npm install

3. Start the React development server:

Copy the code bellow:
npm start

The frontend will be available at http://localhost:3000.