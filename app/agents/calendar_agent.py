from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.config.config import DEFAULT_MODEL, OPENAI_API_KEY

from app.tools.calendar import calendar_tools
from app.tools.handoff import create_handoff_tool


tools = calendar_tools + [
    create_handoff_tool(
        agent_name="travel_agent",
        description="새로운 여행 계획을 짜거나, 관광지 정보를 찾아야 할 때 사용합니다."
    ),
    create_handoff_tool(
        agent_name="restaurant_agent",
        description="맛집, 카페, 음식점 추천이 필요할 때 사용합니다."
    ),
    create_handoff_tool(
        agent_name="hotel_agent",
        description="호텔, 숙박, 펜션, 리조트 검색 및 가격 비교가 필요할 때 사용합니다."
    ),
]


llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0, api_key=OPENAI_API_KEY)


calendar_agent_executor = create_react_agent(llm, tools) 