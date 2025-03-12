import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import FileUploader from './components/FileUploader';
import ProgressBar from './components/ProgressBar';
import TestCasePreview from './components/TestCasePreview';
import DownloadSection from './components/DownloadSection';
import ErrorAlert from './components/ErrorAlert';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState(null);
  const [filePath, setFilePath] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [showProgress, setShowProgress] = useState(false);
  const [testCases, setTestCases] = useState([]);
  const [excelPath, setExcelPath] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [error, setError] = useState(null);

  const resetState = () => {
    setFile(null);
    setExtractedText(null);
    setFilePath(null);
    setProgress(0);
    setStatus('');
    setShowProgress(false);
    setTestCases([]);
    setExcelPath(null);
    setShowResult(false);
    setError(null);
  };

  const handleGenerateClick = async () => {
    if (!extractedText) {
      setError('먼저 PDF 파일을 업로드하세요.');
      return;
    }

    setShowProgress(true);
    setStatus('테스트 케이스 생성 중...');
    setProgress(70);

    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: extractedText,
          file_path: filePath
        }),
      });

      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
        return;
      }

      setExcelPath(data.excel_path);
      if (data.test_cases && Array.isArray(data.test_cases)) {
        setTestCases(data.test_cases);
      }

      setProgress(100);
      setStatus('테스트 케이스 생성 완료!');
      
      setTimeout(() => {
        setShowProgress(false);
        setShowResult(true);
      }, 500);
    } catch (error) {
      setError('테스트 케이스 생성 중 오류가 발생했습니다: ' + error.message);
    }
  };

  return (
    <Container className="py-4">
      <header className="text-center mb-5">
        <h1 className="display-4 text-primary">게임 테스트 케이스 생성기</h1>
        <p className="lead">기획서 PDF 파일을 업로드하여 테스트 케이스를 자동으로 생성하세요.</p>
        <p className="small text-muted bg-light py-1 px-2 d-inline-block">
          ※ 주의: 텍스트를 추출할 수 있는 PDF 파일만 지원됩니다. 이미지 형태의 PDF는 정상 처리되지 않을 수 있습니다.
        </p>
      </header>

      <Row className="justify-content-center">
        <Col md={10}>
          {!showResult && !showProgress && !error && (
            <FileUploader
              file={file}
              setFile={setFile}
              setExtractedText={setExtractedText}
              setFilePath={setFilePath}
              setProgress={setProgress}
              setStatus={setStatus}
              setShowProgress={setShowProgress}
              setError={setError}
              onGenerateClick={handleGenerateClick}
            />
          )}

          {showProgress && (
            <ProgressBar progress={progress} status={status} />
          )}

          {showResult && (
            <div className="result-section">
              <TestCasePreview testCases={testCases} />
              <DownloadSection excelPath={excelPath} />
              <button 
                className="btn btn-secondary mt-3"
                onClick={resetState}
              >
                다시 시작하기
              </button>
            </div>
          )}

          {error && (
            <ErrorAlert 
              message={error} 
              onRetry={() => {
                setError(null);
                if (file) {
                  setShowProgress(false);
                } else {
                  resetState();
                }
              }} 
            />
          )}
        </Col>
      </Row>

      <footer className="text-center mt-5 pt-3 border-top text-muted">
        <p>&copy; 2025 LLM 기반 TC 생성기 - 서준석</p>
      </footer>
    </Container>
  );
}

export default App; 