from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition,create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults

class Graph2(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
        #self.set_websearch_tool('TAVILY')
        tool = TavilySearchResults(max_results=2)
        print("test tavily:",tool.invoke("What's a 'node' in LangGraph?"))
        self.tools = [tool]
        #self.set_tools_executor(self.tools)
        
    def get_graph(self) -> CompiledStateGraph:
        llm = self.get_node_llm()
        print("[LLM]",llm)
        print("[TOOLS]",self.tools)
        graph = create_react_agent(llm,self.tools)
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
