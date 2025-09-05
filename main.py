from MSLance import MSLance
from MSLeilao import MSLeilao
from MSNotificacao import MSNotificacao
from RabbitMQConnection import RabbitMQConnection


if __name__ == "__main__":
    print("Iniciando...")
    rabbit = RabbitMQConnection()
    rabbit.connect()
    rabbit.setupExchange("leiloes")
    ms_leilao = MSLeilao(rabbit)
    ms_lance = MSLance(rabbit)
    ms_notificacao = MSNotificacao(rabbit, ms_leilao.lots)
    ms_leilao.startService()