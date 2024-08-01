from CascataPackage.ArquivoCascata import ArquivoCascata
from CascataPackage.Cascata import Cascata
from CascataPackage.SequenciaCascata import SequenciaCascata
from CascataPackage.DistribuidorCascata import DistribuidorCascata
from SelecaoNatural.Seletor import Seletor
from DadosExecucao import DadosExecucao

class CascataApi:
    def __init__(self, input:list[int], ramSize:int, qtdFiles:int, seqsIniciais:int|None=None):
        self._input:list[int] = input
        self._ramSize:list[int] = ramSize
        self._qtdFiles:list[int] = qtdFiles
        self._seqsIniciais:int|None = seqsIniciais #Número de sequências iniciais desejado, o 'r' do enunciado
        self._files:list[ArquivoCascata] = []
        self._cascata:Cascata

    def runWithSelecaoNatural(self)->DadosExecucao: #Roda o algoritmo com geração de sequencias inicias com seleção natural e retorna os dados de execução
        sequencias:list[SequenciaCascata] = self._selecaoNatural()
        distribuidor:DistribuidorCascata = DistribuidorCascata(sequencias, self._qtdFiles)
        self._files = distribuidor.distributeSequences(True)
        self._cascata = Cascata(self._files, self._ramSize)
        self._cascata.run()
        print(self._cascata.output)
        return self._cascata.dadosExecucao

    def _selecaoNatural(self)->list[list[int]]:
        seletor:Seletor = Seletor(self._input, self._ramSize)
        return seletor.selecionar()

