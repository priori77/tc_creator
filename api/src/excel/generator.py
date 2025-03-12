import os
from datetime import datetime

def generate_excel(test_cases):
    """테스트 케이스 데이터를 Excel 파일로 생성합니다."""
    
    # 서버리스 환경용 출력 폴더 설정
    output_dir = '/tmp/output'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_path = os.path.join(output_dir, f"test_cases_{timestamp}.xlsx")
    
    # Excel 파일 생성 로직...
    
    return excel_path 