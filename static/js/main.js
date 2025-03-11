document.addEventListener('DOMContentLoaded', function() {
    // 요소 참조
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const removeFileBtn = document.getElementById('removeFile');
    const generateBtn = document.getElementById('generateBtn');
    const progressSection = document.getElementById('progressSection');
    const progressBar = document.getElementById('progressBar');
    const progressStatus = document.getElementById('progressStatus');
    const resultSection = document.getElementById('resultSection');
    const downloadBtn = document.getElementById('downloadBtn');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    const retryBtn = document.getElementById('retryBtn');
    
    let uploadedFile = null;
    let extractedText = null;
    let filePath = null;
    let excelPath = null;
    
    // 드래그 앤 드롭 이벤트
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('dragover');
    }
    
    function unhighlight() {
        dropArea.classList.remove('dragover');
    }
    
    // 파일 드롭 처리
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            handleFiles(files);
        }
    }
    
    // 파일 선택 처리
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            handleFiles(this.files);
        }
    });
    
    function handleFiles(files) {
        const file = files[0];
        
        // PDF 파일 확인
        if (file.type !== 'application/pdf') {
            showError('PDF 파일만 업로드 가능합니다.');
            return;
        }
        
        uploadedFile = file;
        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        
        // 파일 업로드
        uploadFile(file);
    }
    
    // 파일 제거
    removeFileBtn.addEventListener('click', () => {
        resetUI();
    });
    
    function resetUI() {
        uploadedFile = null;
        extractedText = null;
        filePath = null;
        excelPath = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        progressSection.style.display = 'none';
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        progressBar.style.width = '0%';
    }
    
    // 파일 업로드
    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // 진행 상태 표시 시작
        progressSection.style.display = 'block';
        progressStatus.textContent = 'PDF 파일 처리 중...';
        progressBar.style.width = '30%';
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            extractedText = data.text;
            filePath = data.file_path;
            progressBar.style.width = '60%';
            progressStatus.textContent = '텍스트 추출 완료.';
        })
        .catch(error => {
            showError('파일 업로드 중 오류가 발생했습니다: ' + error.message);
        });
    }
    
    // 테스트 케이스 생성
    generateBtn.addEventListener('click', () => {
        if (!extractedText) {
            showError('먼저 PDF 파일을 업로드하세요.');
            return;
        }
        
        progressSection.style.display = 'block';
        progressStatus.textContent = '테스트 케이스 생성 중...';
        progressBar.style.width = '70%';
        
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: extractedText,
                file_path: filePath
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            excelPath = data.excel_path;
            progressBar.style.width = '100%';
            progressStatus.textContent = '테스트 케이스 생성 완료!';
            
            // 결과 섹션 표시
            setTimeout(() => {
                progressSection.style.display = 'none';
                resultSection.style.display = 'block';
            }, 500);
        })
        .catch(error => {
            showError('테스트 케이스 생성 중 오류가 발생했습니다: ' + error.message);
        });
    });
    
    // 다운로드 처리
    downloadBtn.addEventListener('click', () => {
        if (!excelPath) {
            showError('다운로드할 파일이 없습니다.');
            return;
        }
        
        window.location.href = `/download/${encodeURIComponent(excelPath)}`;
    });
    
    // 오류 표시
    function showError(message) {
        errorMessage.textContent = message;
        progressSection.style.display = 'none';
        errorSection.style.display = 'block';
    }
    
    // 재시도 처리
    retryBtn.addEventListener('click', () => {
        errorSection.style.display = 'none';
        if (uploadedFile) {
            fileInfo.style.display = 'block';
        } else {
            resetUI();
        }
    });
}); 