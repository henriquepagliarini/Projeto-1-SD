import pika


class RabbitMQConnection:
    def __init__(self):
        self.connection: None
        self.channel: None
        self.isOnline = False

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters("localhost")
            )
            self.channel = self.connection.channel()
            self.isOnline = True
            print("Conectado ao RabbitMQ.")
        except Exception as e:
            print(f"Erro ao conectar {e}.")
        
    def disconnect(self):
        if self.isOnline:
            self.connection.close()
            print("Conexão fechada.")
    
    def setupExchange(self, exchange: str):
        self.channel.exchange_declare(
            exchange=exchange, 
            exchange_type='direct', 
            durable=True
        )
        print(f"Exchange '{exchange}' criada.")

    def setupQueue(self, exchange: str, queue: str, routing_key: str):
        self.channel.queue_declare(
            queue=queue,
            durable=True
        )

        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key
        )
        print(f"Fila '{queue}' iniciada.")