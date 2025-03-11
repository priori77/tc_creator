from flask import Flask, render_template, request, jsonify, send_file
import os
from src.pdf_processor.extractor import extract_text_from_pdf
from src.llm.openai_client import generate_test_cases
from src.excel.generator import generate_excel
from src.llm.example_loader import load_examples

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'  # Vercel의 임시 디렉토리 사용
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

# 업로드 폴더가 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'PDF 파일만 업로드 가능합니다'}), 400
    
    # 파일 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # PDF에서 텍스트 추출
    try:
        extracted_text = extract_text_from_pdf(file_path)
        return jsonify({'success': True, 'text': extracted_text, 'file_path': file_path})
    except Exception as e:
        return jsonify({'error': f'PDF 처리 중 오류 발생: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    file_path = data.get('file_path')
    extracted_text = data.get('text')
    
    if not extracted_text:
        return jsonify({'error': '추출된 텍스트가 없습니다'}), 400
    
    try:
        # 예시 테스트 케이스 로드
        examples = load_examples()
        
        # OpenAI API를 사용하여 테스트 케이스 생성
        test_cases = generate_test_cases(extracted_text, examples)
        
        # Excel 파일 생성 (Vercel의 임시 디렉토리 사용)
        output_dir = '/tmp/output'
        os.makedirs(output_dir, exist_ok=True)
        excel_path = generate_excel(test_cases, output_path=os.path.join(output_dir, 'test_cases.xlsx'))
        
        return jsonify({'success': True, 'excel_path': excel_path})
    except Exception as e:
        return jsonify({'error': f'테스트 케이스 생성 중 오류 발생: {str(e)}'}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'파일 다운로드 중 오류 발생: {str(e)}'}), 500

# Vercel 서버리스 함수를 위한 핸들러
app.debug = False
app.testing = False

# 서버리스 환경에서 필요한 WSGI 핸들러
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Vercel 서버리스 환경에서 사용됨
    pass 