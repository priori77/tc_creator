import openai
import os

def generate_test_cases(document_text, examples):
    # API 키 확인
    if not openai.api_key:
        print("경고: 유효한 OpenAI API 키가 설정되지 않았습니다.")
        return generate_test_data()
    
    try:
        # 시스템 프롬프트 생성
        system_prompt = "테스트 케이스 생성 전문가로서, 문서 텍스트에서 테스트 케이스를 추출하세요."
        
        # 타임아웃 설정 추가 (Vercel 10초 제한 고려)
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "o3-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"문서 텍스트:\n\n{document_text}"}
            ],
            max_completion_tokens=8000,
            reasoning_effort="medium",
            timeout=9  # 9초 타임아웃 설정
        )
        
        # 나머지 코드...
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return generate_test_data() 