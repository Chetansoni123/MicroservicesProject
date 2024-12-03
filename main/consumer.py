import pika, json
from main import Product, db, app

params = pika.URLParameters('amqps://emcdgmsb:4R1JgXsFJMq5zeOEscolPWCntH9grE1D@fuji.lmq.cloudamqp.com/emcdgmsb')
# create a connection channel with RabbitMQ
connection = pika.BlockingConnection(params)
channel = connection.channel() 

# verify if the queue exists or not
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    with app.app_context():
        print("Received in main")
        data = json.loads(body)
        print(data)

        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product) 
            db.session.commit()
            print('Product Deleted')



channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started consming')

channel.start_consuming()

channel.close()