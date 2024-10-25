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

```bash
git clone https://github.com/yourusername document-summarization-app.git
cd document-summarization-app/backend
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate.bat #On Windows
```

3. Install the dependencies:

```bash
pip install django djangorestframework pypdf2 django-cors-headers
```

or

```bash
pip install -r requirements.txt
```

4. Add CORS support:

Add django-cors-headers to your INSTALLED_APPS and set it up in settings.py as follows:

### backend/backend/settings.py

```python
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
```

5. Run database migrations (although no database is used in this step, it's required for Django setup):

```bash
python manage.py migrate
```

6. Run the Django development server:

```bash
python3 manage.py runserver
```

The backend will now be running on http://localhost:8000.

Frontend (React) Setup
1. Navigate to the frontend folder **:

```bash
cd .\document-summarizer\
```

2. Install the required NPM dependencies:

```bash
npm install
```

3. Start the React development server:

```bash
npm start
```

The frontend will be available at http://localhost:3000.