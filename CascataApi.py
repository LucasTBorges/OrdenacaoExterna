from CascataPackage.ArquivoCascata import ArquivoCascata
from CascataPackage.Cascata import Cascata
from CascataPackage.SequenciaCascata import SequenciaCascata
from CascataPackage.DistribuidorCascata import DistribuidorCascata
from SelecaoNatural.Seletor import Seletor
from DadosExecucao import DadosExecucao

class CascataApi:
    def _run(self, input: list[list[int]], ramSize:int, qtdFiles:int, printResult:bool, ordered:bool)->DadosExecucao: #Ordered é a garantia de que as sequências estão ordenadas, se for falso, faz a verificação
        cascata = Cascata(input,ramSize,qtdFiles,ordered)
        cascata.run()
        if printResult:
            print(cascata.output)
        return cascata.dadosExecucao
    
    def run(self, input: list[list[int]], ramSize:int, qtdFiles:int, ordered=True)->DadosExecucao: #Roda a cascata sem imprimir o resultado
        return self._run(input, ramSize, qtdFiles, False, ordered)
    
    def runAndPrint(self, input: list[list[int]], ramSize:int, qtdFiles:int, ordered=True)->DadosExecucao: #Roda a cascata e imprime o resultado
        return self._run(input, ramSize, qtdFiles, True, ordered)
    
    def runFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, False, True)
    
    def runAndPrintFromDados(self, dados: DadosExecucao)->DadosExecucao:
        return self._run(dados.seqsInic, dados.ramSize, dados.qtdArquivos, True, True)

    def runFromDadosList(self, dadosList: list[DadosExecucao])->list[DadosExecucao]:
        return [self.runFromDados(dados) for dados in dadosList]
