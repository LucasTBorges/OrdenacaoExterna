from Arquivo import Arquivo
from copy import deepcopy
from SequenciaCascata import SequenciaCascata

class ArquivoCascata():
    def __init__(self, lists: list = []) -> None:
        self._sequencias:list[SequenciaCascata] = list(map(SequenciaCascata, lists))
        self._writeOps:int = 0 #Contador de operações de escrita no arquivo
        self._congelado:bool = False #Indica se o arquivo já foi arquivo alvo na fase atual da cascata, indicando que não deve mais ser alterado até o fim da fase
        self._seqClosed:bool = False #Indica se a última sequência do arquivo está fechada, indicando que a próxima inserção deve ser em uma nova sequência
        
    
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
        if len(self._sequencias)>0 and not self._seqClosed:
            self._sequencias[-1].append(value)
        else:
            self._sequencias.append(SequenciaCascata([value]))
        self._writeOps += 1
        
    def newSeq(self)->None: #Cria uma nova sequência vazia no arquivo
        self._sequencias.append(SequenciaCascata())

    def dequeue(self)->int: #Retorna o primeiro elemento da primeira sequência do arquivo
        if len(self._sequencias) == 0:
            raise IndexError("Houve a tentativa de remover o primeiro elemento de um arquivo vazio")
        value = self._sequencias[0].dequeue()
        if len(self._sequencias[0]) == 0:
            self._sequencias.pop(0)
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
    
    def getFirstSeqSize(self)->int:
        if len(self._sequencias) == 0:
            raise IndexError("Houve a tentativa de acessar o tamanho da primeira sequência de um arquivo vazio")
        return len(self._sequencias[0])
    
    def closeSeq(self)->None:
        if self._seqClosed:
            raise ValueError("Tentativa de fechar sequência já fechada")
        self._seqClosed = True

    def openSeq(self)->None:
        if not self._seqClosed:
            raise ValueError("Tentativa de abrir sequência já aberta")
        self._seqClosed = False

    @property
    def seqClosed(self)->bool:
        return self._seqClosed

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
