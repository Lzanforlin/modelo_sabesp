import sys
import json
import requests
import pandas as pd

pd.set_option('display.max_columns', None)

MODO_OUTPUT = ['w', 'a']
SISTEMAS = {
'cantareira': 0,
'alto_tiete': 1,
'guarapiranga': 2,
'cotia': 3,
'rio_grande': 4,
'rio_claro': 5,
'sao_lourenco': 17
}
ID_PROJETO_GCP = 'sabesp-dados'

def raspar_sistemas(data_inicio, data_fim, modo_output, dir_output, sistemas_input):
	include_header = False if modo_output == 'a' else True
	
	print(f'Iniciando raspagem de {data_inicio} a {data_fim} no modo {modo_output} no diretório {dir_output}')
	
	for sistema in sistemas_input:
		url_api = f'https://mananciais.sabesp.com.br/api/Mananciais/RepresasSistemasNivel/{data_inicio}/{data_fim}/{SISTEMAS[sistema]}'
		req = requests.get(url_api, verify=False)
		dados_json = None
		
		if req.status_code == 200:
			print(f'API da SABESP para o sistema {sistema} acessada com sucesso')
			dados_json = json.loads(req.text)
			
			objs_reserv = dados_json['ReturnObj']['ListaDados']
			df_reserv = pd.DataFrame(data={'Data': [], 'Nível': [], 'Volume (hm³)': [], 'Volume (%)': [], 'Chuva (mm)': [], 'Vazão natural (m³/s)': [], 'Vazão a jusante (m³/s)': [], 'Reservatório': []})
			for dia in objs_reserv:
				for n in range(len(dia['Dados'])):
					dados = dia['Dados'][n]
					if not dados:
						continue
					v_natural = ''
					if dia['Qnat'][n]:
						v_natural = dia['Qnat'][n]['VazaoNatural']
					data = dados['Data'].split('T')[0]
					df_reserv.loc[len(df_reserv)] = [data, dados['Nivel'], dados['VolumeOperacional'], dados['VolumePorcentagem'], dados['Chuva'], v_natural, dados['QJusante'], dados['Nome']]
			
			print(f'Dados dos reservatórios do sistema {sistema} obtidos com sucesso')
			path = f'{dir_output}/{sistema}_reservatorios.csv'
			df_reserv.to_csv(path, index=False, mode=modo_output, header=include_header)
			print(f'Dados dos reservatórios do sistema {sistema} salvos com sucesso em {path}')
			
			objs_sistema = dados_json['ReturnObj']['ListaDadosSistema']
			df_sistema = pd.DataFrame(data={'Data': [], 'Volume (hm³)': [], 'Volume (%)': [], 'Chuva (mm)': [], 'Vazão natural (m³/s)': [], 'Vazão a jusante (m³/s)': []})
			
			if objs_sistema:
				for obj in objs_sistema:
					dados = obj['objSistema']
					data = dados['Data'].split('T')[0]
					df_sistema.loc[len(df_sistema)] = [data, dados['VolumeOperacionalHm3'], dados['VolumePorcentagem'], dados['Precipitacao'], dados['VazaoNatural'], dados['VazaoJusante']]
			else:
				df_sistema = df_reserv.copy()
				df_sistema.drop(['Nível'], axis=1, inplace=True)
				df_sistema.drop(['Reservatório'], axis=1, inplace=True)
			
			print(f'Dados do sistema {sistema} obtidos com sucesso')
			path = f'{dir_output}/{sistema}.csv'
			df_sistema.to_csv(path, index=False, mode=modo_output, header=include_header)
			print(f'Dados do sistema {sistema} salvos com sucesso em {path}')
		else:
			print(f'Acesso à API da SABESP para o sistema {sistema} falhou com status {req.status_code}')
		print('---------------------------------------------------')