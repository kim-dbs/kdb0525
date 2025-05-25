import streamlit as st
import sys
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 그래프 모듈 임포트
from graph import run_agent_system, create_new_session


# 페이지 설정
st.set_page_config(
    page_title="🌟 여행 AI 어시스턴트",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바
with st.sidebar:
    st.title("🌟 여행 AI 어시스턴트")
    st.markdown("---")
    st.markdown("### 🎯 기능")
    st.markdown("- 🗺️ 여행 계획 생성")
    st.markdown("- 🔍 관광지 정보 검색")
    st.markdown("- 🍽️ 맛집/카페 추천")
    st.markdown("- 🏨 호텔 검색 & 가격 비교")
    st.markdown("- 📅 캘린더 일정 관리")
    st.markdown("- 💬 대화형 상담")
    
    st.markdown("---")
    st.markdown("### 💡 사용법")
    st.markdown("1. 아래 채팅창에 여행 관련 질문을 입력하세요")
    st.markdown("2. AI가 답변을 생성합니다")
    st.markdown("3. 여행 계획을 캘린더에 등록할 수 있습니다")
    
    st.markdown("---")
    if st.button("🔄 새 대화 시작", use_container_width=True):
        # 세션 상태 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 메인 제목
st.title("🌟 여행 AI 어시스턴트")
st.markdown("여행 계획부터 맛집 추천, 캘린더 관리까지 모든 것을 도와드립니다!")

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread_id, st.session_state.config = create_new_session()
    
    # 환영 메시지
    welcome_message = """
    안녕하세요! 저는 **여행 AI 어시스턴트**입니다. 🌟
    
    다음과 같은 여행 관련 질문들을 도와드릴 수 있어요:
    
    🗺️ **여행 계획**: "제주도 2박 3일 여행 계획 짜줘"
    🔍 **관광지 정보**: "부산 가볼만한 곳 추천해줘"  
    🍽️ **맛집 정보**: "강릉 맛집 알려줘"
    ☕ **카페 정보**: "홍대 카페 추천해줘"
    📅 **일정 관리**: "이 계획을 캘린더에 등록해줘"
    
    어떤 여행을 계획하고 계신가요? 😊
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("여행 관련 질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤖 AI가 답변을 생성하고 있습니다..."):
            try:
                # 에이전트 시스템 실행
                response = run_agent_system(prompt, st.session_state.config)
                
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    error_msg = "죄송합니다. 응답을 생성하는 중에 문제가 발생했습니다. 다시 시도해주세요."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    🌟 여행 AI 어시스턴트 | Powered by LangGraph & Streamlit
    </div>
    """, 
    unsafe_allow_html=True
) 