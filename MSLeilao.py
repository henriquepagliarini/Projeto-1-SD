from Lot import Lot
from RabbitMQConnection import RabbitMQConnection

class MSLeilao:
    def __init__(self):
        self.rabbit = RabbitMQConnection()
        self.rabbit.connect()
        self.setupQueues()
        self.lots = self.initializeLots()

    def setupQueues(self):
        exchange = "leiloes"
        self.rabbit.setupExchange(exchange)
        self.rabbit.setupQueue(exchange, "leilao_iniciado", "leilao_iniciado")
        self.rabbit.setupQueue(exchange, "leilao_finalizado", "leilao_finalizado")

    def initializeLots(self):
        return [
            Lot(1, "Celular", {"seconds": 10}, {"minutes": 2}),
            Lot(2, "Televisão", {"seconds": 30}, {"minutes": 3}),
            Lot(3, "Carro", {"seconds": 40}, {"minutes": 2})
        ]

    def startAuction(self):
        for lot in self.lots:
            print(lot)
        
        self.rabbit.disconnect()

if __name__ == "__main__":
    print("Iniciando...")
    ms_leilao = MSLeilao()
    ms_leilao.startAuction()