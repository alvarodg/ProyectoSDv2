from celery import Celery
import dropboxBajada
from Dropbox import subida
import matplotlib.pyplot

app1 = Celery('dropboxSubidaParaProcesar', broker="pyamqp://guest@localhost//")


@app1.task(name='worker1', no_ack=True)
def dropbox_subida_parap(data):
    subida(data)
    dropboxBajada.dropbox_bajada.apply_async()

