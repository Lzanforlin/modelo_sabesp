import pandas as pd
from datetime import date, timedelta
from scraper import raspar_sistemas

SISTEMAS_SABESP = ['cantareira', 'alto_tiete', 'guarapiranga','cotia', 'rio_grande', 'rio_claro', 'sao_lourenco']
DIR_DADOS = '../dados'

data_hoje = date.today()

for sis in SISTEMAS_SABESP:
	df = pd.read_csv(f'{DIR_DADOS}/{sis}.csv')
	df.sort_values(by=['Data'], ascending=False, inplace=True)
	mais_recente = pd.to_datetime(df.head(1)['Data']).dt.date.iloc[0]
	
	if mais_recente < data_hoje:
		data_inicio = mais_recente + timedelta(days=1)
		print(f'Dados do sistema {sis} estão desatualizados. Última atualização em {mais_recente}. Extrair dados de {data_inicio} a {data_hoje}')
		raspar_sistemas(data_inicio, data_hoje, 'a', DIR_DADOS, [sis])
	else:
		print(f'Dados do sistema {sis} estão atualizados')
		continue