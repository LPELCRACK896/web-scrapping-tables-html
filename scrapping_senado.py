from bs4 import BeautifulSoup, element
import pandas as pd
import requests
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

def cell_info_getter(tag):
    text = getTextInTag(tag)
    if not text: return None
    if not text[-3:]== '...': return text
    if not tag.contents: return text
    if not tag.contents[0].name == 'a': return text
    a_tag = tag.contents[0]
    get_req_expediente = BASE_URL_GET+a_tag.attrs.get('href') 
    response = start_session_and_make_request(LOG_IN_URL, {}, get_req_expediente)
    temp_html = 'temp.html'
    writeHTML(response.text, temp_html)
    return get_full_title(temp_html)

def start_session_and_make_request(login_url, credentials, get_url):
    with requests.session() as s:
        s.post(login_url, credentials)
        r = s.get(get_url)
        return r

def get_full_title(html_page):
    with open(html_page, 'r', encoding='utf8') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        return soup.find('textarea', {'id': 'campos_nota_630'}).text   

def get_project_descrition_from_response(response):
    writeHTML(response.text, 'temp-pagina.html')

def table_scrapper(html_file_name) -> pd.DataFrame:
    with open(html_file_name, 'r', encoding='utf8') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        #DtgExpedientes
        table = soup.find('table', {'id': 'DtgExpedientes'})
        columns = []
        data = []
        contenido = table.contents
        redefined = False
        cont = 0
        while not redefined and not cont>len(table.contents):
            if type(table.contents[cont])==element.Tag:
                if table.contents[cont].name == 'tbody':
                    contenido = table.contents[cont]
                    redefined = True
            cont += 1

        for tag in contenido:
            if type(tag)==element.Tag:
                if tag.attrs:
                    if tag.attrs.get('class'):
                        if 'cabezaTabla' in tag.attrs.get('class') and not columns:
                            columns = [item_in_tag.contents[0] for item_in_tag in tag.contents if type(item_in_tag)==element.Tag]
                        else:
                            data.append([cell_info_getter(child_tag) for child_tag in tag.contents if type(child_tag)==element.Tag])
                else:
                    data.append([cell_info_getter(child_tag) for child_tag in tag.contents if type(child_tag)==element.Tag])
        if columns:
            return pd.DataFrame(data, columns=columns)
            #df.to_excel(excel_file_name, index=False, header=True)
        else:
            return None

def writeXSLS(xlsx_filename: str, df: pd.DataFrame):
    df.to_excel(xlsx_filename, index=False, header=True)

def check_if_next(html_file_name):
    pass

def checi_if_previous(html_file_name):
    pass

def writeHTML(text, filename):
    f = open(filename, "w", encoding='utf-8')
    f.write(text)
    f.close()