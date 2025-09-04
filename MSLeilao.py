from datetime import datetime, timedelta
import time
import pika

class RabbitMQConnection:
    def __init__(self):
        self.connection: None
        self.channel: None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters("localhost")
            )
            self.channel = self.connection.channel()
            print("Conectado ao RabbitMQ.")
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}.")
            return False
        
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexão fechada.")

class MSLeilao:
    def __init__(self):
        self.rabbit = RabbitMQConnection()
        self.rabbit.connect()

        self.auctionLot = [
            {
                "id": 1,
                "description": "Celular",
                "start_date": datetime.now() + timedelta(seconds=10),
                "end_date": datetime.now() + timedelta(seconds=30),
                "status": "ATIVO"
            },
            {
                "id": 2,
                "description": "Televisão",
                "start_date": datetime.now() + timedelta(seconds=20),
                "end_date": datetime.now() + timedelta(seconds=40),
                "status": "INATIVO"
            },
            {
                "id": 3,
                "description": "Carro",
                "start_date": datetime.now() + timedelta(seconds=30),
                "end_date": datetime.now() + timedelta(seconds=20),
                "status": "INATIVO"
            }
        ]

        self.setupQueues()

    def setupQueues(self):
        self.rabbit.channel.exchange_declare(
            exchange='leiloes', 
            exchange_type='direct', 
            durable=True
        )

        self.rabbit.channel.queue_declare(
            queue="leilao_iniciado",
            durable=True
        )
        self.rabbit.channel.queue_bind(
            exchange="leiloes", 
            queue="leilao_iniciado", 
            routing_key="leilao_iniciado"
        )
        print("Fila de leilões iniciados iniciada.")

        self.rabbit.channel.queue_declare(
            queue="leilao_finalizado",
            durable=True
        )
        self.rabbit.channel.queue_bind(
            exchange="leiloes", 
            queue="leilao_finalizado", 
            routing_key="leilao_finalizado"
        )
        print("Fila de leilões finalizados iniciada.")

if __name__ == "__main__":
    print("Iniciando...")
    ms_leilao = MSLeilao()
    ms_leilao.rabbit.disconnect()