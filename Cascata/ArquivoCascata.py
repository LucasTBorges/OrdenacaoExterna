from Arquivo import Arquivo
from copy import deepcopy
from SequenciaCascata import SequenciaCascata

class ArquivoCascata():
    def __init__(self, lists: list = []) -> None:
        self._sequencias = list(map(SequenciaCascata, lists))
        self._writeOps = 0
        self._congelado = False
    
    @staticmethod
    def converteArquivo(arquivo: Arquivo)->'ArquivoCascata':
        arq = ArquivoCascata()
        arq._sequencias = list(SequenciaCascata, deepcopy(arquivo.getLists()))
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
