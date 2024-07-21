class Registro():
    def __init__(self, value: int|None = None) -> None:
        self._value = value
        if value is None:
            self._fake = True #Registro "falso", fará parte de sequências falsas
        else:
            self._fake = False #Resgitro "verdadeiro", contém um valor

    def __str__(self) -> str:
        if self._fake:
            return "*"
        return str(self._value)
    
    def __repr__(self) -> str:
        return f'({self.__str__()})'
    
    def __lt__(self, other: "Registro") -> bool:
        if self._fake:
            return False
        if other.fake:
            return True
        return self._value < other.value
    
    def __gt__(self, other: "Registro") -> bool:
        if self._fake:
            return True
        if other.fake:
            return False
        return self._value > other.value
    
    def __le__(self, other: "Registro") -> bool:
        return self < other or self == other
    
    def __ge__(self, other: "Registro") -> bool:
        return self > other or self == other

    def __eq__(self, other: "Registro") -> bool:
        if self._fake and other.fake:
            return True
        return self._value == other._value

    @staticmethod
    def convertValue(value) -> 'Registro':
        if isinstance(value, Registro):
            return value
        return Registro(value)
        
    
    @property
    def value(self) -> int:
        return self._value
    
    @property
    def fake(self) -> bool:
        return self._fake