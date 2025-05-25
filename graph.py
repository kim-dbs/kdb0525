import sys
import os
import uuid
from typing import Literal

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from app.agents.travel_agent import travel_agent_executor
from app.agents.calendar_agent import calendar_agent_executor
from app.agents.restaurant_agent import restaurant_agent_executor
from app.config.config import OPENAI_API_KEY, DEFAULT_MODEL

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#super visior 에이전트의 라우팅 기능
def router(state: MessagesState) -> Command:
    """사용자의 첫 질문을 받고, 어떤 전문 에이전트에게 보낼지 결정합니다."""
    router_llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0, api_key=OPENAI_API_KEY)
    
    messages = state["messages"]
    recent_context = ""
    
    # 최근 5개 메시지에서 컨텍스트 추출
    if len(messages) > 1:
        recent_messages = messages[-5:]
        context_parts = []
        for msg in recent_messages:
            if hasattr(msg, 'content') and msg.content:
                content = msg.content
                context_parts.append(f"- {type(msg).__name__}: {content}")
        recent_context = "\n".join(context_parts)
    
    current_message = messages[-1].content if messages else ""
    
    @tool
    def route(destination: Literal["travel_agent", "calendar_agent", "restaurant_agent", "end"]):
        """
        사용자의 질문과 이전 대화 내역을 고려하여 가장 적합한 전문가에게 라우팅합니다.
        
        라우팅 규칙:
        - 여행 계획, 관광지 정보 등은 'travel_agent'
        - 맛집, 카페, 음식점 추천 등은 'restaurant_agent'
        - 캘린더 일정 생성, 조회, 수정, 삭제 등은 'calendar_agent'
        - 간단한 인사나 여행과 관련없는 질문은 'end'
        """
        return destination

    try:
        # 컨텍스트를 포함한 프롬프트 생성
        routing_prompt = f"""
        현재 사용자 메시지: "{current_message}"

        최근 대화 내역:
        {recent_context}

        위 대화 내역을 고려하여 라우팅을 결정하세요.
        """

        decision = router_llm.bind_tools([route]).invoke([HumanMessage(content=routing_prompt)])
        
        if not decision.tool_calls:
            return Command(goto="end_handler")
        
        # 안전한 destination 접근
        tool_call = decision.tool_calls[0]
        args = tool_call.get('args', {})
        destination = args.get('destination', 'end')
        
        if destination == "end":
            return Command(goto="end_handler")
        
        return Command(goto=destination)
        
    except Exception as e:
        return Command(goto="end_handler")

#end handler
#여행과 관련없는 질문에 대하여 가드레일 에이전트가 발동하여 안내 메시지를 반환합니다.
def end_handler(state: MessagesState):
    """여행과 관련없는 질문에 대한 안내 메시지를 반환합니다."""
    
    guide_message = """안녕하세요! 😊 

저는 **여행 AI 어시스턴트**입니다. 가드레일이 발동하였습니다. 
다음과 같은 여행 관련 질문들을 도와드릴 수 있어요:

🗺️ **여행 계획**: "제주도 2박 3일 여행 계획 짜줘"
🔍 **관광지 정보**: "부산 가볼만한 곳 추천해줘"  
🍽️ **맛집 정보**: "강릉 맛집 알려줘"
☕ **카페 정보**: "홍대 카페 추천해줘"
📅 **일정 관리**: "이 계획을 캘린더에 등록해줘"

어떤 여행을 계획하고 계신가요? 🌟"""
    
    return {"messages": [AIMessage(content=guide_message)]}

#그래프 생성
def create_agent_graph():
    """에이전트 그래프를 생성하고 반환합니다."""
    graph_builder = StateGraph(MessagesState)

    graph_builder.add_node("travel_agent", travel_agent_executor)
    graph_builder.add_node("calendar_agent", calendar_agent_executor)
    graph_builder.add_node("restaurant_agent", restaurant_agent_executor)
    graph_builder.add_node("router", router)
    graph_builder.add_node("end_handler", end_handler)

    # start router
    graph_builder.add_edge(START, "router")

    # checkpointer를 생성하고 그래프 컴파일 시 추가
    checkpointer = InMemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)

#에이전트 시스템 실행
def run_agent_system(query: str, config: dict):
    """에이전트 시스템을 실행합니다."""
    app = create_agent_graph()
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    events = app.stream(initial_state, config=config, stream_mode="values")
    
    final_answer = ""
    event_count = 0
    
    try:
        for event in events:
            event_count += 1
            
            if event['messages'] and hasattr(event['messages'][-1], 'content'):
                last_message = event['messages'][-1]
                
                # 도구 호출이 없는 AI 메시지만 최종 답변으로 사용
                if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
                    final_answer = last_message.content
        
    except Exception as e:
        return f"정보를 검색하는 데 문제가 발생했습니다. 오류: {str(e)}"

    return final_answer if final_answer else "응답을 생성할 수 없습니다."

def create_new_session():
    """새로운 대화 세션을 생성합니다."""
    thread_id = str(uuid.uuid4()) # 대화 세션 고유 ID 생성
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 25}
    return thread_id, config 