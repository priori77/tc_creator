import PyPDF2
import os
import subprocess
import tempfile
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """PDF 파일에서 텍스트를 추출합니다. 여러 방법을 시도합니다."""
    # 방법 1: PyPDF2 사용
    text = extract_with_pypdf2(pdf_path)
    if text and len(text.strip()) > 100:  # 충분한 텍스트가 추출되었는지 확인
        return text
    
    # 방법 2: pdfminer 사용 (설치된 경우)
    try:
        text = extract_with_pdfminer(pdf_path)
        if text and len(text.strip()) > 100:
            return text
    except ImportError:
        print("pdfminer.six가 설치되어 있지 않습니다. pip install pdfminer.six로 설치하세요.")
    
    # 방법 3: 외부 도구 사용 (가능한 경우)
    try:
        text = extract_with_external_tool(pdf_path)
        if text and len(text.strip()) > 100:
            return text
    except Exception as e:
        print(f"외부 도구 사용 중 오류: {e}")
    
    # 기본 PyPDF2 결과 반환 (위의 모든 방법이 실패한 경우)
    return text or "PDF에서 텍스트를 추출할 수 없습니다. 텍스트 기반 PDF인지 확인하세요."

def extract_with_pypdf2(pdf_path):
    """PyPDF2를 사용하여 텍스트 추출"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        print(f"PyPDF2 텍스트 추출 중 오류 발생: {e}")
        return ""

def extract_with_pdfminer(pdf_path):
    """pdfminer.six를 사용하여 텍스트 추출"""
    from pdfminer.high_level import extract_text as pdfminer_extract
    try:
        return pdfminer_extract(pdf_path)
    except Exception as e:
        print(f"pdfminer 텍스트 추출 중 오류 발생: {e}")
        return ""

def extract_with_external_tool(pdf_path):
    """외부 도구(예: pdftotext)를 사용하여 텍스트 추출"""
    # pdftotext가 설치되어 있는지 확인
    try:
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        # pdftotext 명령어 실행
        subprocess.run(['pdftotext', pdf_path, tmp_path], check=True, capture_output=True)
        
        # 결과 읽기
        with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
        
        # 임시 파일 삭제
        os.unlink(tmp_path)
        return text
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"외부 도구 실행 오류: {e}")
        return "" 