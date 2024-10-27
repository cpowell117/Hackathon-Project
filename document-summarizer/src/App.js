// src/App.js

import React from 'react';
import UploadForm from './components/UploadForm';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>Document Summarization and Compliance Reports</h1>
      <UploadForm />
      <AnalyticsDashboard />
    </div>
  );
}

export default App;
