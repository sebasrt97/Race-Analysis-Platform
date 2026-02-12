import pymongo
import json
from itemadapter import ItemAdapter
from datetime import datetime

class MongoImporter:
    def __init__(self):
        # Configuración de la base de datos
        self.uri = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
        self.db_name = "carreras_db"
        self.collection_name = "resultados"

    def importar_desde_json(self, nombre_archivo='../edMongo.json'):

        #  Conexión y configuración inicial
        client = pymongo.MongoClient(self.uri)
        db = client[self.db_name]
        coleccion = db[self.collection_name]
        
        # Crear índice único para evitar duplicados
        coleccion.create_index([("runner_name", 1), ("fecha", 1)], unique=True)

        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                exitos = 0
                duplicados = 0

                for item in datos:
                    adapter = ItemAdapter(item)
                    
                    # Validación mínima
                    if not adapter.get('runner_name') or not adapter.get('finish_time'):
                        continue

                    # Limpieza y conversión de datos
                    try:
                        # Distancia a float
                        adapter['race_distance'] = float(adapter.get('race_distance', 0))
                        
                        # Fecha a objeto datetime
                        fecha_str = adapter.get('fecha')
                        if isinstance(fecha_str, str):
                            adapter['fecha'] = datetime.strptime(fecha_str, "%d/%m/%Y")
                        
                        # Inserción en MongoDB
                        coleccion.insert_one(adapter.asdict())
                        exitos += 1

                    except pymongo.errors.DuplicateKeyError:
                        duplicados += 1
                    except Exception as e:
                        print(f"Error procesando registro: {e}")

                print("--- Resumen de Importación ---")
                print(f"Registros nuevos: {exitos}")
                print(f"Duplicados omitidos: {duplicados}")
                print(f"Total en colección: {coleccion.count_documents({})}")

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {nombre_archivo}")
        except json.JSONDecodeError:
            print(f"Error: El archivo {nombre_archivo} no tiene un formato JSON válido.")
        finally:
            client.close()
            print("Conexión a MongoDB cerrada.")

# --- Ejecución del script ---
if __name__ == "__main__":
    importer = MongoImporter()
    importer.importar_desde_json()