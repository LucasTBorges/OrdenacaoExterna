from CascataPackage.Registro import Registro

class HeapCascata:
    def __init__(self, size:int)->None:
        self._size = size
        self._memory = []

    def queue(self, elemento:Registro, fileNum:int)->None:
        if self.isFull:
            raise IndexError(f"Houve a tentativa de adicionar o elemento ({elemento}) a uma memória cheia")
        record = {"value":elemento, "file":fileNum}
        self._memory.append(record)
        self.heapifyUp(len(self._memory)-1)
        return

    def dequeue(self)->int:
        if self.isEmpty:
            raise IndexError("Houve a tentativa de remover um elemento de uma memória vazia")
        record = self._memory[0]
        self._memory[0] = self._memory[-1]
        self._memory.pop()
        self.heapifyDown(0)
        return record
    
    def __str__(self) -> str:
        return "(Valor, Origem): {" + " ".join([f'({x["value"]}, {x["file"]})' for x in self._memory]) + "}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def heapifyDown(self, index:int)->None:
        left = HeapCascata.leftChild(index)
        right = HeapCascata.rightChild(index)
        smallest = index
        if left < len(self._memory) and self._memory[left]["value"] < self._memory[smallest]["value"]:
            smallest = left
        if right < len(self._memory) and self._memory[right]["value"] < self._memory[smallest]["value"]:
            smallest = right
        if smallest != index:
            self._memory[index], self._memory[smallest] = self._memory[smallest], self._memory[index]
            self.heapifyDown(smallest)

    def heapifyUp(self, index):
        parent  = HeapCascata.parent(index)
        if index > 0 and self._memory[index]["value"] < self._memory[parent]["value"]:
            self._memory[index], self._memory[parent] = self._memory[parent], self._memory[index]
            self.heapifyUp(parent)
    
    @staticmethod
    def parent(index:int)->int:
        return (index-1)//2
    @staticmethod
    def leftChild(index:int)->int:
        return 2*index + 1
    @staticmethod
    def rightChild(index:int)->int:
        return 2*index + 2

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