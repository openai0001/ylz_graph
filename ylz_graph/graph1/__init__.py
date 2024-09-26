from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph

from .state import State
from .tools import add
from rich import print

class Graph1(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
    
    def get_graph(self) -> CompiledStateGraph:
        self.llm = self.get_node_llm()
        self.llm_bind_tool = self.llm.bind_tools([add])
        workflow = StateGraph(State)
        workflow.add_node("nodeA1",NodeA1(self))
        workflow.add_node("nodeA2",NodeA2(self))
        workflow.add_node("tools",ToolNode(tools=[add]))
        workflow.add_edge(START,"nodeA1")
        workflow.add_edge("nodeA1","nodeA2")
        workflow.add_conditional_edges("nodeA2",tools_condition)
        workflow.add_edge("tools","nodeA2")        
        graph = workflow.compile(self.memory)
        return graph

    def human_action(self, graph, thread_id=None):
        return super().human_action(graph, thread_id)
    
class NodeA1():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        print("--->NodeA1",state)
        llm_bind_tool = self.graphLib.llm_bind_tool
        messages = state["messagesA"]
        messages[-1].content = "你好,"+ messages[-1].content
        res = llm_bind_tool.invoke(messages)
        return {"messagesA":[res],"resultA":res.content}
class NodeA2():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        print("--->NodeA2",state)
        llm_bind_tool = self.graphLib.llm_bind_tool
        messages = state["messagesA"]
        sysPrompt = "把以下句子翻译成英文"
        res = llm_bind_tool.invoke([("system",sysPrompt)]+messages)
        return {"messagesA":[res],"resultA":res.content}
        
