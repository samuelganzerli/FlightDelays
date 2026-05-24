import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes (nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addEdges()

    def addEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        #Queste tratte hanno due problemi
        #1- Ho archi diretti inversi (0-20 e 20-1, da sommare)
        #2- Ho tutti gli aerporto senza il filtro dei 5

        for t in allTratte:
            #Controlliamo se l'aeroporto è nei miei filtri
            if t.aeroprtoP in self._graph and t.aeroprtoA in self._graph:
                if self._graph.has_edge(t.aeroprtoP, t.aeroprtoA):
                    self._graph[t.aeroprtoP][t.aeroprtoA]["weight"] += t.peso
                else:
                    #allora posso aggiungerlo
                    self._graph.add_edge(t.aeroprtoP,t.aeroprtoA,weight= t.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)