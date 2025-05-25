# kdb0525
kdb9525
# 🌟 여행 AI 어시스턴트

LangGraph 기반의 멀티 에이전트 여행 도우미 시스템

## 📊 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    🌟 여행 AI 어시스턴트                      │
│                     (Streamlit UI)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  🚦 Router Agent                           │
│              (Supervisor/라우팅 에이전트)                    │
│                                                             │
│  • 사용자 질문 분석                                          │
│  • 컨텍스트 인식 (최근 5개 메시지)                           │
│  • 적절한 전문 에이전트로 라우팅                             │
│  • 가드레일 기능 (여행 외 질문 차단)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│🗺️ Travel    │ │🍽️ Restaurant│ │📅 Calendar  │
│   Agent     │ │   Agent     │ │   Agent     │
└─────────────┘ └─────────────┘ └─────────────┘
```

## 🎯 에이전트별 상세 구조

### 1. 🚦 Router Agent (라우터/슈퍼바이저)
- **위치**: `graph.py`
- **역할**: 중앙 라우팅 및 가드레일
- **기능**:
  - 사용자 질문 분석
  - 컨텍스트 인식 (최근 5개 메시지)
  - 적절한 전문 에이전트 선택
  - 여행 외 질문 차단 (가드레일)
  - End Handler로 안내 메시지 제공

**라우팅 규칙**:
- `travel_agent` ← 여행 계획, 관광지 정보
- `restaurant_agent` ← 맛집, 카페, 음식점 추천
- `calendar_agent` ← 일정 생성/조회/수정/삭제
- `end` ← 여행 무관 질문 (가드레일 발동)

### 2. 🗺️ Travel Agent (여행 전문 에이전트)
- **위치**: `app/agents/travel_agent.py`
- **역할**: 여행 계획 및 관광지 정보 제공
- **도구들**:
  - `search_agent` (웹 검색)
  - `planner_agent` (여행 계획 생성)
  - 핸드오프 도구들:
    - → `calendar_agent` (일정 등록)
    - → `restaurant_agent` (맛집 추천)

**핸드오프 시나리오**:
- "이 계획을 캘린더에 등록해줘" → calendar_agent
- "부산 맛집도 추천해줘" → restaurant_agent

### 3. 🍽️ Restaurant Agent (맛집 전문 에이전트)
- **위치**: `app/agents/restaurant_agent.py`
- **역할**: 맛집, 카페, 음식점 추천
- **도구들**:
  - `restaurant_search` (지역별 맛집 검색)
  - `restaurant_recommendation` (맞춤 추천)
  - 핸드오프 도구들:
    - → `travel_agent` (여행 계획)
    - → `calendar_agent` (일정 등록)

**핸드오프 시나리오**:
- "제주도 여행 계획도 짜줘" → travel_agent
- "이 맛집을 캘린더에 등록해줘" → calendar_agent

### 4. 📅 Calendar Agent (캘린더 전문 에이전트)
- **위치**: `app/agents/calendar_agent.py`
- **역할**: 일정 관리 (생성/조회/수정/삭제)
- **도구들**:
  - `calendar_tools` (Google Calendar 연동)
  - 핸드오프 도구들:
    - → `travel_agent` (여행 계획)
    - → `restaurant_agent` (맛집 추천)

**핸드오프 시나리오**:
- "새로운 여행 계획 짜줘" → travel_agent
- "맛집도 추천해줘" → restaurant_agent

### 5. 🔚 End Handler (가드레일 에이전트)
- **위치**: `graph.py`
- **역할**: 여행 무관 질문 처리
- **기능**:
  - 가드레일 발동 안내
  - 사용 가능한 기능 안내
  - 여행 관련 질문 유도

## 🛠️ 도구(Tools) 구조

```
📁 app/tools/
├── search.py ← 웹 검색 (Google Search API)
├── planner.py ← 여행 계획 생성
├── restaurant.py ← 맛집 검색 & 추천
├── calendar.py ← Google Calendar 연동
└── handoff.py ← 에이전트 간 핸드오프
```

### 🔄 핸드오프 시스템
각 에이전트는 다른 에이전트로 작업을 넘길 수 있습니다:

```
Travel Agent ←→ Restaurant Agent ←→ Calendar Agent
```

## 📊 데이터 흐름

```
1. 사용자 입력 (Streamlit)
   ↓
2. Router Agent (질문 분석 & 라우팅)
   ↓
3. 전문 에이전트 (Travel/Restaurant/Calendar)
   ↓
4. 도구 실행 (검색/계획/추천/일정관리)
   ↓
5. 필요시 다른 에이전트로 핸드오프
   ↓
6. 최종 응답 반환 (Streamlit)
```

## 🎯 주요 기능

### ✅ 활성화된 기능
- 🗺️ 여행 계획 생성
- 🔍 관광지 정보 검색
- 🍽️ 맛집/카페 추천
- 📅 캘린더 일정 관리
- 🔄 에이전트 간 핸드오프
- 🚦 컨텍스트 인식 라우팅
- 🛡️ 가드레일 시스템

### 💬 사용 예시
- "제주도 2박 3일 여행 계획 짜줘"
- "부산 가볼만한 곳 추천해줘"
- "강릉 맛집 알려줘"
- "홍대 카페 추천해줘"
- "이 계획을 캘린더에 등록해줘"

## 🔧 기술 스택

- **프레임워크**: LangGraph (에이전트 오케스트레이션)
- **LLM**: OpenAI GPT (ChatOpenAI)
- **UI**: Streamlit
- **에이전트 패턴**: ReAct (Reasoning + Acting)
- **메모리**: InMemorySaver (대화 세션 관리)
- **외부 API**: Google Search API, Google Calendar API

## 🚀 설치 및 실행

### 1. 환경 설정


# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

### 3. 실행
```bash
streamlit run main.py
```

## 📁 프로젝트 구조

```
kakaobank/
├── main.py                 # Streamlit 메인 앱
├── graph.py               # 에이전트 그래프 및 라우터
├── requirements.txt       # 의존성 목록
├── .env                  # 환경 변수
├── readme.md             # 프로젝트 문서
└── app/
    ├── __init__.py
    ├── agents/           # 에이전트들
    │   ├── __init__.py
    │   ├── travel_agent.py
    │   ├── restaurant_agent.py
    │   └── calendar_agent.py
    ├── tools/            # 도구들
    │   ├── __init__.py
    │   ├── search.py
    │   ├── planner.py
    │   ├── restaurant.py
    │   ├── calendar.py
    │   └── handoff.py
    ├── config/           # 설정
    │   ├── __init__.py
    │   └── config.py
    └── models/           # 데이터 모델
        ├── __init__.py
        ├── state.py
        └── hotel_parser.py
```

## 🔄 확장성

이 시스템은 모듈화되어 있어 새로운 에이전트나 도구를 쉽게 추가할 수 있습니다:

1. **새 에이전트 추가**: `app/agents/` 폴더에 새 에이전트 파일 생성
2. **새 도구 추가**: `app/tools/` 폴더에 새 도구 파일 생성
3. **라우터 업데이트**: `graph.py`에서 라우팅 규칙 추가
4. **핸드오프 설정**: 기존 에이전트에 새 에이전트로의 핸드오프 도구 추가


## 📸 테스트 사진
1. **가드레일 테스트**
- 여행 AI 어시스턴트에 상관 없는 질문, 단순한 쿼리에는 가드레일이 작동을 합니다.
<img width="800" alt="스크린샷 2025-05-25 오후 4 50 10" src="https://github.com/user-attachments/assets/26a84f57-b8c0-4ec3-9d1b-398a32d3f02b" />

2. **여행 계획 및 검색 에이전트 테스트**

<img width="800" alt="스크린샷 2025-05-25 오후 4 53 29" src="https://github.com/user-attachments/assets/51161b3c-cd5c-4451-bdba-7af9b0ba8788" />
<img width="800" alt="스크린샷 2025-05-25 오후 4 53 42" src="https://github.com/user-attachments/assets/5ff6d384-a395-4176-8fd7-b468673de5c5" />

3. **맛집,카페 추천 에이전트 테스트**

- 맛집 추천 받은 후 컨텍스트 기반으로 계획 짜주는 테스트
![스크린샷 2025-05-25 오후 5 12 19](https://github.com/user-attachments/assets/97dc6881-e34d-4acb-8a08-50ccd4ec8570)
![스크린샷 2025-05-25 오후 5 12 51](https://github.com/user-attachments/assets/588cb8c6-b92a-40e4-ba05-5577221976d9)

4. **캘린더 에이전트 테스트**
- 캘린더 등록

![스크린샷 2025-05-25 오후 5 26 38](https://github.com/user-attachments/assets/6a8fa32a-fdaa-47b2-aafe-ad455eaa7a1f)
![스크린샷 2025-05-25 오후 5 26 42](https://github.com/user-attachments/assets/2616139a-1eac-4a3b-87fc-951abfb86709)

- 캘린더 조회, 삭제

![스크린샷 2025-05-25 오후 5 25 48](https://github.com/user-attachments/assets/42449ee0-3524-47ee-9b98-d5dee5a76675)




## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

