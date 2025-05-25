from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from app.config.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, OPENAI_API_KEY

#planner tools
@tool
def planner_agent(user_prompt: str, search_results: str) -> str:
    """검색된 정보를 바탕으로 여행 계획을 생성합니다."""
    
    prompt = f"""
    검색 결과와 사용자 요청을 바탕으로 상세한 여행 계획을 작성해주세요.

    검색 결과: {search_results}
    사용자 요청: {user_prompt}

    여행 계획을 시간순으로 정리하여 작성해주세요.
    """
    
    model = ChatOpenAI(
        model=DEFAULT_MODEL, 
        temperature=DEFAULT_TEMPERATURE,
        api_key=OPENAI_API_KEY
    )
    
    response = model.invoke(prompt)
    return response.content 