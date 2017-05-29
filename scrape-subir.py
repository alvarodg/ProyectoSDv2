import scrapy
from celery import Celery
from celery.schedules import crontab, timedelta
from scrapy.crawler import CrawlerProcess
import random

class StackObjeto(scrapy.Item):
    tags = scrapy.Field()

class StackSpider(scrapy.Spider):
    name = "stack"

    def start_requests(self): 
        random.seed()
        pagina = random.randint(1, 100000)
        urls = [
            "http://stackoverflow.com/questions?page=" + str(pagina) + "&pagesize=50&sort=newest"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        preguntas = response.xpath('//div[@class="summary"]/div')

        for pregunta in preguntas:
            obj = StackObjeto()
            obj['tags'] = pregunta.xpath(
                'a[@class="post-tag"]/text()').extract()
            yield obj

app = Celery(backend="rpc://")

# Configuración de tareas periódicas
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	# Parámetros de sender.add_periodic_class: 
	# (periodo, nombre_funcion.s(parametro), name=nombre_cualquiera)
	sender.add_periodic_task(5.0, empezar_crawl.s(), name='scrape cada 5')
	sender.add_periodic_task(20.0, procesar_subir.s(), name='subir cada 20')
	"""sender.add_periodic_task(
		crontab(hour=7, minute=30, day_of_week=1),
		empezar_crawl.s(),
	)"""


app.conf.timezone = 'Europe/London'
# Necesario para que no se intente reiniciar el twisted reactor
app.conf.worker_max_tasks_per_child = 1

# Tarea que se va a ejecutar
@app.task(name = "procesa")
def empezar_crawl():
	print("funcionando")
	process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
			'FEED_FORMAT' : 'json',
			'FEED_URI' : 'resultado.txt'
        })
	process.crawl(StackSpider)
	process.start()

@app.task(name = "sube")
def procesar_subir():
	try:
		with open('resultado.txt', 'r') as datos:
			with open('r_procesado.txt', 'w+') as procesado:
				for line in datos:
					if line != '][\n' and line != "{\"tags\": []}\n" and line != "{\"tags\": []},\n":

						procesado.write(line)

		with open('r_procesado.txt', 'r') as procesado:
			"""array = pandas.DataFrame(data=numpy.array([0, 0, 0, 0, 0, 0]), 
					index=['Row1'],
					columns=['java', 'C#', 'javascript', 'python', 'html', 'php'],
					)"""
			array = pandas.DataFrame({
					'java' : 0,
		 			'c#' : 0,
					'javascript' : 0,
					'python' : 0,
					'html' : 0,
					'php' : 0
			}, index=['Row1'])
			for line in procesado:
				if '\"java\"' in line: 
					array.set_value('Row1', 'java', array.loc['Row1', 'java']+1)
				if 'c#' in line: 
					array.set_value('Row1', 'c#', array.loc['Row1', 'c#']+1)
				if 'javascript' in line: 
					array.set_value('Row1', 'javascript', array.loc['Row1', 'javascript']+1)
				if 'python' in line: 
					array.set_value('Row1', 'python', array.loc['Row1', 'python']+1)
				if 'html' in line: 
					array.set_value('Row1', 'html', array.loc['Row1', 'html']+1)
				if 'php' in line: 
					array.set_value('Row1', 'php', array.loc['Row1', 'php']+1)

			dropbox_subida_parap.delay(array.to_json())

		os.remove('resultado.txt')

	except IOError:
		print("Aún no hay archivo que subir.")
			
