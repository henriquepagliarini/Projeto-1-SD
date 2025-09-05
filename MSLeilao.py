from datetime import datetime
import json
import os
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import pika
from Lot import Lot
from QueueNames import QueueNames
from RabbitMQConnection import RabbitMQConnection

class MSLeilao:
    def __init__(self, rabbit: RabbitMQConnection):
        self.rabbit = rabbit
        self.scheduler = BackgroundScheduler()
        self.setupQueues()
        self.lots = self.initializeLots()
        self.scheduleLots()
        print("MS Leilão configurado.")

    def setupQueues(self):
        self.rabbit.setupRabbitQueues(self.rabbit.exchange, QueueNames.AUCTION_STARTED.__str__())
        self.rabbit.setupRabbitQueues(self.rabbit.exchange, QueueNames.AUCTION_ENDED.__str__())

    def initializeLots(self) -> list[Lot]:
        lots = [
            Lot(1, "Celular", {"seconds": 10}, {"seconds": 15}, self.rabbit),
            Lot(2, "Televisão", {"seconds": 20}, {"seconds": 10}, self.rabbit),
            Lot(3, "Carro", {"seconds": 25}, {"seconds": 10}, self.rabbit)
        ]
        print("Lotes inicializados")
        return lots

    def scheduleLots(self):
        print("Agendando leilões...")
        for lot in self.lots:
            self.scheduler.add_job(
                func=self.startAuction,
                trigger=DateTrigger(run_date=lot.start_date),
                args=[lot.id],
            )

            self.scheduler.add_job(
                func=self.endAuction,
                trigger=DateTrigger(run_date=lot.end_date),
                args=[lot.id]
            )

            print(f"Leilão {lot.id}: {lot.description}")
            print(f"Início: {lot.start_date.strftime('%H:%M:%S')}")
            print(f"Fim: {lot.end_date.strftime('%H:%M:%S')}\n")

    def startAuction(self, lot_id: int):
        lot = self.findLotById(lot_id)
        
        if lot:
            try:
                lot.openLot()
                event = {
                    "lot_id": lot.id,
                    "description": lot.description,
                    "start_date": lot.start_date.isoformat(),
                    "end_date": lot.end_date.isoformat(),
                    "status": lot.status.__str__(),
                }
                self.publishEvent(QueueNames.AUCTION_STARTED.__str__(), event)
            except Exception as e:
                print(f"Erro ao iniciar leilão {lot_id}: {e}")

    def endAuction(self, lot_id: int):
        lot = self.findLotById(lot_id)
        
        if lot:
            try:
                lot.closeLot()
                event = {
                    "lot_id": lot.id,
                    "description": lot.description,
                    "start_date": lot.start_date.isoformat(),
                    "end_date": lot.end_date.isoformat(),
                    "status": lot.status.__str__(),
                    "highest_bid": lot.currentBid,
                    "winner": lot.winner.name if lot.winner else "Nenhum"
                }
                self.publishEvent(QueueNames.AUCTION_ENDED.__str__(), event)

                print(f"Leilão {lot.id} finalizado: {lot.description}")

                if lot.winner:
                    print(f"Vencedor: {lot.winner.name} - R${lot.currenteBid:.2f}")
                else:
                    print(f"Sem lances")
            except Exception as e:
                print(f"Erro ao finalizar leilão {lot_id}: {e}")

    def publishEvent(self, routing_key: str, event: dict):
        try:
            self.rabbit.channel.basic_publish(
                exchange="leiloes",
                routing_key=routing_key,
                body=json.dumps(event, default=str),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(f"Evento publicado em '{routing_key}'")
        except Exception as e:
            print(f"Erro ao publicar evento: {e}")

    def findLotById(self, lot_id: int) -> Lot | None:
        for lot in self.lots:
            if lot.id == lot_id:
                return lot
        return None
    
    def startService(self):
        print("INICIANDO SISTEMA DE LEILÃO")
        print("--------------------------------")
        print(f"Agora são {datetime.now().strftime('%H:%M:%S')}\n")

        print("Leilões agendados:")
        for lot in self.lots:
            time_to_start = (lot.start_date - datetime.now()).total_seconds()
            print(f"Leilão {lot.id}: {lot.description} inicia em {time_to_start:.0f}s\n")
        
        print("Iniciando scheduler...")
        self.scheduler.start()

        try:
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("MS Leilão interrompido")
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)
        except Exception as e:
            print(f"Erro no MS Leilão: {e}")
        finally:
            self.scheduler.shutdown()
            self.rabbit.disconnect()
            print("MS Leilão terminado com sucesso")