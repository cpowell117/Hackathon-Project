// src/components/UploadForm.js

import React, { useState } from 'react';
import axios from 'axios';
import { Button, Input } from '@mui/material';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');

  // Function to handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Function to upload file and get summary
  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Post request to backend
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSummary(response.data.summary);
    } catch (error) {
      console.error('File upload failed:', error);
    }
  };

  return (
    <div>
      <Input type="file" onChange={handleFileChange} />
      <Button variant="contained" color="primary" onClick={handleFileUpload}>
        Upload and Summarize
      </Button>
      {summary && <div><h2>Document Summary:</h2><p>{summary}</p></div>}
    </div>
  );
};

export default UploadForm;
