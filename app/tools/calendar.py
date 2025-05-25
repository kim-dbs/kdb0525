from langchain_google_community.calendar.toolkit import CalendarToolkit

def get_calendar_tools():
    """캘린더 도구들을 반환합니다."""
    calendar_toolkit = CalendarToolkit()
    return calendar_toolkit.get_tools()

# 캘린더 도구들을 미리 로드
calendar_tools = get_calendar_tools() 