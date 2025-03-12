import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, Button } from 'react-bootstrap';
import '../styles/FileUploader.css';

function FileUploader({ file, setFile, setExtractedText, setFilePath, setProgress, setStatus, setShowProgress, setError, onGenerateClick }) {
  
  const onDrop = useCallback(acceptedFiles => {
    const selectedFile = acceptedFiles[0];
    
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      setError('PDF 파일만 업로드 가능합니다.');
      return;
    }
    
    setFile(selectedFile);
    uploadFile(selectedFile);
  }, [setFile, setError, setExtractedText, setFilePath, setProgress, setStatus, setShowProgress]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    }
  });

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    setShowProgress(true);
    setStatus('PDF 파일 처리 중...');
    setProgress(30);
    
    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        setError(`서버 응답 오류: ${response.status} - ${data.error || '알 수 없는 오류'}`);
        setShowProgress(false);
        return;
      }
      
      if (data.error) {
        setError(data.error);
        setShowProgress(false);
        return;
      }
      
      // 텍스트 길이 확인
      if (!data.text || data.text.length < 50) {
        setError('PDF에서 추출된 텍스트가 너무 적습니다. 다른 PDF 파일을 시도해보세요.');
        setShowProgress(false);
        return;
      }
      
      setExtractedText(data.text);
      setFilePath(data.file_path);
      setProgress(60);
      setStatus('텍스트 추출 완료. 텍스트 길이: ' + data.text.length + '자');
      setShowProgress(false);
    } catch (error) {
      console.error('파일 업로드 오류:', error);
      setError('파일 업로드 중 오류가 발생했습니다: ' + error.message);
      setShowProgress(false);
    }
  };

  return (
    <div className="upload-section">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
        </div>
        <p>PDF 파일을 여기에 드래그하거나 클릭하여 업로드하세요</p>
        <p className="small text-muted">(업로드 가능한 최대 파일 크기는 16MB입니다.)</p>
      </div>

      {file && (
        <Card className="mt-3 file-info">
          <Card.Body>
            <div className="d-flex justify-content-between align-items-center">
              <span>{file.name}</span>
              <Button 
                variant="link" 
                className="text-danger p-0" 
                onClick={() => setFile(null)}
              >
                삭제
              </Button>
            </div>
            <Button 
              variant="primary" 
              className="w-100 mt-3" 
              onClick={onGenerateClick}
            >
              테스트 케이스 생성
            </Button>
          </Card.Body>
        </Card>
      )}
    </div>
  );
}

export default FileUploader; 