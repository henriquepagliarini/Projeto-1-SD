from enum import Enum

class LotStatus(Enum):
    INACTIVE = "Inativo"
    ACTIVE = "Ativo"
    CLOSED = "Encerrado"

    def __str__(self):
        return self.value
