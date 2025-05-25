import os

# API 키 설정 (환경변수 우선, 없으면 기본값 사용)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your_google_api_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "your_google_cse_id")

# 환경변수 설정
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID

# 모델 설정
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
SUPERVISOR_TEMPERATURE = 0

# 그래프 설정
RECURSION_LIMIT = 15 