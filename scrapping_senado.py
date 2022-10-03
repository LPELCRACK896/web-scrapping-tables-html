from bs4 import BeautifulSoup, element
import pandas as pd
import requests
import pruebas
from constants import *

__author__ = 'Forbidden'
__copyright__ = 'Copyright 2022, Scrapping Senado'
__credits__ = ['Forbidden']
__license__ = '{None License}'
__version__ = '1.0.0'
__maintainer__ = 'Fordidden'
__email__ = 'luispedev@gmail.com'
__status__ = 'Available and ready.'


tildesParser = lambda text : text.replace('&#243;', 'ó').replace('&#237;', 'í').replace('&#218;', 'Ú').replace('&#225;', 'á').replace('&#250;', 'ú') 

def getTextInTag(content):
    if not type(content) == element.Tag: return content
    if not content.contents: return ''
    if len(content.contents)!= 1: 
        print("Tag contiene mas de un hijo")
        return None
    
    content = content.contents[0]
    if type(content)== element.Tag: return getTextInTag(content)
    elif type(content)== element.NavigableString: return content
    else:
        print("Item de tipo inesperado")
        return None

def start_session_and_make_request(login_url, credentials, get_url):
    with requests.session() as s:
        s.post(login_url, credentials)
        r = s.get(get_url)
        return r

def get_full_title(tag):
    pass

def get_project_descrition_from_response(response):
    pruebas.writeHTML(response.text, 'temp-pagina.html')

def table_scrapper(pagina):    
    with open(pagina, 'r', encoding='utf8') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        #DtgExpedientes
        table = soup.find('table', {'id': 'DtgExpedientes'})
        columns = []
        data = []
        for tag in table.contents:
            if type(tag)==element.Tag:
                if tag.attrs:
                    if tag.attrs.get('class'):
                        if 'cabezaTabla' in tag.attrs.get('class') and not columns:
                            columns = [item_in_tag.contents[0] for item_in_tag in tag.contents if type(item_in_tag)==element.Tag]
                        elif 'linea_gris' in tag.attrs.get('class'):
                            data.append([getTextInTag(child_tag) for child_tag in tag.contents if type(child_tag)==element.Tag])
        if columns:
            df = pd.DataFrame(data, columns=columns)
            df.to_excel('otro_excel.xlsx', index=False, header=True)

def writeHTML(text, filename):
    f = open(filename, "w", encoding='utf-8')
    f.write(text)
    f.close()

