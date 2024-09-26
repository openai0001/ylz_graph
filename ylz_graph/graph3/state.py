from langgraph.graph import MessagesState

class State(MessagesState):
    messagesA: list
    messagesB: list
    resultA: str
    resultB: str