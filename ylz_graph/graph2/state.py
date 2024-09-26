from langgraph.graph import add_messages
from typing import Annotated

class State():
    messagesB: Annotated[list,add_messages]
    resultB: str