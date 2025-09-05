from QueueNames import QueueNames
from RabbitMQConnection import RabbitMQConnection

class MSLance:
    def __init__(self, rabbit: RabbitMQConnection):
        self.rabbit = rabbit
        self.setupQueues()

    def setupQueues(self):
        self.rabbit.setupRabbitQueues(self.rabbit.exchange, QueueNames.BID_DONE.__str__())
        self.rabbit.setupRabbitQueues(self.rabbit.exchange, QueueNames.BID_VALIDATED.__str__())
        self.rabbit.setupRabbitQueues(self.rabbit.exchange, QueueNames.AUCTION_WINNER.__str__())
    
    def consumeEvent(self):
        print("Publicando evento")

    def publishEvent(self):
        print("Publicando evento")

    def processBid(self):
        print("Processando lance válido")
    
    def processAuctionWinner(self):
        print("Processando leilão vencedor")

    def startService(self):
        print("Serviço iniciado")