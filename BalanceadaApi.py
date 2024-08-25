from BalanceadaPackage.Balanceada import Balanceada
from DadosExecucao import DadosExecucao

class BalanceadaApi:
    def _run(self, seqsInic: list[list[int]], ramSize:int, qtdArquivos:int, printResult:bool, beta_test:bool = False)->DadosExecucao:
        balanceada = Balanceada(ramSize, qtdArquivos, seqsInic)
        balanceada.run()
        if printResult:
            print(balanceada.output)
        return balanceada.dadosExecucao
    
    def run(self, seqsInic: list[list[int]], ramSize:int, qtdArquivos:int, beta_test:bool = False)->DadosExecucao:
        return self._run(seqsInic, ramSize, qtdArquivos, False, beta_test)
    
    def runAndPrint(self, seqsInic: list[list[int]], ramSize:int, qtdArquivos:int)->DadosExecucao: #Ordena e imprime o resultado
        return self._run(seqsInic, ramSize, qtdArquivos, True)
    
    def runFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, False, True)
    
    def runAndPrintFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, True, True)

    def runFromDadosList(self, dadosList: list[DadosExecucao])->list[DadosExecucao]:
        return [self.runFromDados(dados) for dados in dadosList]