import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    user_prompt: str 