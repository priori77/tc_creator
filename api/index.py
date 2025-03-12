import sys
import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# 상대 경로 처리를 위한 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 로드
dotenv_paths = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
]

for dotenv_path in dotenv_paths:
    if os.path.exists(dotenv_path):
        print(f"환경 설정 파일을 로드합니다: {dotenv_path}")
        load_dotenv(dotenv_path)
        break

# Config 클래스 및 기타 임포트
from src.utils.config import Config

# 앱 초기화
app = Flask(__name__)
CORS(app)

# Config 초기화
Config.init_app()

# OpenAI API 키 설정
api_key = os.getenv("OPENAI_API_KEY") or Config.OPENAI_API_KEY
if api_key:
    openai.api_key = api_key
    try:
        openai_client = openai.OpenAI(api_key=api_key)
    except Exception as e:
        print(f"OpenAI 클라이언트 초기화 실패: {e}")
else:
    print("경고: API 키를 찾을 수 없습니다!")

# 환경 변수 설정
upload_folder = Config.UPLOAD_FOLDER if hasattr(Config, 'UPLOAD_FOLDER') else 'uploads'
max_content_length = Config.MAX_CONTENT_LENGTH if hasattr(Config, 'MAX_CONTENT_LENGTH') else 16 * 1024 * 1024

# 서버리스 환경에서는 /tmp 폴더를 사용해야 함
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = int(max_content_length)

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '선택된 파일이 없습니다'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'PDF 파일만 업로드 가능합니다'}), 400
        
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            file_size = os.path.getsize(file_path)
            if file_size > app.config['MAX_CONTENT_LENGTH']:
                os.remove(file_path)
                return jsonify({'error': f'파일 크기가 {app.config["MAX_CONTENT_LENGTH"]/1024/1024:.1f}MB를 초과합니다'}), 413
            
        except Exception as e:
            return jsonify({'error': f'파일 저장 중 오류 발생: {str(e)}'}), 500
        
        try:
            import src.pdf_processor.extractor as extractor
            extracted_text = extractor.extract_text_from_pdf(file_path)
            
            if not extracted_text:
                return jsonify({'error': 'PDF에서 텍스트를 추출할 수 없습니다. 텍스트 기반 PDF인지 확인하세요.'}), 400
            
        except Exception as e:
            return jsonify({'error': f'PDF 텍스트 추출 중 오류 발생: {str(e)}'}), 500
        
        return jsonify({
            'success': True, 
            'text': extracted_text, 
            'file_path': file_path
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'error': f'PDF 처리 중 오류 발생: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    extracted_text = data.get('text')
    
    if not extracted_text:
        return jsonify({'error': '추출된 텍스트가 없습니다'}), 400
    
    try:
        import src.llm.example_loader as example_loader
        examples = example_loader.load_examples()
        
        import src.llm.openai_client as openai_client
        test_cases = openai_client.generate_test_cases(extracted_text, examples)
        
        import src.excel.generator as generator
        excel_path = generator.generate_excel(test_cases)
        
        return jsonify({
            'success': True, 
            'excel_path': excel_path,
            'test_cases': test_cases
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'error': f'테스트 케이스 생성 중 오류 발생: {str(e)}'}), 500

@app.route('/api/download/<path:filename>', methods=['GET'])
def download(filename):
    # 서버리스 환경에서는 /tmp 경로 확인
    if not filename.startswith('/tmp/'):
        filename = os.path.join('/tmp', filename)
    return send_file(filename, as_attachment=True)

# Vercel 서버리스 함수 지원을 위한 handler
def handler(event, context):
    return app(event, context)

# 로컬 개발용
if __name__ == '__main__':
    app.run(debug=True) 