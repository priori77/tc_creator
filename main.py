import argparse
import os
from src.pdf_processor.extractor import extract_text_from_pdf
from src.llm.openai_client import generate_test_cases
from src.excel.generator import generate_excel
from src.llm.example_loader import load_examples

def main():
    parser = argparse.ArgumentParser(description='게임 테스트 케이스 생성기')
    parser.add_argument('--pdf', required=True, help='기획서 PDF 파일 경로')
    parser.add_argument('--output', default='output.xlsx', help='출력 Excel 파일 경로')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf):
        print(f"오류: 파일을 찾을 수 없습니다: {args.pdf}")
        return
    
    if not args.pdf.endswith('.pdf'):
        print("오류: PDF 파일만 지원합니다.")
        return
    
    print(f"PDF 파일 처리 중: {args.pdf}")
    extracted_text = extract_text_from_pdf(args.pdf)
    
    print("테스트 케이스 예시 로드 중...")
    examples = load_examples()
    
    print("테스트 케이스 생성 중...")
    test_cases = generate_test_cases(extracted_text, examples)
    
    print(f"Excel 파일 생성 중: {args.output}")
    excel_path = generate_excel(test_cases, output_path=args.output)
    
    print(f"완료! 생성된 파일: {excel_path}")

if __name__ == "__main__":
    main() 