import React from 'react';
import { ProgressBar as BootstrapProgressBar } from 'react-bootstrap';

function ProgressBar({ progress, status }) {
  return (
    <div className="progress-section my-4">
      <div className="progress-container p-4 bg-white rounded shadow-sm">
        <BootstrapProgressBar 
          now={progress} 
          variant="primary" 
          animated 
          className="mb-3" 
        />
        <p className="text-center mb-0">{status}</p>
      </div>
    </div>
  );
}

export default ProgressBar; 