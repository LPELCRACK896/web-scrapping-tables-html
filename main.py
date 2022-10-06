from scrapping_senado import *
from constants import *
from explore_all_pages_sel import *
import pandas as pd

__author__ = "fualp-dev"
__copyright__ = "Copyright 2022, The Fualp Dev"
__credits__ = ["fualp-dev"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "fualp-dev"
__email__ = "luispedev@gmail.com"
__status__ = "Finished"

html_file_name = 'pagina.html'
xlsx_file_name = 'pruebas2.xlsx'
df = pd.DataFrame()

all_pages = get_all_pages() #Llamada a la funcion selenium que extrae todas las paginas con las tablas 
#response = start_session_and_make_request(LOG_IN_URL,  {}, COLECCIONES_URL)
print("Termina scan de paginas html")
print('Total paginas')
print(len(all_pages))
cont= 1

dfs = []
cont = 1
total = len(all_pages)
for page in all_pages:
    writeHTML(page, html_file_name)
    dfs.append(table_scrapper(html_file_name))
    print(f"({cont}/{total}). Pagina añadida a lis de dataframes")
    cont += 1 

print('Uniendo dataframes...')
dff = pd.concat(dfs)
print("Todos los datos fueron llevado al dataframe\nComienza transformacion a excel.")
writeXSLS('resultados.xlsx', dff) 