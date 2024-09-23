from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph

from .state import State

class Graph1(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
    
    def get_graph(self) -> CompiledStateGraph:
        workflow = StateGraph(MessagesState)
        workflow.add_node("nodeA",NodeA("nodeA",self))
        workflow.add_node("nodeB",NodeB("nodeB",self))
        workflow.add_edge(START,"nodeA")
        workflow.add_edge("nodeA","nodeB")
        workflow.add_edge("nodeB",END)        
        graph = workflow.compile(self.memory)
        return graph

    def human_action(self, graph, thread_id=None):
        return super().human_action(graph, thread_id)
    

class NodeA():
    def __init__(self,msg,graphLib:GraphLib=None):
        self.llm=None
        if graphLib:
            self.llm = graphLib.get_node_llm()
        self.msg = msg
    def __call__(self,state):
        print("*"*50,self.msg)
        messages = state["messages"]
        if self.llm:
            res = self.llm.invoke(messages)
            return {"messages":[res]}
        
class NodeB():
    def __init__(self,msg,graphLib:GraphLib=None):
        self.llm=None
        if graphLib:
            self.llm = graphLib.get_node_llm()
        self.msg = msg
        self.tools = [self.add]
    def add(self,a:int , b:int)->int:
        '''将两个整数相加'''
        return a+b
    def __call__(self,state:State):
        print("*"*50,self.msg)
        messages = state["messages"]
        if self.llm:
            llm_bind = self.llm.bind_tools(self.tools)
            res = llm_bind.invoke(messages + [HumanMessage("反思刚才的回答，给出语句更通顺，逻辑更清晰的回答")])
            print("???",res)
            return {"messages":[res]}
    