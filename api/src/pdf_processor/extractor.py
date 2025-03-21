import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """PDF 파일에서 텍스트를 추출합니다."""
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
        return "PDF에서 텍스트를 추출할 수 없습니다. 텍스트 기반 PDF인지 확인하세요." 