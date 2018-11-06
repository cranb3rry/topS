	# #!/usr/bin/env python
	# import pika

	# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	# channel = connection.channel()


	# channel.queue_declare(queue='hello')

	# channel.basic_publish(exchange='',
	#                       routing_key='hello',
	#                       body='Hello World!')
	# print(" [x] Sent 'Hello World!'")
	# connection.close()


import asyncio
from aio_pika import connect, Message


async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    # Sending the message
    await channel.default_exchange.publish(
        Message(b'Hello World!'),
        routing_key='hello',
    )

    print(" [x] Sent 'Hello World!'")

    await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))