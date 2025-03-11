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
    OpenAI의 o3-mini (reasoning model)을 사용하여 문서 텍스트에서 테스트 케이스를 생성합니다.
    
    Args:
        document_text (str): 기획서에서 추출한 텍스트
        examples (list): 테스트 케이스 예시 목록
        
    Returns:
        list: 생성된 테스트 케이스 목록
    """
    # (1) 시스템 프롬프트를 더욱 강화하여, 테스트 케이스를 풍부하게 생성하도록 지시
    #     - 다양한 범주의 테스트(기본 시나리오, 예외 케이스, 경계값, 상태 전이 등)를 반드시 포함
    #     - 예시 구조를 참고하여 JSON 형식으로만 반환하도록 강력하게 요구
    system_prompt = (
        "당신은 게임 10년 이상의 경력을 가진 게임 QA 시니어입니다.\n"
        "아래에 주어진 게임 기획서 내용을 꼼꼼히 분석하여, 가능한 한 풍부한 테스트 케이스를 생성해 주세요.\n"
        "테스트 케이스 작성 시 다음 사항을 반드시 포함해야 합니다:\n"
        "  1) 정상 시나리오(정상적인 흐름)\n"
        "  2) 예외/에러 상황(비정상 흐름)\n"
        "  3) 경계값/엣지 케이스\n"
        "  4) 상태 전이(특정 상태에서 다른 상태로 넘어가는 흐름, 유효 전이/무효 전이 모두 고려)\n"
        "  5) 기능별 제약사항 및 제한사항 검증\n\n"
        "테스트 케이스를 최대한 상세하게, 그리고 많은 개수를 생성해 주십시오.\n"
        "형식은 JSON 배열(list)로만 작성하고, 예시는 아래와 같은 필드를 가져야 합니다:\n"
        "  - TID: 테스트 ID (예: ITEM_001, CHAR_001 등 식별이 용이하도록)\n"
        "  - 대분류: 테스트 대분류 (NPC, 캐릭터, 아이템 등)\n"
        "  - 중분류: 테스트 중분류\n"
        "  - 소분류: 테스트 소분류\n"
        "  - Precondition: 사전 조건(캐릭터 레벨, 게임 환경 등)\n"
        "  - Test_Step: 테스트 실행 단계 혹은 절차\n"
        "  - Expected_Result: 기대 결과\n"
        "  - Result: (빈 문자열로)\n"
        "  - BTS_Key: (빈 문자열로)\n"
        "  - Comment: (빈 문자열로)\n\n"
        "절대 JSON 형식 외의 불필요한 문구나 해설을 포함하지 말고,\n"
        "정확한 JSON 배열로만 결과를 응답하세요."
    )

    # (2) 유저 프롬프트(실제 기획서 및 예시 정보 전달)
    user_prompt = f"""
다음은 테스트 케이스 예시입니다:
{json.dumps(examples, ensure_ascii=False, indent=2)}

아래 기획서 내용에 대해 위 예시와 같은 구조로, 가능한 한 많은 테스트 케이스를 생성해주세요.

기획서 내용:
{document_text}
"""

    try:
        # (3) ChatCompletion API를 호출하되, o3-mini (reasoning model) 사용 및
        #     reasoning_effort 파라미터를 medium 혹은 high로 설정.
        #     max_completion_tokens를 크게 잡아 테스트케이스가 잘리지 않도록 함.
        response = openai.chat.completions.create(
            model=Config.OPENAI_MODEL,         # o3-mini (reasoning model)이라고 가정
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=8000,  # 충분한 응답 길이를 확보
            reasoning_effort="medium"    # 생성 깊이: "low", "medium", "high" 중 선택
        )
        
        # (4) 응답 텍스트 추출
        response_text = response.choices[0].message.content.strip()
        
        # (5) JSON 파싱 시도
        try:
            test_cases = json.loads(response_text)
        except json.JSONDecodeError:
            # JSON 형식 추출 실패 시 예외 처리
            import re
            json_pattern = r'(\[[\s\S]*\])'  # 배열 형태의 JSON 추출
            json_matches = re.findall(json_pattern, response_text)

            if json_matches:
                try:
                    test_cases = json.loads(json_matches[0])
                except json.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                    print(f"추출된 JSON 문자열: {json_matches[0]}")
                    raise ValueError("추출된 JSON을 파싱할 수 없습니다.")
            else:
                print(f"원본 응답: {response_text}")
                raise ValueError("응답에서 JSON 배열 형식을 찾을 수 없습니다.")
        
        # (6) 테스트 케이스가 리스트 형태인지 확인 후 반환
        if isinstance(test_cases, list):
            return test_cases
        else:
            # 만약 단일 객체 혹은 다른 형태라면 리스트로 감싸서 반환
            return [test_cases]

    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {str(e)}")
        raise

# ------------------------------------------------------------
# 아래는 테스트 실행 예시 코드입니다. (메인에서 테스트 시)
if __name__ == "__main__":
    # (A) 예시 기획서와 예제 테스트 케이스
    document = "여기에 예시 게임 기획서 내용이 들어갑니다."
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
        # (B) 테스트 케이스 생성 함수 호출
        test_cases = generate_test_cases(document, examples)
        print(json.dumps(test_cases, ensure_ascii=False, indent=2))
    except Exception as error:
        print(f"테스트 케이스 생성 중 오류 발생: {error}")
