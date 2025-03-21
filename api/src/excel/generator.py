import pandas as pd
import os
from datetime import datetime

def generate_excel(test_cases, output_path=None):
    """
    테스트 케이스 목록을 Excel 파일로 변환합니다.
    
    Args:
        test_cases (list): 테스트 케이스 목록
        output_path (str, optional): 출력 파일 경로
        
    Returns:
        str: 생성된 Excel 파일 경로
    """
    try:
        # 서버리스 환경용 출력 폴더 설정
        output_dir = '/tmp/output'
        os.makedirs(output_dir, exist_ok=True)
        
        # 파일명 생성 (기본값: 현재 날짜/시간)
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"test_cases_{timestamp}.xlsx")
        
        # 데이터프레임 생성
        df = pd.DataFrame(test_cases)
        
        # Excel 파일 생성
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Test Cases', index=False)
        
        # 열 너비 조정
        worksheet = writer.sheets['Test Cases']
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)
        
        # 파일 저장
        writer.close()
        
        return output_path
    except Exception as e:
        print(f"Excel 파일 생성 중 오류 발생: {e}")
        raise 