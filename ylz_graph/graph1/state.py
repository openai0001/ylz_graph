from langgraph.graph import add_messages
from typing import Annotated
class State():
    messagesA: Annotated[list,add_messages]
    resultA: str