import scrapy
from ..items import ScrapyProjectItem
class RaceSpider(scrapy.Spider):
    name = "race"
    EDICIONES = [
        {"anio": 2010, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion--435"},
        {"anio": 2011, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion--603"},
        {"anio": 2012, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion--836"},
        #{"anio": 2013, "url": "https://sansilvestrecoruna.com/edicion-2019/"},
        {"anio": 2014, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-899"},
        {"anio": 2015, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-5000"},
        {"anio": 2016, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-6273"},
        {"anio": 2017, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-7799"},
        {"anio": 2018, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-9310"},
        {"anio": 2019, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-10910"},
        {"anio": 2020, "url": "https://sansilvestrecoruna.com/edicion-2023/"},
        #{"anio": 2020, "url": "https://sansilvestrecoruna.com/edicion-2023/"},
        {"anio": 2021, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-11984"},
        {"anio": 2022, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-13121"},
        {"anio": 2023, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-14359"},
        {"anio": 2024, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-15442"},
        {"anio": 2025, "url": "https://sansilvestrecoruna.com/es/web/resultado/competicion-16683"}
    ]

    def start_requests(self):
        # Iteramos directamente sobre nuestra lista manual
        for edicion in self.EDICIONES:
            yield scrapy.Request(
                url=edicion["url"],
                callback=self.parse,
                meta={'anio': edicion["anio"]} # Pasamos el año para etiquetar los datos
            )

    def parse(self, response):
        anio = response.meta['anio']

        # Localizamos las filas de la tabla de resultados
        rows = response.css('table.table-striped tbody tr')

        for row in rows:
            # Extraemos nombre y apellidos para combinarlos
            nombre = row.css('td.nombre *::text').get('').strip()
            apellidos = row.css('td.apellidos *::text').get('').strip()
            
            # Género basado en el texto de la columna correspondiente
            sexo_raw = row.css('td.get_puesto_sexo_display::text').get('').upper()
            genero = "Masculino" if "M" in sexo_raw else "Femenino"

            item = ScrapyProjectItem()

            item['fecha'] = f"31/12/{anio}"
            item['runner_name'] = f"{nombre} {apellidos}".strip()
            item['finish_time'] = row.css('td.tiempo_display::text').get('').strip()
            item['age_group'] = row.css('td.get_puesto_categoria_display::text').get('').strip()
            item['gender'] = genero
            item['race_distance'] = '7.5'
            item['location'] = 'A Coruña'

            yield item
            
        next_page = response.xpath('//a[contains(text(), "Siguiente") or contains(text(), ">")]/@href').get()
        
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={'anio': anio})