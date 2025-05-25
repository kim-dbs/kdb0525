from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from app.config.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, OPENAI_API_KEY

@tool
def restaurant_search(location: str, food_type: str = "", budget: str = "") -> str:
    """특정 지역의 맛집과 카페를 검색합니다."""
    
    # 맛집 검색에 특화된 프롬프트
    prompt = f"""
    {location}의 맛집과 카페를 추천해주세요.
    
    검색 조건:
    - 위치: {location}
    - 음식 종류: {food_type if food_type else "전체"}
    - 예산: {budget if budget else "상관없음"}
    
    다음 형식으로 추천해주세요:
    
    ## 🍽️ 추천 맛집
    
    ### 1. [맛집명]
    - 📍 주소: 
    - 🍴 대표메뉴: 
    - 💰 가격대: 
    - ⭐ 특징: 
    - 📞 연락처: 
    
    ### 2. [맛집명]
    ...
    
    ## ☕ 추천 카페
    
    ### 1. [카페명]
    - 📍 주소:
    - ☕ 대표메뉴:
    - 💰 가격대:
    - ⭐ 특징:
    
    ## 💡 맛집 탐방 팁
    - 운영시간 확인 필수
    - 예약 가능 여부
    - 주차 정보
    """
    
    model = ChatOpenAI(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        api_key=OPENAI_API_KEY
    )
    
    response = model.invoke(prompt)
    return response.content

@tool  
def restaurant_recommendation(user_request: str) -> str:
    """사용자의 맛집/카페 요청을 분석하여 맞춤 추천을 제공합니다."""
    
    prompt = f"""
    사용자의 맛집/카페 요청을 분석하여 맞춤 추천을 제공해주세요.
    
    사용자 요청: {user_request}
    
    다음 사항을 고려하여 추천해주세요:
    - 위치 정보 추출
    - 선호하는 음식 종류
    - 예산 범위
    - 분위기나 특별한 요구사항
    
    추천 형식:
    
    ## 🎯 맞춤 추천
    
    ### 추천 이유
    - 요청 분석 결과를 바탕으로 설명
    
    ### 🍽️ 추천 맛집/카페
    
    **1. [업소명]**
    - 📍 위치: 
    - 🍴 추천메뉴: 
    - 💰 예상비용: 
    - ⭐ 추천이유: 
    - 🕐 운영시간: 
    
    **2. [업소명]**
    ...
    
    ## 📝 방문 가이드
    - 예약 필요 여부
    - 교통편 안내
    - 주의사항
    """
    
    model = ChatOpenAI(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        api_key=OPENAI_API_KEY
    )
    
    response = model.invoke(prompt)
    return response.content 