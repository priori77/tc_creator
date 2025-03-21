import os
import json
import openai
from dotenv import load_dotenv
from src.utils.config import Config  # Config 클래스 임포트
import random

# .env 파일에서 환경 변수 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_cases(document_text, examples):
    """
    문서 텍스트에서 테스트 케이스를 생성합니다.
    
    Args:
        document_text (str): 분석할 문서 텍스트
        examples (list): 예시 테스트 케이스
        
    Returns:
        list: 생성된 테스트 케이스 목록
    """
    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY") 
    if not api_key:
        print("경고: 유효한 OpenAI API 키가 설정되지 않았습니다.")
        return generate_test_data()
    
    try:
        # OpenAI 클라이언트 초기화
        client = openai.OpenAI(api_key=api_key)
        
        # 시스템 프롬프트 생성
        system_prompt = "테스트 케이스 생성 전문가로서, 문서 텍스트에서 테스트 케이스를 추출하세요."
        
        # 예시 데이터를 JSON 문자열로 변환
        examples_json = json.dumps(examples, ensure_ascii=False, indent=2)
        
        # 타임아웃 설정 추가 (Vercel 10초 제한 고려)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "o3-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 형식의 테스트 케이스 예시를 참고하세요:\n\n{examples_json}\n\n이 형식에 맞게 다음 문서에서 테스트 케이스를 생성해주세요:\n\n{document_text[:4000]}"}
            ],
            response_format={"type": "json_object"},
            timeout=9  # 9초 타임아웃 설정
        )
        
        # 응답에서 테스트 케이스 추출
        try:
            response_content = response.choices[0].message.content
            result = json.loads(response_content)
            
            # 응답 구조 확인하고 테스트 케이스 배열 추출
            if "test_cases" in result:
                return result["test_cases"]
            else:
                # 응답에 test_cases 키가 없는 경우 응답 전체를 확인
                for key, value in result.items():
                    if isinstance(value, list) and len(value) > 0:
                        return value
                
                # 적절한 배열을 찾지 못한 경우 테스트 데이터 반환
                return generate_test_data()
            
        except Exception as e:
            print(f"응답 데이터 처리 오류: {e}")
            return generate_test_data()
        
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return generate_test_data()

def generate_test_data():
    """샘플 테스트 케이스 데이터를 생성합니다."""
    # 기본 테스트 데이터 (API 호출 실패 시 사용)
    return [
        {
            "TID": f"TC{str(i+1).zfill(3)}",
            "대분류": random.choice(["로그인", "회원가입", "게임플레이", "상점", "인벤토리"]),
            "중분류": random.choice(["기본기능", "예외처리", "경계값", "성능"]),
            "소분류": f"테스트 케이스 {i+1}",
            "Precondition": "시스템 접속 상태",
            "Test_Step": f"1. 테스트 스텝 1\n2. 테스트 스텝 2\n3. 테스트 스텝 3",
            "Expected_Result": f"1. 예상 결과 1\n2. 예상 결과 2"
        } for i in range(10)
    ] 