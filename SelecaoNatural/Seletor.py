from SelecaoNatural.Heap import Heap
from SelecaoNatural.Record import Record
class Seletor:
    def __init__(self, input: list[int], size:int)->None: #Recebe uma lista de registros e o tamanho da memória principal
        if(size<1):
            raise ValueError("Tamanho da memória principal inválido")
        if(len(input)<1):
            raise ValueError("Entrada vazia")
        self._heap: Heap = Heap(size)
        self._input: list[int] = input
        self._output: list[list[int]] = [[]]
        self._remaining: int = len(input) #Número de registros restantes para serem processados

    def selecionar(self)->list[list[int]]:
        while not self._heap.full and len(self._input)>0:
            self._heap.insert(Record(self._input.pop(0)))
        while self._remaining>0:
            nextRecordOutput: Record = self._heap.remove()
            if nextRecordOutput.marked:#Se o registro do topo da heap foi marcado, todos os registros da heap já foram marcados então desmarcaremos todos e iniciaremos uma nova sequência ordenada
                self._output.append([nextRecordOutput.value])
                self._heap.unmarkAll()
            else:
                self._output[-1].append(nextRecordOutput.value)
            self._remaining -= 1 #Uma vez que um registro é colocado na saída, reduzimos em 1 o número de registros restantes
            if len(self._input)>0:
                nextValueInput:int = self._input.pop(0)
                nextRecordInput: Record = Record(nextValueInput, len(self._output[-1])>0 and nextValueInput<self._output[-1][-1]) #Marcamos o registro da entrada se ele for menor que o último registro da sequência ordenada atual
                self._heap.insert(nextRecordInput)
        return self._output

            

