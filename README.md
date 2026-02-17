🏃‍♂️ San Silvestre Coruña Race Analysis Platform
Autores: Sebastian Ramos y Gabriel Tenreiro

Este proyecto consiste en una plataforma integral para la captura, almacenamiento y análisis de resultados de la carrera San Silvestra en A Coruña.
 El sistema automatiza el flujo de datos desde la extracción web mediante Scrapy, el almacenamiento en una base de datos NoSQL con MongoDB, hasta la visualización de métricas avanzadas en un dashboard de Streamlit y un cuaderno de análisis de datos.

📊 Descripción del Proyecto
La plataforma permite procesar y visualizar el rendimiento de los corredores.

🛠️ Tecnologías y Librerías
El stack tecnológico utilizado para este desarrollo incluye las siguientes librerías de Python:

Extracción: scrapy.

Base de Datos: pymongo (MongoDB).

Visualización: streamlit, plotly y matplotlib.

Procesamiento: pandas y datetime.

⚙️ Configuración del Entorno (Conda)
Para replicar el entorno de desarrollo y evitar conflictos de versiones, ejecute el siguiente script en su terminal:

Bash
# 1. Crear el entorno con Python 3.12
conda create --name sansilvestre python=3.12 -y
conda activate sansilvestre

# 2. Instalar el stack tecnológico base
# Incluimos scipy para corregir el error en la Curva de Densidad
conda install -c conda-forge streamlit pandas plotly scrapy pymongo matplotlib scipy ipykernel -y

# 3. Parche de compatibilidad para visualización
# Corrige el error: ModuleNotFoundError: No module named 'altair.vegalite.v4'
pip install altair==4.2.2


🚀 Guía de Ejecución
1. Web Scraping
Para iniciar la recolección de datos y generar el archivo de salida JSON, sitúese en la carpeta del proyecto Scrapy y ejecute:

Bash
scrapy crawl race -O edMongo.json
Este comando captura campos como runner_name, finish_time, age_group, gender, race_distance, location y fecha.

2. Importación a Base de Datos
Procese el archivo JSON para limpiar los datos y cargarlos en MongoDB:

Bash
python pipelines.py
El sistema utiliza la URI mongodb://admin:admin123@localhost:27017/ para conectar con la base de datos carreras_db.

3. Dashboard de Visualización
Lanze la interfaz gráfica interactiva:

Bash
streamlit run scrapy_project/dashboard.py
📂 Estructura del Proyecto
Basado en los componentes del repositorio:

📂 scrapy_project/: Directorio principal del scraper.

items.py: Definición de los campos a extraer.

pipelines.py: Lógica de limpieza e inserción en MongoDB.

settings.py: Configuración de comportamiento del bot y cortesía.

dashboard.py: Aplicación Streamlit para la visualización de resultados.

edMongo.json: Archivo generado por el scraper con los datos brutos.

📄 analisis.ipynb: Cuaderno de Jupyter para análisis estadístico y visualización con Matplotlib.

📄 diagrama.md / diagrama_er.jpg: Documentación del modelo lógico de datos.

📄 requirements.txt: Lista de dependencias del proyecto.