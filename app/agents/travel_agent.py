from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.config.config import DEFAULT_MODEL, OPENAI_API_KEY

from app.tools.search import search_agent
from app.tools.planner import planner_agent
from app.tools.handoff import create_handoff_tool

# tool + agent  ReAct 에이전트
tools = [
    search_agent,
    planner_agent,
    create_handoff_tool(
        agent_name="calendar_agent",
        description="캘린더에 일정을 추가, 수정, 삭제 또는 검색해야 할 때 사용합니다. 예를 들어 '이 계획을 캘린더에 등록해줘' 같은 요청이 있을 때 호출합니다."
    ),
    create_handoff_tool(
        agent_name="restaurant_agent",
        description="맛집, 카페, 음식점 추천이 필요할 때 사용합니다. 예를 들어 '부산 맛집 추천해줘', '강남 카페 알려줘' 같은 요청이 있을 때 호출합니다."
    ),
    create_handoff_tool(
        agent_name="hotel_agent",
        description="호텔, 숙박, 펜션, 리조트 검색 및 가격 비교가 필요할 때 사용합니다. 예를 들어 '서울 호텔 가격 비교해줘', '제주도 펜션 추천해줘' 같은 요청이 있을 때 호출합니다."
    ),
]


llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0, api_key=OPENAI_API_KEY)


travel_agent_executor = create_react_agent(llm, tools) 