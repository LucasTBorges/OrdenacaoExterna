from CascataPackage.ArquivoCascata import ArquivoCascata
from CascataPackage.HeapCascata import HeapCascata
from CascataPackage.Intercalador import Intercalador
from DadosExecucao import DadosExecucao
from CascataPackage.DistribuidorCascata import DistribuidorCascata

class Cascata:
    def __init__(self, input:list[list[int]], ramSize: int, qtdFiles: int, ordered=False)->None: #Parâmetro ordered indica se há certeza de que as sequências iniciais estão ordenadas e portanto não deve haver uma checagem de ordenação
        if ramSize < qtdFiles-1:
            raise ValueError("Memória principal deve ser maior ou igual ao número de arquivos menos 1")
        distribuidor = DistribuidorCascata(input, qtdFiles)
        self._arquivos:list[ArquivoCascata] = distribuidor.distributeSequences(ordered) #Lista de arquivos
        self._fase:int = 0 #Fase atual
        self._ram:HeapCascata = HeapCascata(ramSize) #Memória principal
        self._qtdRegistros:int|None = None #Quantidade de registros, calculado quando chamado pela primeira vez
        self._output:str = "" #String de saída
        self._dadosExecucao:DadosExecucao = DadosExecucao(ramSize, qtdFiles, input)

    @staticmethod
    def loadFromDados(dados:DadosExecucao)->'Cascata': #Carrega uma instância de Cascata a partir de um objeto DadosExecucao
        return Cascata(dados.seqsInic, dados.ramSize, dados.qtdArquivos)

    def run(self)->str: #Executa a ordenação
        self.addToOutput()
        while not self.completo:
            self.cascatear()
        alfa:float = self.calcEsforco()
        self.output += f"\nfinal {alfa:.2f}"
        self._dadosExecucao.alpha = alfa #Adiciona o valor de alfa aos dados de execução
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
        nRegistros:int = self.qtdRegistros
        if nRegistros == 0:
            raise ZeroDivisionError("Quantidade de registros é zero, impossível calcular alfa")
        for arq in self.arquivos:
            writeOps += arq.writeOps
        return writeOps/nRegistros
    
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
            targetFile:ArquivoCascata|None = None
            for file in self.arquivos:
                if file.isEmpty:
                    targetFile = file
            if targetFile is None:
                raise Exception("Tentativa de executar cascata falhou pois todos os arquivos estavam ocupados")
            arquivos = [arq for arq in self.arquivos if arq != targetFile and not arq.isEmpty and not arq.congelado] #lista os arquivos com sequências a serem intercaladas
            if len(arquivos) == 0:
                raise Exception("Tentativa de executar cascata falhou pois não haviam arquivos disponíveis para intercalar, apesar da verificação de faseCompleta ter indicado o contrário")
            while (all([not arq.isEmpty for arq in arquivos])):#Enquanto nenhum dos arquivos disponíveis para intercalação forem esvaziados, intercala as sequências
                merger: Intercalador = Intercalador(arquivos, targetFile, self.ram)
                merger.intercala()
            targetFile.congela()
        self.fase += 1 #Incrementa a fase
        self.descongelarAll() #Descongela todos os arquivos
        self.addToOutput() #Adiciona a string da fase atual à string de saída e adiciona o valor atual de beta aos dados de execução

    def addToOutput(self)->None: #Adiciona a string da fase atual à string de saída e adiciona o valor atual de beta aos dados de execução
        if self.output != "":
            self.output += "\n"
        self.output += self.strFase()
        self._dadosExecucao.betas.append(self.avgSeqSize) #Adiciona o valor atual de beta aos dados de execução

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
        return self.qtdRegistros/(self.qtdSequenciasReais*self.ramSize)

    @property
    def fase(self)->int:
        return self._fase
    
    @property
    def arquivos(self)->list[ArquivoCascata]:
        return self._arquivos
    
    @property
    def ramSize(self)->int:
        return self._ram.size
    
    @property
    def ram(self)->HeapCascata:
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
    def qtdSequenciasReais(self)->int:
        n = 0
        for file in self.arquivos:
            n += file.qtdSequenciasReais
        return n
    
    @property
    def output(self)->str:
        return self._output

    @property
    def dadosExecucao(self)->DadosExecucao:
        return self._dadosExecucao

    @arquivos.setter
    def arquivos(self, arquivos: list[ArquivoCascata])->None:
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