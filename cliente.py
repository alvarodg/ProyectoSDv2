from time import sleep

import pika

from tutorial import extraccion


# Modificar esto para realizar la transferencia de archivos
for i in range(0, 5):
    result = extraccion.ext.delay()
    sleep(2)

message = result.get()
