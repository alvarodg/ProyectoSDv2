from celery import Celery
import Dropbox

app4 = Celery('dropboxSubidaGrafica', broker="pyamqp://guest@localhost//")


@app4.task(name='worker4', no_ack=True)
def dropbox_grafica(data):
    Dropbox.subidaGrafica(data)
