// src/App.js

import React from 'react';
import UploadForm from './components/UploadForm';
import DataVisualization from './components/DataVisualization';

function App() {
  const data = [
    { name: 'Income', value: 4000 },
    { name: 'Expenses', value: 2400 },
  ];

  return (
    <div className="App">
      <h1>Document Summarization and Compliance Reports</h1>
      <UploadForm />
      <DataVisualization data={data} />
    </div>
  );
}

export default App;
