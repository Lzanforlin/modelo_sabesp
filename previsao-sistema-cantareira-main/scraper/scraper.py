from os import listdir
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Diretório contendo o WebDriver
WEBDRIVER_DIR = 'webdriver'

# URL da página
URL = 'https://mananciais.sabesp.com.br/HistoricoSistemas?SistemaId=0'

# Retorna o caminho do WebDriver, assumindo que esteja no diretório
# especificado em WEBDRIVER_DIR
def caminho_driver():
	return WEBDRIVER_DIR + '/' + listdir(WEBDRIVER_DIR)[0]

# Interage com a página para selecionar os dados desde o início
# dos registros
def selecionar_inicio(driver):
	return None

# Interage com a página para selecionar os dados referentes ao
# sistema Cantareira e retorna o elemento da página contendo os dados
def dados_cantareira(driver):
	return None

# Salva os dados obtidos em arquivo
def salvar_dados(dados):
	return None

options = Options()
options.add_argument('--headless')
service = Service(executable_path=caminho_driver())

driver = webdriver.Firefox(options=options, service=service)
driver.get(URL)

selecionar_inicio(driver)
dados = dados_cantareira(driver)
salvar_dados(dados)

driver.quit()