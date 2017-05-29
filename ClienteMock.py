import pandas
import numpy
from dropboxSubidaParaProcesar import dropbox_subida_parap

array = pandas.DataFrame(data=numpy.array([[3, 2, 2, 1, 5, 3]]),
                         columns=['java', 'C#', 'javascript', 'python', 'html', 'php'],
                         index=['Row1'])

dropbox_subida_parap.apply_async()
