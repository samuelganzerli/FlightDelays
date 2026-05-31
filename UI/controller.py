from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArrivo= None
        self._choicePartenza = None

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt =="":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("inserire un valore numerico per il numero minimo di compagnie. ", color="red")
            )
            self._view.update_page()
            return


        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtInCMin.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("inserire un valore intero per il numero minimo di compagnie. ", color="red")
            )
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("il filtro sul numero di compagnie deve essere un intero positivo. ", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        nNodes, nEdges = self._model.getGraphDetails()

        allNodes = self._model.getAllNodes()
        self.fillDropDown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato: ", color="Green")
        )
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi. ", color="Green")
        )
        self._view.update_page()

    def handleTestConnessione(self,e):

        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre "
                                                           "selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre "
                                                           "selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text(f"non ho trovato un cammino tra i due aeroporti: "
                                                           f"{self._choicePartenza} e {self._choiceArrivo}", color="orange"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceArrivo)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(ft.Text(f"ho trovato un cammino tra i due aeroporti: "
                                                       f"{self._choicePartenza} e {self._choiceArrivo}. Di seguito i nodi del cammino",
                                                       color="green"))
        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()


    def handleConnessi(self, e):

        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre "
                                                           "selezionare un aeroporto di partenza"))
            self._view.update_page()
            return

        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(ft.Text(f"{v[0]} - peso {v[1]}"))
        self._view.update_page()


    def handleCerca(self, e):

        t = self._view._txtInTratteMax.value
        try:
            tInt = int(t)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("il valore di t deve essere un intero positivo", color="red"))
            return

        tic = datetime.now()



        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view._txtResults.controls.clear()

        self._view._txtResults.controls.append(
            ft.Text(f"cammino fra {self._choicePartenza} e {self._choiceArrivo} trovato", color = "green"))
        self._view._txtResults.controls.append(
            ft.Text(f"il cammino ha uno score complessivo di: {score} e contiene i seguenti nodi: ", color = "green"))

        for p in path:
            self._view._txtResults.controls.append(
                ft.Text(p, color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"cammino trovato in {datetime.now()-tic}: ", color="green"))

        self._view.update_page()
        return





    def fillDropDown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self._choiceDdPartenza
                                   )
            )
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self._choiceDdArrivo
                                   )
            )

    def _choiceDdPartenza(self,e):
        self._choicePartenza = e.control.data
        print(f"Hai selezionato {self._choicePartenza} come aeroporto di partenza")

    def _choiceDdArrivo(self, e):
        self._choiceArrivo = e.control.data
        print(f"Hai selezionato {self._choiceArrivo} come aeroporto di arrivo")




















