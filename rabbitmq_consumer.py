#!/usr/bin/env python
import pika, sys, os

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('127.0.0.1',
                                    5672,
                                    '/',
                                    credentials)

    connection = pika.BlockingConnection(parameters)
    
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')


    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)