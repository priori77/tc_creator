import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정을 관리하는 클래스"""
    
    # API 설정
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # 기본값 설정
    
    # 파일 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
    
    @classmethod
    def init_app(cls):
        """필수 설정 값 검증"""
        if not cls.OPENAI_API_KEY:
            print("경고: OPENAI_API_KEY가 설정되지 않았습니다. 테스트 모드로 동작합니다.")
        
        # 필요한 디렉토리 생성
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.OUTPUT_FOLDER, exist_ok=True) 