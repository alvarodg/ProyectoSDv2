import dropbox
import pendulum
import threading
import os
import pandas

token = "kvbe4Epe2OAAAAAAAAAACFLOXRE34frCMWlvINIBHhfGehOAifIhED4gxvvVfhyU"
dbx = dropbox.Dropbox(token)


def subida(newdata):
    now = pendulum.now('Europe/Madrid')
    newdata = pandas.read_json(newdata)
    writer = pandas.ExcelWriter('myDataFrame.xlsx')
    newdata.to_excel(writer, 'DataFrame')
    writer.save()
    with open('myDataFrame.xlsx', 'rb') as f:
        data = f.read()
    fname = "/ParaProcesar/Datos_" + now.isoformat() + ".xlsx"
    response = dbx.files_upload(data, fname, mute=True)
    os.remove('myDataFrame.xlsx')
    print("uploaded2:", response)


def bajar():
    bajar.mutex = threading.Lock()
    bajar.mutex.acquire()
    path = '/ParaProcesar'
    array = dbx.files_list_folder(path).entries
    if array[0] is not None:
        dbx.files_download_to_file(array[0].name, path + '/' + array[0].name)
        file = pandas.ExcelFile(array[0].name)
        data = file.parse('DataFrame')
        dbx.files_delete(path + '/' + array[0].name)
        bajar.mutex.release()
        os.remove(array[0].name)
        return data
    else:
        bajar.mutex.release()
        return None


def subidaGrafica(data):
    Month = pendulum.now('Europe/Madrid')
    print("Subiendo")
    fname = "/Procesado/Datos_" + Month.format('YYYY-MM', formatter='alternative') + ".png"
    response = dbx.files_upload(data, fname, mute=True)
    print("uploaded2:", response)


"""def bajarArchivoDatos():
    bajarArchivoDatos.mutex2 = threading.Lock()
    bajarArchivoDatos.mutex2.acquire()
    path = '/Procesado'
    array = dbx.files_list_folder(path).entries
    if array[0] is not None:
        dbx.files_download_to_file(array[0].name, path + '/' + array[0].name)
        with open(array[0].name, 'rb') as f:
            data = f.read()
        bajarArchivoDatos.mutex.release()
        os.remove(array[0].name)
        return data
    else:
        bajarArchivoDatos.mutex.release()
        return None"""

