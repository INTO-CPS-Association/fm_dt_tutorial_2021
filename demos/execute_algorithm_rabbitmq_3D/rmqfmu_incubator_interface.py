#!/usr/bin/env python3
## this script flattens the json structure of the msgs sent by the incubator, 
# and forwards it via the rabbitmq server to the rmmfmu
## it also connects to a custom exchange -- this is not yet configurable on the rmqfmu
import pika
import json
from datetime import datetime
import threading
import pandas as pd


new_data = False
data = {}
lock = threading.Lock()
host = "localhost"

def callback(ch, method, properties, body):
    global new_data, data, lock
    with lock:
        new_data = True
        data = body
    print("Received [x] %r" % body)
    print("")

def publishToRmqfmu():
    global new_data, data, lock
    print(' [*] Will publish to rmqfmu')

    credentials = pika.PlainCredentials('incubator', 'incubator')
    connection_rmqfmu = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=credentials))
    channel_rmqfmu = connection_rmqfmu.channel()

    channel_rmqfmu.exchange_declare(exchange='Incubator_AMQP', exchange_type='topic')
    result = channel_rmqfmu.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel_rmqfmu.queue_bind(exchange='Incubator_AMQP', routing_key='incubator.cosim.bridge.state', queue=queue_name)
    
    seqno = 1
    try:
        while True:
            if new_data:
                with lock:
                    flattened = pd.json_normalize(json.loads(data))
                    flattened['t3'] = flattened['fields.t3']
                    del flattened['fields.t3']
                    flattened["average_temperature"] = flattened["fields.average_temperature"]
                    del flattened["fields.average_temperature"]
                    flattened["heater_on"] = flattened["fields.heater_on"]
                    del flattened["fields.heater_on"]
                    print("")
                    timet = datetime.fromtimestamp(flattened.iloc[0,1]/pow(10,9)) #turn to sec from nanosec
                    #flattened.iloc[0,1] = datetime.strftime( timet, "%Y-%m-%dT%H:%M:%S.%f%z").isoformat()
                    flattened.iloc[0,1] = timet.astimezone().isoformat(timespec='milliseconds')
                    flattened.iloc[0,4] = flattened.iloc[0,4]/pow(10,9) #turn to sec from nanosec
                    flattened.iloc[0,6] = flattened.iloc[0,6]/pow(10,9) #turn to sec from nanosec
                    flattened.iloc[0,8] = flattened.iloc[0,8]/pow(10,9) #turn to sec from nanosec
                    #flattened["seqno"] = seqno
                    flattened = flattened.reset_index()
                    del flattened['index']
                    #remove the first character [ and last ] from the json string
                    flattened = flattened.to_json(orient='records')[1:-1]

                    channel_rmqfmu.basic_publish(exchange='Incubator_AMQP', routing_key='incubator.cosim.bridge.state', body=flattened)
                    print("[*] Sent")
                    print(flattened) 
                    new_data = False
                seqno = seqno + 1
    except KeyboardInterrupt:
        connection_rmqfmu.close()

def consumeFromIncubator():
    credentials = pika.PlainCredentials('incubator', 'incubator')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
    channel = connection.channel()

    print("Declaring exchange")
    channel.exchange_declare(exchange='Incubator_AMQP', exchange_type='topic')

    print("Creating queue")
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='Incubator_AMQP', queue=queue_name,
                    routing_key='incubator.record.driver.state')

    print(' [*] Waiting for logs. To exit press CTRL+C')
    print(' [*] I am consuming the commands sent from incubator')

    channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

    connection.close()

def run_bridge():
    thread = threading.Thread(target = publishToRmqfmu)
    thread.start()

    thread2 = threading.Thread(target = consumeFromIncubator)
    thread2.start()

if __name__ == '__main__':
    run_bridge()
