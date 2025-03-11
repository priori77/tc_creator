import os
import json
import openai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_cases(document_text, examples):
    """
    OpenAI API를 사용하여 문서 텍스트에서 테스트 케이스를 생성합니다.
    
    Args:
        document_text (str): 기획서에서 추출한 텍스트
        examples (list): 테스트 케이스 예시 목록
        
    Returns:
        list: 생성된 테스트 케이스 목록
    """
    # 프롬프트 구성
    prompt = f"""
    당신은 게임 QA 테스트 케이스 작성 전문가입니다. 
    주어진 게임 기획서를 분석하여 테스트 케이스를 생성해주세요.
    
    다음은 테스트 케이스 예시입니다:
    {json.dumps(examples, ensure_ascii=False, indent=2)}
    
    위 예시와 같은 형식으로, 아래 기획서 내용에 대한 테스트 케이스를 생성해주세요.
    각 테스트 케이스는 다음 필드를 포함해야 합니다:
    - TID: 테스트 ID (예: ITEM_001, CHAR_001 등)
    - 대분류: 테스트 대분류 (예: NPC, 캐릭터, 아이템 등)
    - 중분류: 테스트 중분류
    - 소분류: 테스트 소분류
    - Precondition: 테스트 전제 조건
    - Test_Step: 테스트 단계
    - Expected_Result: 기대 결과
    - Result: 초기값은 빈 문자열
    - BTS_Key: 초기값은 빈 문자열
    - Comment: 초기값은 빈 문자열
    
    기획서 내용:
    {document_text}
    
    JSON 형식으로 테스트 케이스 목록만 반환해주세요.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 게임 QA 테스트 케이스 작성 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        # 응답에서 JSON 부분 추출
        response_text = response.choices[0].message.content.strip()
        
        # JSON 문자열 찾기
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            test_cases = json.loads(json_str)
            
            # 응답 형식 확인 및 조정
            if isinstance(test_cases, dict) and "tc_examples" in test_cases:
                return test_cases["tc_examples"]
            elif isinstance(test_cases, list):
                return test_cases
            else:
                return [test_cases]
        else:
            raise ValueError("API 응답에서 JSON 형식을 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {str(e)}")
        raise 