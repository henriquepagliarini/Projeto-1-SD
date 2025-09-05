from enum import Enum

class QueueNames(Enum):
    AUCTION_STARTED = "leilao_iniciado"
    AUCTION_ENDED = "leilao_finalizado"
    BID_DONE = "lance_realizado"
    BID_VALIDATED = "lance_validado"
    AUCTION_WINNER = "leilao_vencedor"
    AUCTION_1 = "leilao_1"
    AUCTION_2 = "leilao_2"

    def __str__(self):
        return self.value
