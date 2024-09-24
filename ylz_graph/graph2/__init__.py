from ylz_utils.langchain.graph import GraphLib
from langgraph.graph import StateGraph, START,END, MessagesState
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition,create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

@tool
def _wrapTavily(query):
    '''
    从互联网上查询query，返回字符串结果
    '''
    search = TavilySearchAPIWrapper(tavily_api_key="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")
    tool = TavilySearchResults(api_wrapper=search,max_results=2)
    tool_doc = tool | RunnableLambda(lambda doc:str(doc), name="Tavily2Document")
    res = tool_doc.invoke(query)
    return res

class Graph2(GraphLib):
    def __init__(self,langchainLib):
        super().__init__(langchainLib)
        #self.set_websearch_tool('TAVILY')
        #self.set_tools_executor(self.tools)
        res = _wrapTavily("北京天气如何?")
        print(res,type(res))
        self.tools = [_wrapTavily]
        
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
