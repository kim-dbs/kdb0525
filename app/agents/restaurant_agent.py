from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.config.config import DEFAULT_MODEL, OPENAI_API_KEY

from app.tools.restaurant import restaurant_search, restaurant_recommendation
from app.tools.handoff import create_handoff_tool

# 맛집/카페 전용 도구들
tools = [
    restaurant_search,
    restaurant_recommendation,
    create_handoff_tool(
        agent_name="travel_agent",
        description="여행 계획이나 관광지 정보가 필요할 때 사용합니다. 예를 들어 '제주도 여행 계획 짜줘' 같은 요청이 있을 때 호출합니다."
    ),
    create_handoff_tool(
        agent_name="calendar_agent", 
        description="캘린더에 일정을 추가, 수정, 삭제 또는 검색해야 할 때 사용합니다. 예를 들어 '이 맛집을 캘린더에 등록해줘' 같은 요청이 있을 때 호출합니다."
    ),
    create_handoff_tool(
        agent_name="hotel_agent",
        description="호텔, 숙박, 펜션, 리조트 검색 및 가격 비교가 필요할 때 사용합니다. 예를 들어 '이 지역 호텔도 알아봐줘' 같은 요청이 있을 때 호출합니다."
    ),
]

# 맛집/카페 전문 LLM 설정
llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0, api_key=OPENAI_API_KEY)

# 맛집/카페 에이전트 생성
restaurant_agent_executor = create_react_agent(llm, tools) 