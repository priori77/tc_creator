# 테스트 케이스 생성기 (TestCase Creator)

PDF 문서에서 요구사항을 추출하고 AI를 활용하여 테스트 케이스를 자동으로 생성하는 웹 애플리케이션입니다.

## 주요 기능

- PDF 파일 업로드 및 텍스트 추출
- OpenAI API를 활용한 테스트 케이스 자동 생성
- 생성된 테스트 케이스 Excel 파일 다운로드
- 사용자 친화적인 웹 인터페이스

## 기술 스택

### 프론트엔드
- React 18
- Vite
- Tailwind CSS
- React Dropzone (파일 업로드)
- Axios (API 통신)

### 백엔드
- Flask (Python 웹 프레임워크)
- OpenAI API (GPT 모델)
- PyPDF2 (PDF 텍스트 추출)
- Pandas (Excel 파일 생성)

## 프로젝트 구조

```
testcase_creator/
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── components/      # 리액트 컴포넌트
│   │   │   ├── FileUploader.jsx       # PDF 파일 업로드 컴포넌트
│   │   │   ├── TestCasePreview.jsx    # 테스트 케이스 미리보기
│   │   │   ├── DownloadSection.jsx    # 다운로드 기능 컴포넌트
│   │   │   ├── ProgressBar.jsx        # 진행 상태 표시
│   │   │   ├── TextDisplay.jsx        # 텍스트 표시 컴포넌트
│   │   │   └── ErrorAlert.jsx         # 오류 알림 컴포넌트
│   │   ├── App.jsx          # 메인 애플리케이션 로직
│   │   └── main.jsx         # 진입점
│   ├── index.html           # HTML 템플릿
│   └── package.json         # 프론트엔드 의존성
│
├── backend/                 # Flask 백엔드
│   ├── src/
│   │   ├── llm/             # LLM 관련 모듈
│   │   │   ├── openai_client.py       # OpenAI API 클라이언트
│   │   │   └── example_loader.py      # 예제 로더
│   │   ├── pdf_processor/   # PDF 처리 모듈
│   │   └── utils/           # 유틸리티 함수
│   ├── app.py              # 플라스크 애플리케이션
│   ├── .env                # 환경 변수 설정
│   └── requirements.txt    # 백엔드 의존성
│
└── tccreator_example/      # 참조용 예제 코드
```

## 설치 및 실행 방법

### 사전 요구사항
- Node.js 16 이상
- Python 3.8 이상
- OpenAI API 키

### 프론트엔드 설정
```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 백엔드 설정
```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상 환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
# .env 파일에 OPENAI_API_KEY 설정

# 서버 실행
python app.py
```

## 사용 방법
1. 웹 브라우저에서 프론트엔드 서버 주소로 접속 (기본: http://localhost:5173)
2. PDF 파일을 업로드 영역에 드래그 앤 드롭 또는 클릭하여 선택
3. 업로드된 PDF에서 추출된 텍스트 확인
4. '테스트 케이스 생성' 버튼 클릭
5. 생성된 테스트 케이스 확인 후 Excel 파일 다운로드

## 라이센스
이 프로젝트는 MIT 라이센스를 따릅니다. 
