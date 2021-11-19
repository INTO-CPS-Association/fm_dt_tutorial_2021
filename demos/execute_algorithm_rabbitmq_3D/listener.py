#!/usr/bin/env python
import pika

if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',credentials=pika.PlainCredentials(
                                                                               username="incubator",
                                                                               password="incubator")))
    channel = connection.channel()

    print("Declaring exchange")
    channel.exchange_declare(exchange='Incubator_AMQP', exchange_type='topic')

    print("Creating queue")
    result = channel.queue_declare(queue='', exclusive=True, auto_delete=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='Incubator_AMQP', queue=queue_name,
                       routing_key='incubator.cosim.controller.parameters')

    print(' [*] Waiting for logs. To exit press CTRL+C')
    print(' [*] I am consuming the commands sent from rbMQ')

    def callback(ch, method, properties, body):
        print("Received [x] %r" % body)


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

    connection.close()