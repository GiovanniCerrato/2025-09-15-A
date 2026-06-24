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

    def getNumNodiArchi(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllYears(self):
        return DAO.getAllYears()
