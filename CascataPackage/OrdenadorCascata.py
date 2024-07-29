from CascataPackage.SequenciaCascata import SequenciaCascata
from CascataPackage.ArquivoCascata import ArquivoCascata
from CascataPackage.Cascata import Cascata

class OrdenadorCascata:
    def __init__(self, input:list[int], ramSize: int)->None:
        self._input = input
        self._ramSize = ramSize