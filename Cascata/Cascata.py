from ArquivoCascata import SequenciaCascata, ArquivoCascata
from RAMCascata import RAMCascata

class Cascata:
    def __init__(self, arquivos: list, ramSize: int, memoriaInfinita:bool = False)->None:
        self._arquivos = arquivos #Lista de arquivos
        self._fase = 0 #Fase atua
        self._ram = RAMCascata(ramSize, memoriaInfinita) #Memória principal
        self._qtdRegistros = None #Quantidade de registros, calculado quando chamado pela primeira vez
        self._output = "" #String de saída

    def run(self)->str: #Executa a ordenação
        self.addToOutput()
        while not self.completo:
            self.cascatear()
        self.output += f"\nfinal {self.calcEsforco():.2f}"
        return self.output

    def strFase(self)->str:
        string =  f"fase {self.fase} {self.avgSeqSize:.2f}"
        for i in range(len(self.arquivos)):
            arq = self.arquivos[i]
            if not arq.isEmpty:
                string += "\n"
                string += f"{i+1}: {arq}"
        return string

    def calcEsforco(self)->float: #Calcula a função alfa, que é a quantidade de operações de escrita dividida pela quantidade de registros
        writeOps = 0
        for arq in self.arquivos:
            writeOps += arq.writeOps
        return writeOps/self.qtdRegistros
    
    def faseCompleta(self)->bool: #Retorna True se todos os arquivos estiverem congelados ou vazios, significando que a fase atual foi completada
        for arq in self.arquivos:
            if not arq.congelado and not arq.isEmpty:
                return False
        return True

    def descongelarAll(self)->None: #Descongela todos os arquivos
        for arq in self.arquivos:
            if arq.congelado:
                arq.descongela()

    def cascatear(self)->None:#Executa uma fase da cascata
        while not self.faseCompleta():
            targetFile = None
            for file in self.arquivos:
                if file.isEmpty:
                    targetFile = file
            if targetFile is None:
                raise Exception("Tentativa de executar cascata falhou pois todos os arquivos estavam ocupados")
            arquivos = [arq for arq in self.arquivos if arq != targetFile and not arq.isEmpty and not arq.congelado] #lista os arquivos com sequências a serem intercaladas
            if len(arquivos) == 0:
                raise Exception("Tentativa de executar cascata falhou pois não haviam arquivos disponíveis para intercalar, apesar da verificação de faseCompleta ter indicado o contrário")
            while (all([not arq.isEmpty for arq in arquivos])):#Enquanto nenhum dos arquivos disponíveis para intercalação forem esvaziados, intercala as sequências
                for arq in arquivos:
                    self.ram.appendList(arq.dequeue())
                self.ram.intercala()
                targetFile.appendList(self.ram.memoria)
                self.ram.memoria = []
            targetFile.congela()
        self.fase += 1 #Incrementa a fase
        self.descongelarAll() #Descongela todos os arquivos
        self.addToOutput() #Adiciona a string da fase atual à string de saída

    def addToOutput(self)->None: #Adiciona a string da fase atual à string de saída
        if self.output != "":
            self.output += "\n"
        self.output += self.strFase()

    @property
    def completo(self) -> bool: #Retorna true se existir uma única sequência ordenada restante
        arquivos = [arq for arq in self.arquivos if not arq.isEmpty]
        if arquivos == 0:
            raise Exception("Tentativa de verificar se a cascata está completa falhou pois todos os arquivos estão vazios")
        if len(arquivos) > 1:
            return False
        return len(arquivos[0].sequencias) == 1

    @property
    def avgSeqSize(self) -> float: #Retorna o valor da função beta, que é a quantidade de registros dividido pela quantidade de sequências vezes o tamanho da memória principal
        if self.qtdSequencias == 0:
            raise ZeroDivisionError("Quantidade de sequências é zero, impossível calcular beta")
        if self.ramSize == 0:
            raise ZeroDivisionError("Tamanho da memória principal é zero, impossível calcular beta")
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
    def ram(self)->RAMCascata:
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
            n += file.qtdSequencias
        return n
    
    @property
    def output(self)->str:
        return self._output

    @arquivos.setter
    def arquivos(self, arquivos: list)->None:
        self._arquivos = arquivos

    @fase.setter
    def fase(self, fase: int)->None:
        self._fase = fase

    @ramSize.setter
    def ramSize(self, ramSize: int)->None:
        self._ramSize = ramSize

    @output.setter
    def output(self, output: str)->None:
        self._output = output