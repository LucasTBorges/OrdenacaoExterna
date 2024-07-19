class HeapCascata: #TODO: implementar como heap mínima
    def __init__(self, size:int)->None:
        self._size = size
        self._memory = []

    def queue(self, elemento:int, fileNum:int)->None:
        if self.isFull:
            raise IndexError(f"Houve a tentativa de adicionar o elemento ({elemento}) a uma memória cheia")
        record = {"value":elemento, "file":fileNum}
        if len(self._memory) == 0:
            self._memory.append(record)
            return
        for i in range(len(self._memory)):
            if self._memory[i]["value"] > elemento:
                self._memory.insert(i, record)
                return
        self._memory.append(record)
        return

    def dequeue(self)->int:
        return self._memory.pop(0)
    
    def __str__(self) -> str:
        return "(Valor, Origem): {" + " ".join([f'({x["value"]}, {x["file"]})' for x in self._memory]) + "}"
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def isFull(self)->bool:
        return len(self._memory) == self._size
    
    @property
    def freeSpace(self)->int:
        return self._size - len(self._memory)
    
    @property
    def isEmpty(self)->bool:
        return len(self._memory) == 0
    
    @property
    def size(self)->int:
        return self._size