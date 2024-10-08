from PolifasicaApi import PolifasicaApi
from CascataApi import CascataApi
from BalanceadaApi import BalanceadaApi
from SelecaoNatural.Seletor import Seletor


def programa():
    metodo = input()
    match metodo:
        case 'B':
            api = BalanceadaApi()
        case 'P':
            api = PolifasicaApi()
        case 'C':
            api = CascataApi()
        case _:
            print("Escolha uma das opções de métodos disponíveis:\nB = Ordenação Balanceada P-Caminhos\nP = Ordenação Polifásica\nC = Ordenação em Cascata")
            return

    m, k, r, n = map(int, input().split())
    values = list(map(int, input().split()))

    initaL_seqs = Seletor(values, m).selecionar(r)


    api.runAndPrint(initaL_seqs, m, k)

while True:
    programa()
    print()

