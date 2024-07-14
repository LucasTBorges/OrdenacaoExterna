from Arquivo import Arquivo
from copy import deepcopy
class SequenciaCascata():
    def __init__(self, sequencia: list) -> None:
        self._sequencia = sequencia
    
    def __len__(self)->int:
        n = 0
    
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
        return self._sequencia.pop(0)
    
class ArquivoCascata():
    def __init__(self, lists: list = []) -> None:
        self._sequencias = map(SequenciaCascata, lists)
        self._writeOps = 0
    
    @staticmethod
    def converteArquivo(arquivo: Arquivo)->'ArquivoCascata':
        arq = ArquivoCascata()
        arq._sequencias = deepcopy(arquivo.getLists())
        arq._writeOps = arquivo.writeOps
        return arq
    
    @property
    def sequencias(self)->list:
        return self._sequencias
    
    @property
    def qtdSequencias(self)->int: #Retorna a quantidade de sequências não vazias
        for seq in self._sequencias:
            if len(seq) > 0:
                n += 1

    @property
    def writeOps(self)->int:
        return self._writeOps
    
    def append(self,value)->None: #Adiciona um valor à última sequência do arquivo, ou cria uma nova sequência com o valor caso o arquivo esteja vazio
        if len(self._sequencias)>0:
            self._sequencias[-1].append(value)
            self._writeOps += 1
        else:
            self._sequencias.append(SequenciaCascata([value]))
            self._writeOps += 1

    def dequeue(self)->int: #Retorna a primeira sequência do arquivo
        if len(self._sequencias) == 0:
            raise IndexError("Houve a tentativa de remover a primeira sequência de um arquivo vazio")
        return self._sequencias.pop(0)
