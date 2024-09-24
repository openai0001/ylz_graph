from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition,create_react_agent

class Graph2(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
        self.set_websearch_tool('TAVILY')
        self.tools = [self.websearch_tool]
        self.set_tools_executor(self.tools)
        self.llm = self.get_node_llm()
        self.llm_bind_tools = self.llm.bind_tools(self.tools)

    def get_graph(self) -> CompiledStateGraph:
        graph = create_react_agent(self.llm,self.tools)
        # workflow = StateGraph(MessagesState)
        # workflow.add_node("robot",self.robot)
        # workflow.add_node("tools",self.tool_node)
        # workflow.add_edge(START,"robot")
        # workflow.add_conditional_edges("robot",tools_condition)
        # workflow.add_edge("tools","robot")        
        # graph = workflow.compile(self.memory)
        return graph

    def human_action(self, graph, thread_id=None):
        return super().human_action(graph, thread_id)
    
    def robot(self,state:MessagesState):
        res  = self.llm_bind_tools.invoke(state["messages"])
        return {"messages":[res]}        
