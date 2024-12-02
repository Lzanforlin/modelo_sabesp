import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json

# Importar dados
df_SABESP = pd.read_excel('../SABESP-sistemas_produtores.xlsx')

# Agrupar dados para obter previsões do Sistema Cantareira como um todo
dfSabesp = df_SABESP.groupby(['Data'], as_index=False).sum(numeric_only=True)

# Criar dataframes para utilizar com o Prophet
dfProphet = pd.DataFrame()
dfProphet['ds'] = dfSabesp['Data']
dfProphet['y'] = dfSabesp['Volume (hm³)']

dfProphet2 = pd.DataFrame()
dfProphet2['ds'] = dfSabesp['Data']
dfProphet2['y'] = dfSabesp['Chuva (mm)']

# Ajustar modelos
modeloVol = Prophet()
modeloVol.fit(dfProphet)
modeloChuva = Prophet()
modeloChuva.fit(dfProphet2)

# Gerar modelos
DataFrameFuturoVol = modeloVol.make_future_dataframe(periods=730, freq = 'd')
previsaoVol = modeloVol.predict(DataFrameFuturoVol)
DataFrameFuturoChuva = modeloChuva.make_future_dataframe(periods=730, freq = 'd')
previsaoChuva = modeloChuva.predict(DataFrameFuturoChuva)

# Salvar modelos
with open('modelo-volume.json', 'w') as file:
	file.write(model_to_json(modeloVol))

with open('modelo-chuva.json', 'w') as file:
	file.write(model_to_json(modeloChuva))

# Salvar dataframes gerado pelo modelo
previsaoVol.to_pickle('previsao-volume.pkl')
previsaoChuva.to_pickle('previsao-chuva.pkl')