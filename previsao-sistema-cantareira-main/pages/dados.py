import streamlit as st
import pandas as pd
from st_pages import add_page_title

# Converter dataframe em formatos distintos. Valores permitidos para o
# formato: 'csv', 'parquet', 'json'

@st.cache_data
def converter_df(df, formato):
	if formato == 'csv':
		return df.to_csv().encode('utf-8')
	if formato == 'parquet':
		return df.to_parquet()
	if formato == 'json':
		return df.to_json()

# Carregar dados

@st.cache_data
def carregar_dados():
	return pd.read_excel('SABESP-sistemas_produtores.xlsx')

add_page_title()

st.markdown('''A fonte dos dados do projeto é a [Sabesp](https://mananciais.sabesp.com.br/HistoricoSistemas?SistemaId=0), que disponibiliza dados referentes ao sistemas produtores. É possível ter informações sobre o Nível (m), Volume (hm³), Volume (%), Q Jusante (m³/s), Q Natural (m³/s) e Chuva (mm). De acordo com este mesmo site, temos a definição dos itens disponibilizados: 

* Nível (m): refere-se ao nível da água no reservatório, em metros; 
* Volume (hm³): corresponde ao volume armazenado na represa, em hectômetros cúbicos; 
* Q Natural (m³/s): representa a vazão média diária afluente ao reservatório, em metros cúbicos por segundo, sem considerar as alterações antrópicas; 
* Qjus (m³/s): indica a vazão média diária descarregada, em metros cúbicos por segundo, para a jusante da barragem, ou seja, a quantidade de água liberada que segue pelo rio ou canal após o barramento; 
* Chuva (mm): refere-se à precipitação acumulada nas últimas 24 horas no local do barramento da represa, em milímetros. 

Obtivemos os dados desde 2000 até o primeiro trimestre de 2023, incluindo apenas as represas principais (Jaguari, Jacareí, Atibainha, Cachoeira e Paiva Castro). Abaixo estão os dados de cada represa e os dados agrupados, disponíveis para download.''')

dados_originais = carregar_dados()
st.write(dados_originais)

st.download_button(
	label="Baixar os dados como .csv",
	data=converter_df(dados_originais, 'csv'),
	file_name='dados_represas.csv',
	mime='text/csv'
)

st.download_button(
	label="Baixar os dados como .parquet",
	data=converter_df(dados_originais, 'parquet'),
	file_name='dados_represas.parquet',
	mime='application/octet-stream'
)

st.download_button(
	label="Baixar os dados como .json",
	data=converter_df(dados_originais, 'json'),
	file_name='dados_represas.json',
	mime='application/json'
)

dados_agrupados = dados_originais.groupby(['Data'], as_index=False).sum(numeric_only=True)
st.write(dados_agrupados)

st.download_button(
	label="Baixar os dados como .csv",
	data=converter_df(dados_agrupados, 'csv'),
	file_name='dados_agrupados.csv',
	mime='text/csv'
)

st.download_button(
	label="Baixar os dados como .parquet",
	data=converter_df(dados_agrupados, 'parquet'),
	file_name='dados_agrupados.parquet',
	mime='application/octet-stream'
)

st.download_button(
	label="Baixar os dados como .json",
	data=converter_df(dados_agrupados, 'json'),
	file_name='dados_agrupados.json',
	mime='application/json'
)