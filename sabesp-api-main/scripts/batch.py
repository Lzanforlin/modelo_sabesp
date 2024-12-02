import sys
import json
import requests
import pandas as pd
from scraper import raspar_sistemas

pd.set_option('display.max_columns', None)

MODO_OUTPUT = ['w', 'a']
SISTEMAS_SABESP = ['cantareira', 'alto_tiete', 'guarapiranga','cotia', 'rio_grande', 'rio_claro', 'sao_lourenco']
ID_PROJETO_GCP = 'sabesp-dados'

data_inicio = sys.argv[1] 
data_fim = sys.argv[2]
modo_output = sys.argv[3].lower()
dir_output = sys.argv[4]
sistemas_input = sys.argv[5].split(',')

if modo_output not in MODO_OUTPUT:
	modo_output = 'a'
if sistemas_input == ['todos']:
	sistemas_input = SISTEMAS_SABESP

raspar_sistemas(data_inicio, data_fim, modo_output, dir_output, sistemas_input)