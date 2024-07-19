class SequenciaCascata():
    def __init__(self, sequencia: list, ordenado= False) -> None:
        if not ordenado: #Essa classe representa uma sequência ordenada, o parâmetro ordenado é uma garantia de que a sequência é ordenada. Sem essa garantia, verifica-se se a sequência está ordenada
            for i in range(1, len(sequencia)):
                if sequencia[i] < sequencia[i-1]:
                    raise ValueError(f"A sequência passada não está ordenada. Sequência: {sequencia}. Elementos {sequencia[i-1]} (índice {i-1}) e {sequencia[i]} (índice {i}) estão fora de ordem.")
        self._sequencia = sequencia
    
    def __len__(self)->int:
        return len(self._sequencia)
    
    def __getitem__(self, index: int)->int:
        return self._sequencia[index]
    
    def __setitem__(self, index: int, value: int)->None:
        self._sequencia[index] = value

    def __str__(self)->str:
        return "{" + " ".join([str(x) for x in self._sequencia]) + "}"
    
    def __iter__(self):
        return iter(self._sequencia)
    
    def __next__(self):
        return next(self._sequencia)
    
    def append(self, elemento: int)->None:
        self._sequencia.append(elemento)

    def dequeue(self)->int: #Retorna o primeiro elemento da sequência
        if len(self._sequencia) == 0:
            raise IndexError("Houve a tentativa de remover o primeiro elemento de uma sequência vazia")
        retorno = self._sequencia.pop(0)
        return retorno
    