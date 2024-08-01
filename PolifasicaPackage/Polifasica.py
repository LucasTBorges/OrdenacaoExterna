from PolifasicaPackage.ArquivoPolifasica import ArquivoPolifasica
from DadosExecucao import DadosExecucao

class Polifasica:
    def __init__(self, qtdRegistros:int, ramSize:int, arquivos: list[ArquivoPolifasica], nSeqsInic:int = -1):
        self._qtdRegistros = qtdRegistros

        if nSeqsInic == -1:
            qtdSeq = 0
            for arq in arquivos:
                qtdSeq += arq.qtdSequencias

            self._dadosExec = DadosExecucao(qtdRegistros, ramSize, qtdSeq)
        else:
            self._dadosExec = DadosExecucao(qtdRegistros, ramSize, nSeqsInic)

        self._arquivos = arquivos
        self._fase = 0
        self._output = ""

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
    def qtdSequencias(self) -> int:
        n = 0
        for arq in self.arquivos:
            n += arq.qtdSequencias
        return n

    @property
    def qtdRegistros(self) -> int:
        return self._qtdRegistros

    @property
    def avgSeqSize(self) -> float:
        if self.qtdSequencias == 0:
            raise ZeroDivisionError("Quantidade de sequências é zero, impossível calcular beta")
        if self._dadosExec.ramSize == 0:
            raise ZeroDivisionError("Tamanho da memória principal é zero, impossível calcular beta")
        return self.qtdRegistros/(self.qtdSequencias*self._dadosExec.ramSize)

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
        self._output += f"fase: {self._fase} {self.avgSeqSize:.2f}\n"
        for i in range(0, len(self._arquivos)):
            self._output += f"{i+1}: {self._arquivos[i]}\n"
        self._fase += 1
        while not self.completo:
            target_file = None
            for file in self._arquivos:
                if file.isEmpty:
                    target_file = file
            if target_file is None:
                raise Exception("Tentativa de executar cascata falhou pois todos os arquivos estavam ocupados")

            arquivos = [arq for arq in self._arquivos if not arq.isEmpty and arq != target_file]
            while (all([not arq.isEmpty for arq in arquivos])):
                sequencias = [arq.sequencias[0] for arq in arquivos]
                sequencia_ordenada = self.ordenarSequencias(sequencias)
                target_file.appendSequencia(sequencia_ordenada)
                for arq in self._arquivos:
                    if arq != target_file and len(arq.sequencias) > 0:
                        arq.sequencias.pop(0)

            self._output += f"fase: {self._fase} {self.avgSeqSize:.2f}\n"
            for i in range(0, len(self._arquivos)):
                self._output += f"{i+1}: {self._arquivos[i]}\n"
            self._fase += 1
    