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
    } else {
      setFile(null);
      setErrorMessage('Please select a valid PDF file.');
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
    } catch (error) {
      console.error('File upload failed:', error);
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
      >
        Upload and Summarize
      </Button>

      {pdfUrl && (
        <div>
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
