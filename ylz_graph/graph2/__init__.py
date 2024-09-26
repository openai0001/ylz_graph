from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph

from .state import State
from .tools import multi

from rich import print

class Graph2(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
    
    def get_graph(self) -> CompiledStateGraph:
        self.llm = self.get_node_llm()
        self.llm_bind_tool = self.llm.bind_tools([multi])
        workflow = StateGraph(State)
        workflow.add_node("nodeB1",NodeB1(self))
        workflow.add_node("nodeB2",NodeB2(self))
        workflow.add_node("tools",ToolNode(tools=[multi]))
        workflow.add_edge(START,"nodeB1")
        workflow.add_edge("nodeB1","nodeB2")
        workflow.add_conditional_edges("nodeB2",tools_condition)
        workflow.add_edge("tools","nodeB2")        
        graph = workflow.compile(self.memory)
        return graph

    def human_action(self, graph, thread_id=None):
        return super().human_action(graph, thread_id)
    
class NodeB1():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        print("--->NodeB1",state)
        llm_bind_tool = self.graphLib.llm_bind_tool
        messages = state["messagesB"]
        messages[-1].content = "你好,"+messages[-1].content
        res = llm_bind_tool.invoke(messages)
        return {"messagesB":[res],"resultB":res.content}

class NodeB2():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        print("--->NodeB2",state)
        llm_bind_tool = self.graphLib.llm_bind_tool
        messages = state["messagesB"]
        sysPrompt = "把以下句子翻译成日文"
        res = llm_bind_tool.invoke([("system",sysPrompt)]+messages)
        return {"messagesB":[res],"resultB":res.content}
        