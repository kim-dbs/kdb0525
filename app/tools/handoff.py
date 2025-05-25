from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.graph import MessagesState
from langgraph.types import Command

def create_handoff_tool(agent_name: str, description: str):
    @tool(f"transfer_to_{agent_name}", description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
    ) -> Command:  # 다음에이전트로 핸드오프
        return Command(
            goto=agent_name,
        )
    return handoff_tool 