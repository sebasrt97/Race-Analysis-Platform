🏃‍♂️ Race Analysis Dashboard
Autores: Sebastian Ramos y Gabriel Tenreiro

Este proyecto es una solución integral para la extracción, procesamiento y visualización de datos de carreras populares. Combina el uso de Scrapy para el web scraping, MongoDB para el almacenamiento de datos y Streamlit para la generación de un dashboard interactivo de análisis de resultados.

📊 Modelo de Datos (ER)
El proyecto utiliza un modelo Entidad-Relación normalizado para asegurar la integridad y evitar la redundancia de la información:

Corredor: Almacena el identificador único (id_corredor), nombre y género.

Carrera: Contiene los detalles del evento como fecha, ubicación y distancia total.

Participación: Entidad puente que vincula a un corredor con una carrera, registrando el tiempo final y el grupo de edad.

🛠️ Requisitos e Instalación
Para ejecutar este proyecto, es necesario instalar las siguientes librerías de Python:


streamlit: Interfaz del dashboard.


pandas: Manipulación y limpieza de datos.


plotly: Generación de gráficos interactivos.

scrapy: Extracción de datos web.

pymongo: Conexión y gestión de la base de datos MongoDB.

🚀 Guía de Ejecución
Siga estos pasos en orden para poner en marcha el ecosistema completo:

1. Web Scraping con Scrapy
Extraiga los datos de las carreras utilizando el spider configurado. Los campos capturados incluyen la fecha, nombre del corredor, tiempo de finalización, grupo de edad, género, distancia y ubicación.

Bash
# Dentro del directorio del proyecto Scrapy
scrapy crawl <nombre_del_spider> -o edMongo.json
La configuración incluye un USER_AGENT personalizado y un DOWNLOAD_DELAY de 1 segundo para garantizar una extracción respetuosa.

2. Importación a MongoDB
Procese el archivo JSON generado y cargue los datos en la base de datos NoSQL. El script de importación limpia los datos, convierte las distancias a formato numérico y las fechas a objetos datetime.

Bash
python pipelines.py
Configuración de DB: Se conecta a mongodb://admin:admin123@localhost:27017/.

Base de datos: carreras_db | Colección: resultados.

Evita duplicados: Utiliza un índice único basado en runner_name y fecha.

3. Visualización en el Dashboard
Inicie la aplicación interactiva de Streamlit para analizar los resultados:

Bash
streamlit run scrapy_project/scrapy_project/dashboard.py
📈 Funcionalidades del Dashboard
La aplicación web permite filtrar por evento y género para explorar los siguientes módulos:

Estadísticas Generales:

Métricas de mejor tiempo, tiempo medio y total de corredores.

Histogramas de distribución de tiempos y gráficos de caja (boxplots) por grupo de edad.

Curva de densidad de finalización comparando géneros.

Buscador Individual:

Análisis personalizado por nombre de corredor.

Cálculo automático de la posición general y el ritmo medio en min/km.

Gráfico comparativo de la posición del corredor respecto al resto de participantes.

Hall of Fame:

Tabla con el Top 10 de atletas con mejores tiempos.

Gráfico de barras comparativo de los líderes de la carrera.