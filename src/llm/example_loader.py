import json
import os

def load_examples():
    """
    테스트 케이스 예시 데이터를 로드합니다.
    
    Returns:
        list: 테스트 케이스 예시 목록
    """
    try:
        # 다양한 가능한 경로 시도
        possible_paths = [
            os.path.join('data', 'examples', 'test_cases.json'),  # 원래 경로
            'tc_cases.json',  # 루트 경로
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tc_cases.json')  # 절대 경로 계산
        ]
        
        # 존재하는 첫 번째 파일 사용
        example_path = None
        for path in possible_paths:
            if os.path.exists(path):
                example_path = path
                print(f"테스트 케이스 예시 파일을 찾았습니다: {path}")
                break
        
        if example_path is None:
            print("경고: 테스트 케이스 예시 파일을 찾을 수 없습니다. 기본 예시를 사용합니다.")
            raise FileNotFoundError("테스트 케이스 예시 파일을 찾을 수 없습니다")
        
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
            "TID": "GEM_001",
            "대분류": "재화",
            "중분류": "다이아",
            "소분류": "아이콘",
            "Precondition": "게임 로비 화면 상태",
            "Test_Step": "다이아 아이콘 터치",
            "Expected_Result": "다이아 상세 정보 팝업창이 출력 됨",
            "Result": "Not Test",
            "BTS_Key": "",
            "Comment": ""
            }
        ]