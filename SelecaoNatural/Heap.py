from SelecaoNatural.Record import Record

class Heap:
    def __init__(self, size:int)->None:
        self._size = size
        self._memory = []

    def insert(self, record: Record|int)->None:
        self._memory.append(record)
        self.heapifyUp(len(self._memory)-1)

    def remove(self)->Record|int:
        if len(self._memory) == 0:
            raise IndexError("Tentativa de remover um registro de uma heap vazia")
        self._memory[0], self._memory[-1] = self._memory[-1], self._memory[0]
        record = self._memory.pop()
        self.heapifyDown(0)
        return record

    def heapifyDown(self, index:int)->None:
        left = Heap .leftChild(index)
        right = Heap.rightChild(index)
        smallest = index
        if left < len(self._memory) and self._memory[left] < self._memory[smallest]:
            smallest = left
        if right < len(self._memory) and self._memory[right] < self._memory[smallest]:
            smallest = right
        if smallest != index:
            self._memory[index], self._memory[smallest] = self._memory[smallest], self._memory[index]
            self.heapifyDown(smallest)

    def heapifyUp(self, index):
        parent  = Heap.parent(index)
        if index > 0 and self._memory[index] < self._memory[parent]:
            self._memory[index], self._memory[parent] = self._memory[parent], self._memory[index]
            self.heapifyUp(parent)

    def unmarkAll(self): #Desmarca todos os registros da heap
        for record in self._memory:
            if not isinstance(record, Record):
                raise TypeError("Tentativa de desmarcar um registro que não é do tipo record")
            if not record.marked:
                raise ValueError("Tentativa de desmarcar um registro que já está desmarcado")
            record.marked = False

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
    def size(self):
        return self._size
    @property
    def full(self):
        return len(self._memory) == self._size
    @property
    def empty(self):
        return len(self._memory) == 0