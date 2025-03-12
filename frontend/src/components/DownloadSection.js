import React from 'react';
import { Button } from 'react-bootstrap';

function DownloadSection({ excelPath }) {
  const handleDownload = () => {
    if (!excelPath) {
      alert('다운로드할 파일이 없습니다.');
      return;
    }
    
    window.location.href = `http://localhost:5000/api/download/${encodeURIComponent(excelPath)}`;
  };

  return (
    <div className="download-section text-center my-4">
      <p>테스트 케이스가 Excel 파일로 생성되었습니다.</p>
      <Button 
        variant="primary" 
        size="lg" 
        onClick={handleDownload}
      >
        Excel 파일 다운로드
      </Button>
    </div>
  );
}

export default DownloadSection; 