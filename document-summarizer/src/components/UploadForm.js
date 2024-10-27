import React, { useState } from 'react';
import axios from 'axios';
import { Button, Input, Typography } from '@mui/material';
import AnalyticsDashboard from './AnalyticsDashboard';
import './UploadForm.css';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [pdfUrl, setPdfUrl] = useState(null);
  const [analysisText, setAnalysisText] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setErrorMessage('');
      setPdfUrl(null);
      setAnalysisText('');
    } else {
      setFile(null);
      setErrorMessage('Please select a valid PDF file.');
      setPdfUrl(null);
      setAnalysisText('');
    }
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      setPdfUrl(url);
      setErrorMessage('');

      const analysisResponse = await axios.post('http://localhost:8000/api/in-depth-analytics/', { text: 'Sample text for analysis' });
      setAnalysisText(analysisResponse.data);

    } catch (error) {
      console.error('File upload failed:', error);
      setErrorMessage('File upload failed. Please try again.');
    }
  };

  return (
    <div className="upload-form">
      <Typography variant="h4" gutterBottom style={{ color: '#333', fontWeight: 'bold' }}>
      Make your Data Smarter
      </Typography>
      
      <div className="button-container">
        <label htmlFor="file-upload">
          <Button
            variant="contained"
            component="span"
            color="primary"
            style={{ fontWeight: 'bold', marginBottom: '10px' }}
          >
            Choose File
          </Button>
        </label>
        <Input
          id="file-upload"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        <Button
          variant="contained"
          color="secondary"
          onClick={handleFileUpload}
          disabled={!file}
          style={{ fontWeight: 'bold' }}
        >
          Upload and Summarize
        </Button>
      </div>

      {errorMessage && <Typography color="error" style={{ marginTop: '10px' }}>{errorMessage}</Typography>}

      {pdfUrl && (
        <div style={{ marginTop: '20px' }}>
          <Button
            variant="contained"
            color="success"
            href={pdfUrl}
            download="summary.pdf"
            style={{ fontWeight: 'bold' }}
          >
            Download Summary
          </Button>
        </div>
      )}

      {analysisText && <AnalyticsDashboard analysisText={analysisText} />}
    </div>
  );
};

export default UploadForm;
