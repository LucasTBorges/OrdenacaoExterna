class Cascata:
    def __init__(self, arquivos: list, ramSize: int)->None:
        self._arquivos = arquivos #Lista de arquivos
        self._fase = 0 #Fase atual
        self._ramSize = ramSize #Número de registros que cabem na memória principal
        self._ram = [] #Memória principal
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
        return self._ramSize
    
    @property
    def ram(self)->list:
        return self._ram
    
    @property
    def qtdRegistros(self)->int:
        if self._qtdRegistros is not None:
            return self._qtdRegistros
        n = 0
        for file in self.arquivos:
            for seq in file.getLists():
                n += len(seq)
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
    

