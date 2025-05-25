from langchain_core.tools import tool
from langchain_community.tools import GoogleSearchRun
from langchain_community.utilities import GoogleSearchAPIWrapper
#search tools google search api
@tool
def search_agent(query: str) -> str:
    """ 웹에서 여행지나 맛집 등 최신 정보를 검색합니다."""
    wrapper = GoogleSearchAPIWrapper()
    search = GoogleSearchRun(api_wrapper=wrapper)
    results = search.run(query)
    return f"검색 결과: {results}" 