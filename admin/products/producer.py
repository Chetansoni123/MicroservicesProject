import pika, json

params = pika.URLParameters('amqps://emcdgmsb:4R1JgXsFJMq5zeOEscolPWCntH9grE1D@fuji.lmq.cloudamqp.com/emcdgmsb')

# create a connection channel with RabbitMQ
connection = pika.BlockingConnection(params)
channel = connection.channel() 

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

