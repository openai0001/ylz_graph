from ylz_utils.config import Config
from ylz_utils.database.neo4j import Neo4jLib
from ylz_utils.langchain import LangchainLib
from ylz_graph.graph1 import Graph1

Config.init('ylz_graph')
langchainLib = LangchainLib()

def get_graph1():
    print("graph_cloud:life")
    graph1= Graph1(langchainLib)
    graph1.set_thread("youht","default")
    graph1.set_nodes_llm_config(("LLM.ZHIPU",None))
    graph = graph1.get_graph()
    return graph

graph1 = get_graph1()
