from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def buildGraph(self, a1, a2):
        self._graph.clear()
        print(self._graph)
        self._addNodes(a1, a2)
        print(self._graph)
        self._addEdges(a1, a2, self._idMap)
        print(self._graph)

    def _addNodes(self, a1, a2):
        allNodes = DAO.getAllNodes(a1, a2)
        for n in allNodes:
            self._idMap[n.driverId] = n
        self._graph.add_nodes_from(allNodes)
        return

    def _addEdges(self, a1, a2, idMap):
        allEdges = DAO.getAllEdges(a1, a2, idMap)
        for e in allEdges:
            self._graph.add_edge(e.p1, e.p2, weight=e.weight)
        return

    def topTreArchi(self):
        listaArchi = list(self._graph.edges(data = True))
        listaArchi.sort(key=lambda x:x[2]["weight"],reverse=True)
        return listaArchi[:3]

    def getNumCC(self):
        return nx.number_connected_components(self._graph)

    def getMaxCC(self):
        compMax = []
        for n in self._graph.nodes():
            if len(nx.node_connected_component(self._graph,n)) > len(compMax):
                compMax = list(nx.node_connected_component(self._graph,n))
        listaNodiDegree = []
        for n in compMax:
            degree = self._graph.degree(n)
            listaNodiDegree.append((n,degree))
        listaNodiDegree.sort(key=lambda x:x[1],reverse=True)
        return listaNodiDegree

    def getNumNodiArchi(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllYears(self):
        return DAO.getAllYears()
