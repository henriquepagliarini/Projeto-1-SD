import os
import sys
from Lot import Lot
from QueueNames import QueueNames
from RabbitMQConnection import RabbitMQConnection

class MSNotificacao:
    def __init__(self, rabbit: RabbitMQConnection, lots: list[Lot]):
        self.rabbit = rabbit

        self.lots = lots
        print("MS Notificação configurado.")

    def consumeEvent(self):
        self.rabbit.channel.basic_consume(
            queue=QueueNames.BID_VALIDATED.__str__(),
            on_message_callback=self.processValidBid,
            auto_ack=True
        )

        self.rabbit.channel.basic_consume(
            queue=QueueNames.AUCTION_WINNER.__str__(),
            on_message_callback=self.processAuctionWinner,
            auto_ack=True
        )

        try:
            self.rabbit.channel.start_consuming()
        except KeyboardInterrupt:
            print("MS Notificação interrompido")
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)
        except Exception as e:
            print(f"Erro no MS Notificação: {e}")
        finally:
            self.rabbit.disconnect()
            print("MS Notificação terminado com sucesso")

    def publishEvent(self):
        print("Publicando evento")

    def processValidBid(self):
        print("Processando lance válido")
    
    def processAuctionWinner(self):
        print("Processando leilão vencedor")

    def startService(self):
        print("Serviço iniciado")