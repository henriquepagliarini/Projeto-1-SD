import os
import sys
import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='',
                        routing_key='task_queue',
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.Delivery_mode.Persistent
                        ))
    print(f" [x] Sent {message}")

    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)