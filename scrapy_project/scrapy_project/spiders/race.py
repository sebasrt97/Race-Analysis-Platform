import scrapy

class RaceSpider(scrapy.Spider):
    name = "race"
    allowed_domains = ["sansilvestrecoruna.com"]
    start_urls = ["https://sansilvestrecoruna.com/es/web/resultado/competicion-16683?page=1"]

    def parse(self, response):

        rows = response.css('table.table-striped tbody tr')

        for row in rows:
            yield {
                'runner_name': f"{row.css('td.nombre *::text').get('').strip()} {row.css('td.apellidos *::text').get('').strip()}",
                'finish_time': row.css('td.tiempo_display::text').get('').strip(),
                'age_group': row.css('td.get_puesto_categoria_display::text').get('').strip(),
                'gender': "Masculino" if "M" in row.css('td.get_puesto_sexo_display::text').get('').upper() else "Femenino",
                'race_distance': '7.5',
                'location': 'A Coruña'
            }

        #Iterar sobre la paginación
        next_page = response.xpath('//a[contains(text(), "Siguiente")]/@href').get()
        
        if next_page:
            yield response.follow(next_page, callback=self.parse)