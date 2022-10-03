from scrapping_senado import *
from constants import *

html_file_name = 'pagina.html'
xlsx_file_name = 'pruebas2.xlsx'

response = start_session_and_make_request(LOG_IN_URL,  {}, COLECCIONES_URL)
writeHTML(response.text, html_file_name)
df = table_scrapper(html_file_name)
writeXSLS('resultados.xlsx', df)