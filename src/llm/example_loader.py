import json
import os

def load_examples():
    """
    테스트 케이스 예시 데이터를 로드합니다.
    
    Returns:
        list: 테스트 케이스 예시 목록
    """
    try:
        # 프로젝트 루트 디렉토리 기준 상대 경로
        example_path = os.path.join('data', 'examples', 'test_cases.json')
        
        # 파일이 없으면 tc_cases.json 사용
        if not os.path.exists(example_path):
            example_path = 'tc_cases.json'
        
        with open(example_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 데이터 형식 확인
        if isinstance(data, dict) and "tc_examples" in data:
            return data["tc_examples"]
        else:
            return data
            
    except Exception as e:
        print(f"예시 데이터 로드 중 오류 발생: {str(e)}")
        # 기본 예시 반환
        return [
            {
                "TID": "ITEM_001",
                "대분류": "NPC\n(공통)",
                "중분류": "리스트",
                "소분류": "M0.2 스펙",
                "Precondition": "1. 라운지에 진입한 상태",
                "Test_Step": "1. 인게임 내 NPC 스폰 확인",
                "Expected_Result": "라운지 내 무기 상인 NPC가 존재한다.",
                "Result": "",
                "BTS_Key": "",
                "Comment": ""
            }
        ] 