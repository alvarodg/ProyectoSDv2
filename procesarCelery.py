from celery import Celery
import Procesar
import dropboxSubidaGrafica

app3 = Celery('procesarCelery', broker="pyamqp://guest@localhost//")


@app3.task(name='worker3', no_ack=True)
def procesar_excel(data):
    data_processed = Procesar.procesar(data)
    dropboxSubidaGrafica.dropbox_grafica.apply_async(data_processed)
