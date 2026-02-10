import pymongo
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from datetime import datetime

class ScrapyProjectPipeline:
    
    def open_spider(self, spider):
        #Conexión a MongoDB 
        uri = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
        self.client = pymongo.MongoClient(uri)

        self.db = self.client["carreras_db"]
        self.coleccion=self.db["resultados"]    
        
        #Manejo duplicaods
        self.db.resultados.create_index([("runner_name", 1), ("fecha", 1)], unique=True)
    



    def process_item(self, item, spider):
        adapter = ItemAdapter(item) 
        
        # Valida que el item tenga los campos mínimos 
        if not adapter.get('runner_name') or not adapter.get('finish_time'):
            raise DropItem(f"Item incompleto descartado: {adapter.get('runner_name')}")
        
        # Conversión de tipos y manejo de errores
        try:
            adapter['race_distance'] = float(adapter.get('race_distance', 0))
            
            if isinstance(adapter.get('fecha'), str):
                adapter['fecha'] = datetime.strptime(adapter['fecha'], "%d/%m/%Y")         
        
        except (ValueError, TypeError):
            adapter['race_distance'] = 0.0

        # Duplicados
        try:
            # Insertamos el item convertido a diccionario
            self.coleccion.insert_one(adapter.asdict())
        except pymongo.errors.DuplicateKeyError:
            # si hay duplicado, lo ignoramos
            spider.logger.debug(f"Duplicado detectado y omitido: {adapter['runner_name']}")
            
        return item
    
    def close_spider(self, spider):
        self.client.close()
    