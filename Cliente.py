from datetime import datetime
import json
import os
import sys
from QueueNames import QueueNames
from RabbitMQConnection import RabbitMQConnection
from User import User


class Cliente:
    def __init__(self, user: User, rabbit: RabbitMQConnection):
        self.user = user
        self.rabbit = rabbit
        self.auctions = [int]
        print(f"Cliente {self.user.id} configurado: {self.user.name}")
    
    def consumeStartedAuctions(self):
        self.rabbit.channel.basic_consume(
            queue=QueueNames.AUCTION_STARTED.__str__(),
            on_message_callback=self.processStartedLot,
            auto_ack=True
        )

        try:
            self.rabbit.channel.start_consuming()
        except KeyboardInterrupt:
            self.keyboardException()
        except Exception as e:
            print(f"Erro no cliente: {e}")
        finally:
            self.rabbit.disconnect()

    def processStartedLot(self, ch, method, properties, body):
        try:
            lot = json.loads(body)
            lot_id = lot.get("lot_id")
            description = lot.get("description")
            start_date = lot.get("start_date")
            end_date = lot.get("end_date")
            
            print(f"NOVO LEILÃO INICIADO!")
            print(f"ID: {lot_id}")
            print(f"Descrição: {description}")
            print(f"Início: {start_date}")
            print(f"Fim: {end_date}")

            try:
                answer = input(f"Deseja participar do leilão {lot_id}: {description}? (s/n): ").strip().lower()
                
                if answer == 's':
                    self.consumeRegisteredLot(lot_id)
                    print(f"Interesse registrado no leilão {lot_id}")
                else:
                    print(f"Não participará do leilão {lot_id}")
                    
            except Exception as e:
                print(f"Erro ao processar resposta: {e}")
        except json.JSONDecodeError:
            print("Mensagem de leilão inválida")
        except Exception as e:
            print(f"Erro ao processar leilão: {e}")

    def consumeRegisteredLot(self, lot_id: int):
        try:
            self.rabbit.channel.basic_consume(
                queue=f"leilao_{lot_id}",
                on_message_callback=self.processLotNotification,
                auto_ack=True
            )
            self.auctions.append(lot_id)
        except KeyboardInterrupt:
            self.keyboardException()
        except Exception as e:
            print(f"Erro no cliente: {e}")
        finally:
            self.rabbit.disconnect()

    def processLotNotification(self, ch, method, properties, body):
        return

    def keyboardException(self):
        print("Cliente interrompido")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)

    def startService(self):
        print(f"CLIENTE: {user.name}")
        print("--------------------------------")
        self.consumeStartedAuctions()


if __name__ == "__main__":
    user_id = int(input("Digite seu ID de usuário: ").strip())
    user_name = input("Digite seu nome: ").strip()
    
    if not user_id or not user_name:
        print("ID e nome são obrigatórios!")
        exit(1)
        
    rabbit = RabbitMQConnection()
    rabbit.connect()
    rabbit.setupExchange("leiloes")
    user = User(user_id, user_name)
    client = Cliente(user, rabbit)
    client.startService()