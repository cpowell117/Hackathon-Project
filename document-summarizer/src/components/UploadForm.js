import React, { useState } from 'react';
import axios from 'axios';
import { Button, Input, Typography } from '@mui/material';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [pdfUrl, setPdfUrl] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setErrorMessage('');
      setPdfUrl(null); // Clear previous PDF URL on new file selection
    } else {
      setFile(null);
      setErrorMessage('Please select a valid PDF file.');
      setPdfUrl(null); // Clear previous PDF URL if an invalid file is selected
    }
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Post request to backend
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      setPdfUrl(url);
      setErrorMessage(''); // Clear error message on successful upload
    } catch (error) {
      console.error('File upload failed:', error);
      setErrorMessage('File upload failed. Please try again.');
    }
  };

  return (
    <div>
      <Input type="file" accept="application/pdf" onChange={handleFileChange} />
      {errorMessage && <Typography color="error">{errorMessage}</Typography>}
      <Button
        variant="contained"
        color="primary"
        onClick={handleFileUpload}
        disabled={!file}
        style={{ marginTop: '10px' }}
      >
        Upload and Summarize
      </Button>

      {pdfUrl && !errorMessage && (
        <div style={{ marginTop: '20px' }}>
          <Button
            variant="contained"
            color="secondary"
            href={pdfUrl}
            download="summary.pdf"
          >
            Download Summary
          </Button>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
