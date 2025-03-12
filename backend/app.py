import sys
import os
from dotenv import load_dotenv
import openai

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 로드 - 여러 위치 시도
dotenv_paths = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),  # backend/.env
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')  # 루트 .env
]

for dotenv_path in dotenv_paths:
    if os.path.exists(dotenv_path):
        print(f"환경 설정 파일을 로드합니다: {dotenv_path}")
        load_dotenv(dotenv_path)
        break

# OpenAI API 키 직접 설정
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API 키 설정 완료: {api_key[:10]}...")
    # 새 버전 API 키 설정 방식
    openai.api_key = api_key
    # 기존 클래스 생성자 방식으로도 설정 (새 버전 대비)
    try:
        openai_client = openai.OpenAI(api_key=api_key)
        print("OpenAI 클라이언트 초기화 성공")
    except Exception as e:
        print(f"OpenAI 클라이언트 초기화 실패: {e}")
else:
    print("경고: API 키를 찾을 수 없습니다!")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
# 기존 import 유지

app = Flask(__name__)
CORS(app)  # CORS 설정 - 중요!
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

# 업로드 폴더가 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from src.utils.config import Config

# 앱 초기화 시 설정 확인
Config.init_app()

# API 키 상태 확인 (하드코딩 제거)
print(f"현재 OPENAI_API_KEY 환경 변수: {'설정됨' if os.environ.get('OPENAI_API_KEY') else '설정되지 않음'}")

# API 키가 없으면 경고만 표시
if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY in ["your_api_key_here", "sk-actual_api_key_goes_here", "sk-your_actual_api_key_here"]:
    print("=== 경고: 유효한 OpenAI API 키가 설정되지 않았습니다. 테스트 데이터만 생성됩니다. ===")
    print("=== .env 파일을 확인하고 실제 API 키를 설정하세요. ===")

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다'}), 400
        
        file = request.files['file']
        print(f"업로드된 파일: {file.filename}, 타입: {file.content_type}")
        
        if file.filename == '':
            return jsonify({'error': '선택된 파일이 없습니다'}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'PDF 파일만 업로드 가능합니다'}), 400
        
        # 파일 저장
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"파일 저장됨: {file_path}")
        
        # PDF에서 텍스트 추출
        import src.pdf_processor.extractor as extractor
        print("PDF 텍스트 추출 시작...")
        extracted_text = extractor.extract_text_from_pdf(file_path)
        
        # 추출된 텍스트 일부 출력 (디버깅용)
        if extracted_text:
            preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
            print(f"텍스트 추출 결과 (일부): {preview}")
        else:
            print("추출된 텍스트 없음")
        
        if not extracted_text or extracted_text.strip() == '':
            return jsonify({'error': 'PDF에서 텍스트를 추출할 수 없습니다. 텍스트 기반 PDF인지 확인하세요.'}), 400
        
        return jsonify({
            'success': True, 
            'text': extracted_text, 
            'file_path': file_path
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"PDF 처리 중 오류 발생: {error_details}")
        return jsonify({'error': f'PDF 처리 중 오류 발생: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    file_path = data.get('file_path')
    extracted_text = data.get('text')
    
    if not extracted_text:
        return jsonify({'error': '추출된 텍스트가 없습니다'}), 400
    
    try:
        # 예시 테스트 케이스 로드
        import src.llm.example_loader as example_loader
        examples = example_loader.load_examples()
        
        # OpenAI API를 사용하여 테스트 케이스 생성
        import src.llm.openai_client as openai_client
        test_cases = openai_client.generate_test_cases(extracted_text, examples)
        
        # Excel 파일 생성
        import src.excel.generator as generator
        excel_path = generator.generate_excel(test_cases)
        
        # 테스트 케이스 데이터와 Excel 경로 모두 반환
        return jsonify({
            'success': True, 
            'excel_path': excel_path,
            'test_cases': test_cases  # 테스트 케이스 데이터 추가
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"오류 발생: {error_details}")
        return jsonify({'error': f'테스트 케이스 생성 중 오류 발생: {str(e)}'}), 500

@app.route('/api/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 