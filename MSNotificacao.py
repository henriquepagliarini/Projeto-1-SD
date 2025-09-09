import json
import pika
from QueueNames import QueueNames
from RabbitMQConnection import RabbitMQConnection

class MSNotificacao:
    def __init__(self):
        print("Configurando MS Notificação")
        self.rabbit = RabbitMQConnection()
        self.rabbit.connect()
        self.rabbit.setupDirectExchange("leiloes")
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
        self.rabbit.channel.start_consuming()

    def processValidBid(self, ch, method, properties, body):
        try:
            bid_data = json.loads(body)
            auction_id = int(bid_data["auction_id"])
            event = {
                "type": "lance_realizado",
                "auction_id": auction_id,
                "user_id": bid_data["user_id"],
                "value": bid_data["value"],
            }
            self.publishToAuctionQueue(auction_id, event)
            print(f"Lance validado enviado para o leilão {auction_id}")
        except Exception as e:
            print(f"Erro ao processar lance válido: {e}")
    
    def processAuctionWinner(self, ch, method, properties, body):
        try:
            winner_data = json.loads(body)
            auction_id = int(winner_data["auction_id"])
            event = {
                "type": "leilao_finalizado",
                "auction_id": auction_id,
                "user_id": winner_data["user_id"],
                "highest_bid": winner_data["highest_bid"],
            }
            self.publishToAuctionQueue(auction_id, event)
            print(f"Leilão {auction_id} finalizado enviado.")
        except Exception as e:
            print(f"Erro ao processar leilão vencedor: {e}")

    def publishToAuctionQueue(self, auction_id, event):
        self.rabbit.channel.basic_publish(
            exchange=self.rabbit.direct_exchange,
            routing_key=f"leilao_{auction_id}",
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def startService(self):
        print("Iniciando MS Notificação")
        print("--------------------------------")
        print("Aguardando notificações para enviar...")
        try:
            self.consumeEvents()
        except KeyboardInterrupt:
            print("MS Notificação interrompido")
        except Exception as e:
            print(f"Erro no MS Notificação: {e}")
        finally:
            self.rabbit.disconnect()
            print("MS Notificação terminado com sucesso")