RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🌟 여행 AI 어시스턴트 시작 중...${NC}"

# __pycache__ 폴더 정리
echo -e "${YELLOW}📁 캐시 파일 정리 중...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 가상환경 확인 및 활성화
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}🔧 가상환경이 없습니다. 생성 중...${NC}"
    python -m venv .venv
fi

echo -e "${YELLOW}🔧 가상환경 활성화 중...${NC}"
source .venv/bin/activate

# 의존성 설치
echo -e "${YELLOW}📦 의존성 설치 중...${NC}"
if ! pip install -r requirements.txt; then
    echo -e "${RED}❌ 의존성 설치 실패${NC}"
    exit 1
fi

# 환경 변수 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env 파일이 없습니다. 환경 변수를 설정해주세요.${NC}"
    echo -e "${YELLOW}   필요한 환경 변수: OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID${NC}"
fi

# 포트 설정 (기본값: 8501, 사용 중이면 다른 포트 사용)
PORT=8501
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; do
    echo -e "${YELLOW}⚠️  포트 $PORT가 사용 중입니다. 다음 포트 시도 중...${NC}"
    PORT=$((PORT + 1))
done

echo -e "${GREEN}🚀 Streamlit 앱 실행 중... (포트: $PORT)${NC}"
echo -e "${GREEN}🌐 브라우저에서 http://localhost:$PORT 로 접속하세요${NC}"

# Streamlit 앱 실행
streamlit run main.py --server.port $PORT --server.address 0.0.0.0 