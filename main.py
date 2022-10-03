from scrapping_senado import *
from constants import *

response = start_session_and_make_request(LOG_IN_URL,  {}, COLECCIONES_URL)
writeHTML(response.text)