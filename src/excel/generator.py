import pandas as pd
import os
from datetime import datetime

def generate_excel(test_cases, output_path=None):
    """
    테스트 케이스 목록을 Excel 파일로 변환합니다.
    
    Args:
        test_cases (list): 테스트 케이스 목록
        output_path (str, optional): 출력 파일 경로. 기본값은 None.
        
    Returns:
        str: 생성된 Excel 파일 경로
    """
    # 출력 디렉토리 생성
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # 출력 파일 경로 설정
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(output_dir, f'test_cases_{timestamp}.xlsx')
    
    # DataFrame 생성
    df = pd.DataFrame(test_cases)
    
    # 열 순서 정의
    columns = [
        'TID', '대분류', '중분류', '소분류', 
        'Precondition', 'Test_Step', 'Expected_Result',
        'Result', 'BTS_Key', 'Comment'
    ]
    
    # 열이 존재하는지 확인하고 순서 조정
    existing_columns = [col for col in columns if col in df.columns]
    df = df[existing_columns]
    
    # Excel 파일 생성
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Test Cases', index=False)
    
    # 워크시트 및 워크북 객체 가져오기
    workbook = writer.book
    worksheet = writer.sheets['Test Cases']
    
    # 열 너비 설정
    for i, col in enumerate(df.columns):
        max_len = max(
            df[col].astype(str).map(len).max(),
            len(col)
        ) + 2
        worksheet.set_column(i, i, max_len)
    
    # 헤더 형식 설정
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # 헤더 행에 형식 적용
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # 파일 저장
    writer.close()
    
    return output_path 