from ylz_utils.config import Config
from ylz_utils.database.neo4j import Neo4jLib
from ylz_utils.langchain import LangchainLib
from ylz_graph.graph1 import Graph1
from ylz_graph.graph2 import Graph2
from ylz_graph.graph3 import Graph3

from ylz_utils.langchain.graph.test_graph.function import FunctionGraph

Config.init('ylz_graph')
langchainLib = LangchainLib()

def get_graph1():
    print("graph_cloud:graph1")
    graphLib= Graph1(langchainLib)
    graphLib.set_thread("youht","default")
    graphLib.set_nodes_llm_config(("LLM.ZHIPU",None))
    graph = graphLib.get_graph()
    return graph

def get_graph2():
    print("graph_cloud:graph2")
    graphLib= Graph2(langchainLib)
    graphLib.set_thread("youht","default")
    graphLib.set_nodes_llm_config(("LLM.ZHIPU",None))
    graph = graphLib.get_graph()
    return graph

def get_graph3():
    print("graph_cloud:graph3")
    graphLib= Graph3(langchainLib)
    graphLib.set_thread("youht","default")
    graphLib.set_nodes_llm_config(("LLM.ZHIPU",None))
    graph = graphLib.get_graph()
    return graphLib,graph

# graph1 = get_graph1()
# graph2 = get_graph2()
# graphLib,graph3 = get_graph3()

# graphLib.graph_test(graph3,"我爱中国")

graphLib = FunctionGraph(langchainLib)
graphTest = graphLib.get_graph()

#graphLib.graph_test(graphTest,"我叫张三",config={"configurable":{"thread_id":"youht-default","user_id":"youht","llm_key":"LLM.DEEPBRICKS"}})
