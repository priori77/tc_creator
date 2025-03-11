import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    PDF 파일에서 텍스트를 추출합니다.
    
    Args:
        pdf_path (str): PDF 파일 경로
        
    Returns:
        str: 추출된 텍스트
    """
    extracted_text = ""
    
    # PyPDF2를 사용하여 텍스트 추출
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted_text += page.extract_text() + "\n"
    
    return extracted_text 