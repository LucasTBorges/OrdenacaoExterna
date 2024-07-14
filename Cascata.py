class RAMCascata:
    def __init__(self, ramSize: int, memoriaInfinita:bool = False)->None:
        self._size = ramSize #Tamanho da memória principal
        self._memoria = []
        self._memoriaInfinita = memoriaInfinita

    @property
    def size(self)->int:
        return self._size
    
    @property
    def memoria(self)->list:
        return self._memoria
    
    @property
    def qtdRegistros(self)->int:
        n = 0
        for elem in self.memoria:
            try:
                iter(elem)
            except TypeError:
                n += 1
            else:
                n += len(elem)
        return n
    
    @property
    def memoriaInfinita(self)->bool:
        return self._memoriaInfinita
    
    @memoria.setter
    def memoria(self, memoria: list)->None:
        self._memoria = memoria

    @size.setter
    def size(self, size: int)->None:
        self._size = size
    
    def appendElement(self, elemento: int)->None:
        if not self.memoriaInfinita and len(self.memoria) == self.size:
            raise IndexError(f"Houve a tentativa de adicionar um elemento ({elemento}) a uma memória cheia")
        self.memoria.append(elemento)

    def appendList(self, lista: list)->None:
        if not self.memoriaInfinita and len(lista)+self.qtdRegistros > self.size:
            raise IndexError(f"Tentativa de inserir lista que não caberia na memória principal.\nA memória principal ({self.qtdRegistros} espaços ocupados de {self.size}) não comportaria a adição da lista de tamanho {len(lista)}")
        self.memoria.append(lista)

    def intercala(self)->list: #Intercala as listas da memória principal em uma única lista ordenada TODO: Otimizar intercalação usando heap mínima no lugar de ponteiros
        for list in self.memoria:
            try:
                iter(list)
            except TypeError:
                raise TypeError("Houve a tentativa de intercalar um objeto que não é iterável")
        seq = [] #Sequência final ordenada
        pointers = [0] * len(self.memoria) #Ponteiros para cada lista (índice do elemento atual em cada lista da memória)
        minVal = None #Menor valor atual
        minIndex = None #Índice da lista com o menor valor atual
        for lista in self.memoria:
            try:
                lista[0]
            except IndexError:
                raise IndexError("Houve a tentativa de intercalar uma lista vazia")
        while len(pointers) > 0:
            for index, pointer in enumerate(pointers): #Percorre todos os ponteiros, identificando menor valor.
                if minVal is None or self.memoria[index][pointer] < minVal:
                    minVal = self.memoria[index][pointer]
                    minIndex = index
            seq.append(minVal) #Adiciona o menor valor à sequência final
            pointers[minIndex] += 1 #Incrementa o ponteiro da lista com o menor valor
            if pointers[minIndex] == len(self.memoria[minIndex]): #Se o ponteiro da lista com o menor valor atingir o tamanho da lista, remove o ponteiro e a lista da memória principal
                pointers.pop(minIndex)
                self.memoria.pop(minIndex)
            minVal = None #Reseta o menor valor
            minIndex = None #Reseta o índice da lista com o menor valor
        self.memoria = seq #Substitui a memória principal pela sequência final
        return seq
                
                
                
            

class Cascata:
    def __init__(self, arquivos: list, ramSize: int, memoriaInfinita:bool = False)->None:
        self._arquivos = arquivos #Lista de arquivos
        self._fase = 0 #Fase atua
        self._ram = RAMCascata(ramSize, memoriaInfinita) #Memória principal
        self._qtdRegistros = None #Quantidade de registros, calculado quando chamado pela primeira vez
        self._output = "" #String de saída

    def strFase(self)->str:
        string =  f"fase {self.fase} {self.avgSeqSize:.2f}"
        for i in range(len(self.arquivos)):
            arq = self.arquivos[i]
            string += f" {arq.writeOps}"
        

    @property
    def avgSeqSize(self) -> float: #Retorna o valor da função beta, que é a quantidade de registros dividido pela quantidade de sequências vezes o tamanho da memória principal
        return self.qtdRegistros/(self.qtdSequencias*self.ramSize)

    @property
    def fase(self)->int:
        return self._fase
    
    @property
    def arquivos(self)->list:
        return self._arquivos
    
    @property
    def ramSize(self)->int:
        return self._ram.size
    
    @property
    def ram(self)->list:
        return self._ram
    
    @property
    def qtdRegistros(self)->int:
        if self._qtdRegistros is not None:
            return self._qtdRegistros
        n = 0
        for file in self.arquivos:
            n += file.qtdRegistros
        self._qtdRegistros = n
        return n
    
    @property
    def qtdSequencias(self)->int:
        n = 0
        for file in self.arquivos:
            for seq in file.getLists():
                if len(seq) > 0:
                    n += 1
        return n

    @arquivos.setter
    def arquivos(self, arquivos: list)->None:
        self._arquivos = arquivos

    @fase.setter
    def fase(self, fase: int)->None:
        self._fase = fase

    @ramSize.setter
    def ramSize(self, ramSize: int)->None:
        self._ramSize = ramSize
    

