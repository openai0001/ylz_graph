from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph

from .state import State
# from .tools import multi

from ..graph1 import Graph1
from ..graph2 import Graph2

from rich import print

class Graph3(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
    
    def get_graph(self) -> CompiledStateGraph:
        self.llm = self.get_node_llm()
        graphLib1= Graph1(self.langchainLib)
        graphLib1.set_thread("youht","default")
        graphLib1.set_nodes_llm_config(("LLM.ZHIPU",None))
        graph1 = graphLib1.get_graph()

        graphLib2= Graph2(self.langchainLib)
        graphLib2.set_thread("youht","default")
        graphLib2.set_nodes_llm_config(("LLM.DEEPBRICKS",None))
        graph2 = graphLib2.get_graph()

        workflow = StateGraph(State)
        workflow.add_node("nodeC1",NodeC1(self))
        workflow.add_node("graph1",graph1)
        workflow.add_node("graph2",graph2)
        workflow.add_node("nodeC2",NodeC2(self))
         
        workflow.add_edge(START,"nodeC1")
        workflow.add_edge("nodeC1","graph1")
        workflow.add_edge("nodeC1","graph2")
        workflow.add_edge(["graph1","graph2"],"nodeC2")        
        workflow.add_edge("nodeC2",END)
        graph = workflow.compile(self.memory)
        return graph

    def human_action(self, graph, thread_id=None):
        return super().human_action(graph, thread_id)
    
class NodeC1():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        print("NodeC1")
        messages = state['messages']
        return {"messagesA":[messages[-1]],"messagesB":[messages[-1]]}

class NodeC2():
    def __init__(self,graphLib:GraphLib=None):
        self.graphLib =graphLib 
    def __call__(self,state):
        #messages = state["messages"]
        print("NodeC2")
        print("final state:",state)
        return {"messages":[('user','ok')]}