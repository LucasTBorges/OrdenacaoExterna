from Arquivo import Arquivo
from copy import deepcopy
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
    
class ArquivoCascata():
    def __init__(self, lists: list = []) -> None:
        self._sequencias = list(map(SequenciaCascata, lists))
        self._writeOps = 0
        self._congelado = False
    
    @staticmethod
    def converteArquivo(arquivo: Arquivo)->'ArquivoCascata':
        arq = ArquivoCascata()
        arq._sequencias = deepcopy(arquivo.getLists())
        arq._writeOps = arquivo.writeOps
        return arq
    
    def appendList(self, lista: list|SequenciaCascata)->None: #Adiciona uma sequência à lista de sequências do arquivo, ou converte a lista em uma sequência (se for uma lista) e a adiciona
        if isinstance(lista, SequenciaCascata):
            self._sequencias.append(lista)
        else:
            self._sequencias.append(SequenciaCascata(lista))
        self._writeOps += len(lista)

    def appendElement(self,value:int)->None: #Adiciona um valor à última sequência do arquivo, ou cria uma nova sequência com o valor caso o arquivo esteja vazio
        if len(self._sequencias)>0:
            self._sequencias[-1].append(value)
            self._writeOps += 1
        else:
            self._sequencias.append(SequenciaCascata([value]))
            self._writeOps += 1

    def dequeue(self)->int: #Retorna a primeira sequência do arquivo
        if len(self._sequencias) == 0:
            raise IndexError("Houve a tentativa de remover a primeira sequência de um arquivo vazio")
        value = self._sequencias.pop(0)
        return value
    
    def congela(self)->None:
        if self._congelado:
            raise ValueError("Tentativa de congelar arquivo já congelado")
        self._congelado = True

    def descongela(self)->None:
        if not self._congelado:
            raise ValueError("Tentativa de descongelar arquivo não congelado")
        self._congelado = False
    
    def __str__(self)->str:
        string=""
        for seq in self._sequencias:
            string += str(seq)
        return string
    
    @property
    def isEmpty(self)->bool:
        return len(self._sequencias) == 0

    @property
    def sequencias(self)->list:
        return self._sequencias

    @property
    def qtdRegistros(self)->int:
        n = 0
        for seq in self._sequencias:
            n += len(seq)
        return n
    
    @property
    def qtdSequencias(self)->int: #Retorna a quantidade de sequências não vazias
        n=0
        for seq in self._sequencias:
            if len(seq) > 0:
                n += 1
        return n

    @property
    def writeOps(self)->int:
        return self._writeOps
    
    @property
    def congelado(self)->bool:
        return self._congelado
