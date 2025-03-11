import os
import json
import openai
from dotenv import load_dotenv
from src.utils.config import Config  # Config 클래스 임포트

# .env 파일에서 환경 변수 로드 및 API 키 설정
load_dotenv()
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
    당신은 게임 10년 이상의 경력을 가진 게임 QA 시니어입니다. 
    주어진 게임 기획서를 분석하여 기능/시나리오/예외/제약사항/상태 전이 등을 고려하여 테스트 케이스를 생성해주세요.
    
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
        # 최신 OpenAI SDK 방식: openai.chat.completions.create() 호출
        response = openai.chat.completions.create(
            model=Config.OPENAI_MODEL,  # .env에서 "o3-mini"로 설정되어 있다고 가정
            messages=[
                {"role": "system", "content": "당신은 게임 QA 테스트 케이스 작성 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=8000,  # 응답 최대 토큰 수 제어 (max_tokens 대신 사용)
            reasoning_effort="medium"         # 생성 깊이 조절: "low", "medium", "high" 중 선택
        )
        
        # 응답 처리: 최신 버전에서는 message가 객체이므로 .content로 접근
        response_text = response.choices[0].message.content.strip()
        
        try:
            # 전체 응답을 JSON으로 파싱 시도
            test_cases = json.loads(response_text)
        except json.JSONDecodeError:
            # 실패하면 JSON 부분만 추출 시도
            import re
            json_pattern = r'(\{[\s\S]*\})'
            json_matches = re.findall(json_pattern, response_text)
            
            if json_matches:
                try:
                    test_cases = json.loads(json_matches[0])
                except json.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                    print(f"추출된 JSON 문자열: {json_matches[0]}")
                    # 디버깅을 위해 응답 전체를 로깅
                    print(f"원본 응답: {response_text}")
                    raise ValueError(f"추출된 JSON을 파싱할 수 없습니다: {e}")
            else:
                # 디버깅을 위해 응답 전체를 로깅
                print(f"원본 응답: {response_text}")
                raise ValueError("응답에서 JSON 형식을 찾을 수 없습니다")
        
        # 응답 형식 확인 및 조정
        if isinstance(test_cases, dict) and "tc_examples" in test_cases:
            return test_cases["tc_examples"]
        elif isinstance(test_cases, list):
            return test_cases
        else:
            return [test_cases]
            
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {str(e)}")
        raise

# 예제 실행 (필요에 따라 아래 코드로 테스트)
if __name__ == "__main__":
    # 예시 문서와 테스트 케이스 예시
    document = "여기에 게임 기획서 내용이 들어갑니다."
    examples = [
        {
            "TID": "ITEM_001",
            "대분류": "아이템",
            "중분류": "무기",
            "소분류": "근접무기",
            "Precondition": "플레이어가 무기를 소지하고 있다.",
            "Test_Step": "무기를 사용하여 공격한다.",
            "Expected_Result": "공격 성공 및 적에게 피해가 전달된다.",
            "Result": "",
            "BTS_Key": "",
            "Comment": ""
        }
    ]
    
    try:
        test_cases = generate_test_cases(document, examples)
        print(json.dumps(test_cases, ensure_ascii=False, indent=2))
    except Exception as error:
        print(f"테스트 케이스 생성 중 오류 발생: {error}")
