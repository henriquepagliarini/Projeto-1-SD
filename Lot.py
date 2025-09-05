from datetime import datetime, timedelta
from typing import Dict, Union
from LotStatus import LotStatus
from User import User

TimeConfig = Dict[str, Union[int, float]]

class Lot:
    def __init__(self, id: int, description: str, start_in: TimeConfig, duration: TimeConfig):
        self.config = [start_in, duration]
        self.id = id
        self.description = description
        self.start_date = self.calculateStartDate()
        self.end_date = self.calculateEndDate()
        self.status = LotStatus.INACTIVE
        self.currenteBid = 0.0
        self.bids = []
        self.winner = None

    def parseTimeConfig(self, time_config: TimeConfig):
        delta = timedelta()
        if "days" in time_config:
            delta += timedelta(days=time_config["days"])
        if "hours" in time_config:
            delta += timedelta(hours=time_config["hours"])
        if "minutes" in time_config:
            delta += timedelta(minutes=time_config["minutes"])
        if "seconds" in time_config:
            delta += timedelta(seconds=time_config["seconds"])
        return delta

    def calculateStartDate(self):
        delta = self.parseTimeConfig(self.config[0])
        return datetime.now() + delta

    def calculateEndDate(self):
        delta = self.parseTimeConfig(self.config[1])
        return self.start_date + delta

    def openLot(self):
        if self.status == LotStatus.INACTIVE:
            self.status = LotStatus.ACTIVE
            return
        raise Exception(f"Não é possível iniciar um lote {self.status}")
    
    def closeLot(self):
        if self.status == LotStatus.ACTIVE:
            self.status = LotStatus.CLOSED
            return
        raise Exception(f"Não é possível encerrar um lote {self.status}")
    
    def addBid(self, bid: float, user: User):
        if self.status != LotStatus.ACTIVE:
            raise Exception(f"Lance inválido: Leilão {self.status}.")
        
        if bid <= self.currenteBid:
            raise Exception("Lance inválido: Menor ou igual ao existente.")
        self.currenteBid = bid
        self.winner = user
        self.bids.append(Bid(bid, user))

    def __str__(self):
        # s = "".join(f"Lote {self.id}: {self.description}\n")
        # s = s.join(f"({self.status})\n")
        # s = s.join(f"Início: {self.start_date.strftime('%H:%M:%S')}\n")
        # s = s.join(f"Fim: {self.end_date.strftime('%H:%M:%S')}\n")
        # s = s.join(f"Lance mais alto: {self.currenteBid}\n")
        # for bid in self.bids:
            # s = s.join(f"Lances:\n {bid}")
        # return s
        return (f"Lote {self.id}: {self.description}\n"
                f"({self.status})\n"
                f"Início: {self.start_date.strftime('%H:%M:%S')}\n"
                f"Fim: {self.end_date.strftime('%H:%M:%S')}\n"
                f"Highest bid: {self.currenteBid}\n"
                f"Bids: \n") # fazer as bids

class Bid:
    def __init__(self, bid: float, user: User):
        self.bid = bid
        self.user = user
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"Valor: R${self.bid:.2f}\n"
                f"Usuário: {self.user.name}\n"
                f"Horário: {self.timestamp.strftime('%H:%M:%S')}\n")