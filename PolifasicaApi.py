from PolifasicaPackage.Polifasica import Polifasica
from DadosExecucao import DadosExecucao

class PolifasicaApi:
    def _run(self, ramSize:int, qtdArquivos:int, seqsInic: list[list[int]], printResult:bool)->DadosExecucao:
        polifasica = Polifasica(ramSize, qtdArquivos, seqsInic)
        polifasica.run()
        if printResult:
            print(polifasica.output)
        return polifasica.dadosExecucao
    
    def run(self, ramSize:int, qtdArquivos:int, seqsInic: list[list[int]])->DadosExecucao:
        return self._run(ramSize, qtdArquivos, seqsInic, False)
    
    def runAndPrint(self, ramSize:int, qtdArquivos:int, seqsInic: list[list[int]])->DadosExecucao: #Ordena e imprime o resultado
        return self._run(ramSize, qtdArquivos, seqsInic, True)
    
    def runFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, False, True)
    
    def runAndPrintFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, True, True)

    def runFromDadosList(self, dadosList: list[DadosExecucao])->list[DadosExecucao]:
        return [self.runFromDados(dados) for dados in dadosList]
