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

if __name__ == "__main__":
    print("Iniciando...")
    r = RabbitMQConnection()
    r.connect()
    time.sleep(5)
    r.disconnect()