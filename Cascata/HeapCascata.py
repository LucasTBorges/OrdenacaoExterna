class HeapCascata: #TODO: implementar como heap mínima
    def __init__(self, size:int, memoriaInfinita:bool = False)->None:
        self._size = size
        self._infinite = memoriaInfinita
        self._memory = []

    def queue(self, elemento:int, fileNum:int)->None:
        if not self._infinite and self.isFull:
            raise IndexError(f"Houve a tentativa de adicionar o elemento ({elemento}) a uma memória cheia")
        for i in range(len(self._memory)):
            if self._memory[i] > elemento:
                self._memory.insert(i, {"value":elemento, "file":fileNum})
                return

    def dequeue(self)->int:
        return self._memory.pop(0)
    
    @property
    def isFull(self)->bool:
        return len(self._memory) == self._size
    
    @property
    def freeSpace(self)->int:
        return self._size - len(self._memory)