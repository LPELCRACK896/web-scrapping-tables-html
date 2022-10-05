from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 
import pandas as pd
from constants import *

#Opciones de navegaciones
def get_all_pages():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')
    driver_path = './chromedriver.exe'

    driver = webdriver.Chrome(driver_path, chrome_options=options)

    driver.get(ALTERNATIVE_URl_START)
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#imgBtnIngresoAlternativo'))).click()
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="DgColecciones"]/tbody/tr[2]/td[1]/a'))).click()

    previous =  None
    cont = 0
    try:
        previous  = driver.find_element('id', 'btnRestaPaginacion')
        cont = 1
    except:
        previous =  None

    while previous:
        WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnRestaPaginacion"]'))).click()
        try:
            previous  = driver.find_element('id', 'btnRestaPaginacion')
            cont += 1
        except:
             previous =  None
    total_paginas = [driver.page_source]
    next =  None
    cont = 0
    try:
        next  = driver.find_element('id', 'btSumaPaginacion')
        cont = 1
    except:
        next = None

    while next:

        try:
            next  = driver.find_element('id', 'btSumaPaginacion')
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btSumaPaginacion"]'))).click()
            cont += 1
        except:
            next =  None
        if total_paginas:
            if driver.page_source != total_paginas[-1]:
                total_paginas.append(driver.page_source)
            else:
                next = None
        else:
            total_paginas.append(driver.page_source)
    driver.close()
    return total_paginas