from DadosExecucao import DadosExecucao
from BalanceadaPackage.DistribuidorBalanceada import DistribuidorBalanceada
from BalanceadaPackage.ArquivoBalanceada import ArquivoBalanceada

class Balanceada:
    def __init__(self, ramSize: int, qtdArquivos:int, seqsInic:list) -> None:
        self._dadosExec = DadosExecucao(ramSize, qtdArquivos, seqsInic)
        distribuidor = DistribuidorBalanceada(qtdArquivos, seqsInic)
        self._arquivosEntrada:dict[int: ArquivoBalanceada] = distribuidor.criarArquivosEntrada()
        self._arquivosSaida:dict[int: ArquivoBalanceada] = distribuidor.criarArquivosSaida()
        self._isOut = True

        self._alpha = 0.0
        
        self._fase = 0
        self._output = ""
        self._betas = []

    def __str__(self) -> str:
        saida = "" 
        for chave in self._arquivosEntrada:
            saida += f"{chave}: {self._arquivosEntrada[chave]}\n"
        for chave in self._arquivosSaida:
            saida += f"{chave}: {self._arquivosSaida[chave]}\n"
        return saida
    
    def setAlpha(self)->None:
        writeOpsTotal = 0
        for arq in self._arquivosEntrada.values():
            writeOpsTotal += arq.getWriteOps
        for arq in self._arquivosSaida.values():
            writeOpsTotal += arq.getWriteOps

        alpha = round((writeOpsTotal / self._dadosExec.inputSize), 2)
        self._dadosExec.alpha = alpha
        self._output += f"final {alpha:.2f}"

        self._alpha = alpha

    @property
    def getAlpha(self)->float:
        return self._alpha

    @property
    def output(self)->str:
        return self._output

    @property
    def dadosExecucao(self)->DadosExecucao:
        return self._dadosExec

    @property
    def completo(self)->bool:

        arquivosEntrada = [arq for arq in self._arquivosEntrada.values() if not arq.isEmpty]
        arquivosSaida = [arq for arq in self._arquivosSaida.values() if not arq.isEmpty]

        return len(arquivosEntrada) == 1 or len(arquivosSaida) == 1

    @property
    def qtdSequencias(self)->int:
        n = 0
        for arq in self._arquivosEntrada.values():
            n+=arq.getQtdSequencias
        for arq in self._arquivosSaida.values():
            n+=arq.getQtdSequencias
        return n

    @property   
    def qtdRegistros(self)->int:
        return self._dadosExec.inputSize

    @property
    def avgSeqSize(self)->float:
        if self.qtdSequencias == 0:
            raise ZeroDivisionError("Quantidade de sequências é zero, impossível calcular beta")
        if self._dadosExec.ramSize == 0:
            raise ZeroDivisionError("Tamanho da memória principal é zero, impossível calcular beta")
        return round(self.qtdRegistros/(self.qtdSequencias*self._dadosExec.ramSize), 2)

    @property
    def haveSequence(self)->bool:
        arquivos = [arq for arq in self._arquivosEntrada.values()]
        
        for arq in arquivos:
            if not arq.isEmpty:
                return True
        
        return False


    def addToOutput(self)->None:
        beta = self.avgSeqSize
        self._dadosExec.betas.append(beta)
        self._output += f"fase {self._fase} {beta}\n"


        arquivos:dict[int: ArquivoBalanceada] = self._arquivosEntrada
        for i in arquivos:
            if not arquivos[i].isEmpty:
                self._output += f"{i}: {arquivos[i]}\n"
        self._fase += 1

    def intercalar(self, sequencias: list[list[int]]) -> list[int]:
        new_ordered_list = []

        while len(sequencias)>0:
            min_val = float('inf')
            index=0
            for i in range(len(sequencias)):
                if sequencias[i][0]<min_val:
                    min_val = sequencias[i][0]
                    index=i
            
            new_ordered_list.append(min_val)
            del sequencias[index][0]
            if len(sequencias[index])==0:
                del sequencias[index]
        
        return new_ordered_list
    
    def balancear(self)->None:
        arquivos = [arq for arq in self._arquivosEntrada.values()]
        target = [arq for arq in self._arquivosSaida.values()]
        
        index = 0
        while(self.haveSequence):
            sequencias = []
            for arq in arquivos:
                if not arq.isEmpty:
                    while(len(arq.getSequencias[0]) == 0):
                        arq.removeSequencia(0)    
                    sequencias.append(arq.getSequencias[0])


            sequencia_ordenada = self.intercalar(sequencias)
            target[index].appendNewSequencia(sequencia_ordenada)



            for arq in arquivos:
                if not arq.isEmpty:
                    arq.removeSequencia(0)

            index= (index+1)%len(arquivos)
        
        self._isOut = not self._isOut

        [self._arquivosEntrada, self._arquivosSaida] = [self._arquivosSaida, self._arquivosEntrada]
            
        

    def run(self)->None:
        self.addToOutput()

        while not self.completo:
            self.balancear()
            self.addToOutput()
        
        self.setAlpha()



