from PolifasicaPackage.ArquivoPolifasica import ArquivoPolifasica
from DadosExecucao import DadosExecucao

class Polifasica:
    def __init__(self, qtdRegistros:int, ramSize:int, qtdArquivos:int, seqsInic:list):
        if ramSize < qtdArquivos-1:
            raise ValueError("Memória principal deve ser maior ou igual ao número de arquivos menos 1")
        self._dadosExec = DadosExecucao(ramSize, qtdArquivos, seqsInic)
        self._fase = 0
        self._output = ""
        self._betas = []

        arquivos = []
        for i in range(0, qtdArquivos-1): #Adiciona k-1 arquivos na lista de arquivos
            arquivos.append(ArquivoPolifasica())

        indexArquivo = 0
        indexSequencia = 0
        while indexSequencia < len(seqsInic):
            try:
                arquivos[indexArquivo].appendSequencia(seqsInic[indexSequencia])
            except:
                indexArquivo = 0
                arquivos[indexArquivo].appendSequencia(seqsInic[indexSequencia])

            indexArquivo += 1
            indexSequencia += 1
        arquivos.append(ArquivoPolifasica()) #Adiciona o k-ésimo arquivo (vazio) na lista de arquivos

        self._arquivos = arquivos


    def __str__(self)->str:
        return str([arq.sequencias for arq in self._arquivos])

    @property
    def completo(self):
        arquivos = [arq for arq in self._arquivos if not arq.isEmpty]
        return len(arquivos) == 1 and len(arquivos[0].sequencias) == 1

    @property
    def arquivos(self)->list[ArquivoPolifasica]:
        return self._arquivos

    @property
    def output(self) -> str:
        return self._output

    @property
    def dadosExecucao(self) -> DadosExecucao:
        return self._dadosExec

    @property
    def qtdSequencias(self) -> int:
        n = 0
        for arq in self.arquivos:
            n += arq.qtdSequencias
        return n

    @property
    def qtdRegistros(self) -> int:
        return self._dadosExec.inputSize

    @property
    def avgSeqSize(self) -> float:
        if self.qtdSequencias == 0:
            raise ZeroDivisionError("Quantidade de sequências é zero, impossível calcular beta")
        if self._dadosExec.ramSize == 0:
            raise ZeroDivisionError("Tamanho da memória principal é zero, impossível calcular beta")
        return round(self.qtdRegistros/(self.qtdSequencias*self._dadosExec.ramSize), 2)

    def addToOutput(self) -> None:
        beta = self.avgSeqSize
        self._dadosExec.betas.append(beta)
        self._output += f"fase: {self._fase} {beta}\n"
        for i in range(0, len(self._arquivos)):
            self._output += f"{i+1}: {self._arquivos[i]}\n"
        self._fase += 1

    def setAlpha(self) -> None:
        writeOpsTotal = 0
        for arq in self._arquivos:
            writeOpsTotal += arq.writeOps

        alpha = round((writeOpsTotal / self._dadosExec.inputSize), 2)
        self._dadosExec.alpha = alpha

    def ordenarSequencias(self, sequencias: list):
        new_ordered_list = []
        index = [0] * len(sequencias)

        while any(index[i] < len(sequencias[i]) for i in range(len(sequencias))):
            min_val = float('inf')
            min_idx = None

            for i in range(len(sequencias)):
                if index[i] < len(sequencias[i]) and sequencias[i][index[i]] < min_val:
                    min_val = sequencias[i][index[i]]
                    min_idx = i

            new_ordered_list.append(min_val)
            index[min_idx] += 1

        return new_ordered_list

        
    def polifasear(self):
        self.addToOutput()

        while not self.completo:
            target_file = None
            for file in self._arquivos:
                if file.isEmpty:
                    target_file = file
            if target_file is None:
                raise Exception("Tentativa de executar polifásica falhou pois todos os arquivos estavam ocupados")

            arquivos = [arq for arq in self._arquivos if not arq.isEmpty and arq != target_file]
            while (all([not arq.isEmpty for arq in arquivos])):
                sequencias = [arq.sequencias[0] for arq in arquivos]
                sequencia_ordenada = self.ordenarSequencias(sequencias)
                target_file.appendSequencia(sequencia_ordenada)
                for arq in self._arquivos:
                    if arq != target_file and len(arq.sequencias) > 0:
                        arq.sequencias.pop(0)

            self.addToOutput()

        self.setAlpha()
    