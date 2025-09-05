echo "Configurando ambiente virtual..."

python3 -m venv venv

source venv/bin/activate

echo "Instalando dependências..."
pip install apscheduler pika rsa

echo "Ambiente configurado!"