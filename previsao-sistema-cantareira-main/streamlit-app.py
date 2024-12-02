import pandas as pd
import streamlit as st
import datetime as dt
from prophet import Prophet
from prophet.serialize import model_from_json
from plotting_utils import plot_plotly
from st_pages import Page, show_pages

# Configurações da página

st.set_page_config(
	page_title='Previsão de volume do Sistema Cantareira'
)

# Definição das páginas da aplicação

show_pages(
    [
        Page('streamlit-app.py', 'Página inicial', ':house:'),
        Page('pages/dados.py', 'Dados', ':bar_chart:'),
        Page('pages/info-modelo.py', 'Sobre o modelo', ':books:'),
    ]
)

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

# Carregar modelos

@st.cache_data
def carregar_modeloVolProphet():
	with open('modelo-prophet/modelo-volume.json', 'r') as file:
		return model_from_json(file.read())

@st.cache_data
def carregar_modeloChuvaProphet():
	with open('modelo-prophet/modelo-chuva.json', 'r') as file:
		return model_from_json(file.read())

# Carregar dados previstos

@st.cache_data
def carregar_previsaoVolProphet():
	return pd.read_pickle('modelo-prophet/previsao-volume.pkl')

@st.cache_data
def carregar_previsaoChuvaProphet():
	return pd.read_pickle('modelo-prophet/previsao-chuva.pkl')

# Carregar imagens e vídeos

@st.cache_data
def carregar_tutorial(num_tutorial):
	tutorial = open(f'static/tutorial{num_tutorial}.mp4', 'rb')
	return tutorial.read()

# Formata uma data no esquema dia/mês/ano, recebendo como entrada
# um objeto pandas.Timestamp

def formatar_data(pd_data):
	return pd_data.strftime('%m/%Y')
	
# Interface

st.title('Previsão de volume do Sistema Cantareira')

modeloVolProphet = carregar_modeloVolProphet()
previsaoVolProphet = carregar_previsaoVolProphet()
modeloChuvaProphet = carregar_modeloChuvaProphet()
previsaoChuvaProphet = carregar_previsaoChuvaProphet()

st.markdown('''O objetivo principal deste projeto é desenvolver e disponibilizar um modelo de previsão do volume do Sistema Cantareira. Como objetivo secundário, analisamos também o volume de chuva. 

***Observação***: Recomendamos acessar esta página em um ambiente desktop.

Para saber a fonte dos dados e ter acesso aos dados completos, acesse a página "Dados" pelo menu à esquerda. Para ver as análises feitas e o modelo utilizado, acesse a página "Sobre o modelo".''')

# Instruções

st.header('Instruções') 

coluna_esquerda1, coluna_direita1 = st.columns([1, 3])
coluna_esquerda1.markdown('''1. Para ampliar um período específico (*zoom*): com o ícone de lupa selecionado, clique e arraste o intervalo desejado.''')
coluna_direita1.video(carregar_tutorial(1))

coluna_esquerda2, coluna_direita2 = st.columns([1, 3])
coluna_esquerda2.markdown('''2. Para retornar ao nível de *zoom* original, clique duas vezes no gráfico ou clique no ícone de casa.''')
coluna_direita2.video(carregar_tutorial(2))

coluna_esquerda3, coluna_direita3 = st.columns([1, 3])
coluna_esquerda3.markdown('''3. Para navegar no gráfico, clique no ícone à direita da lupa e arraste à esquerda ou direita.''')
coluna_direita3.video(carregar_tutorial(3))

coluna_esquerda4, coluna_direita4 = st.columns([1, 3])
coluna_esquerda4.markdown('''4. Você pode selecionar períodos específicos de 1 semana, 1 mês, 6 meses e 1 ano.''')
coluna_direita4.video(carregar_tutorial(4))

coluna_esquerda5, coluna_direita5 = st.columns([1, 3])
coluna_esquerda5.markdown('''5. Você também pode navegar usando o mini-gráfico na parte inferior.''')
coluna_direita5.video(carregar_tutorial(5))

# Gráfico de volume

st.header('Volume (em hm³)')

modoCorVol = st.radio('Selecione o modo de cores:', ('Claro', 'Escuro'), horizontal=True, key='modoCorVol')
print(f'Modo cor selecionado: {modoCorVol}')

st.plotly_chart(plot_plotly(modeloVolProphet, previsaoVolProphet, xlabel='Data', ylabel='Volume (hm³)', colorScheme=modoCorVol), use_container_width=True)

st.caption('''<div style='text-align: center;'>Em preto (ou branco, no modo escuro) estão os dados observados, em azul estão os dados previstos pelo modelo. A área azul acima e abaixo dos pontos representa o intervalo de confiança da previsão.</div><br>''', unsafe_allow_html=True)

dadosPrevisaoVol = previsaoVolProphet[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
vol_csv = converter_df(dadosPrevisaoVol, 'csv')
vol_parquet = converter_df(dadosPrevisaoVol, 'parquet')
vol_json = converter_df(dadosPrevisaoVol, 'json')

st.markdown('''Clique nos botões abaixo para salvar as previsões em arquivo. As colunas `ds`, `yhat`, `yhat_lower` e `yhat_upper` representam, respectivamente, a data, o volume previsto, o limite inferior do intervalo de confiança para a previsão e o limite superior do intervalo de confiança para a previsão. Para obter os valores observados, acesse a página "Dados" pelo menu à esquerda.''')

st.download_button(
	label="Baixar os dados como .csv",
	data=vol_csv,
	file_name='dadosPrevisaoVol.csv',
	mime='text/csv'
)

st.download_button(
	label="Baixar os dados como .parquet",
	data=vol_parquet,
	file_name='dadosPrevisaoVol.parquet',
	mime='application/octet-stream'
)

st.download_button(
	label="Baixar os dados como .json",
	data=vol_json,
	file_name='dadosPrevisaoVol.json',
	mime='application/json'
)

# Gráfico de chuva

st.header('Chuva (em mm)')

modoCorChuva = st.radio('Selecione o modo de cores:', ('Claro', 'Escuro'), horizontal=True, key='modoCorChuva')

st.plotly_chart(plot_plotly(modeloChuvaProphet, previsaoChuvaProphet, xlabel='Data', ylabel='Chuva (mm)', colorScheme=modoCorChuva), use_container_width=True)

st.caption('''<div style='text-align: center;'>Em preto (ou branco, no modo escuro) estão os dados observados, em azul estão os dados previstos pelo modelo. A área azul acima e abaixo dos pontos representa o intervalo de confiança da previsão.</div><br>''', unsafe_allow_html=True)

dadosPrevisaoChuva = previsaoVolProphet[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
chuva_csv = converter_df(dadosPrevisaoChuva, 'csv')
chuva_parquet = converter_df(dadosPrevisaoChuva, 'parquet')
chuva_json = converter_df(dadosPrevisaoChuva, 'json')

st.markdown('''Clique nos botões abaixo para salvar as previsões em arquivo. As colunas `ds`, `yhat`, `yhat_lower` e `yhat_upper` representam, respectivamente, a data, o volume de chuva previsto, o limite inferior do intervalo de confiança para a previsão e o limite superior do intervalo de confiança para a previsão. Para obter os valores observados, acesse a página "Dados" pelo menu à esquerda.''')

st.download_button(
	label="Baixar os dados como .csv",
	data=chuva_csv,
	file_name='dadosPrevisaoChuva.csv',
	mime='text/csv'
)

st.download_button(
	label="Baixar os dados como .parquet",
	data=chuva_parquet,
	file_name='dadosPrevisaoChuva.parquet',
	mime='application/octet-stream'
)

st.download_button(
	label="Baixar os dados como .json",
	data=chuva_json,
	file_name='dadosPrevisaoChuva.json',
	mime='application/json'
)