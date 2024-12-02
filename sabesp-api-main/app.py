from flask import Flask
from flask_restx import Api, Resource, fields
import pandas as pd
from datetime import date

DIR_DADOS = 'dados'
SISTEMAS = ['cantareira', 'alto_tiete', 'guarapiranga','cotia', 'rio_grande', 'rio_claro', 'sao_lourenco']

app = Flask(__name__)
app.config['RESTX_MASK_SWAGGER'] = False
app.config['ERROR_404_HELP'] = False

api = Api(
    app,
    version="1.0",
    title="API SABESP",
    description="API que disponibiliza os dados de reservatórios e sistemas da SABESP, atualizados diariamente. A verificação de novos dados ocorre, aproximadamente, às 09:00, 10:00, 15:00 e 20:00 no horário de Brasília."
)

ns_sis = api.namespace("sistemas", description="Dados de sistemas")
ns_res = api.namespace("reservatorios", description="Dados de reservatórios")

sistema = api.model(
    "Sistema",
    {
        "Data": fields.Date(description="Data do registro", example="2000-12-31"),
        "Volume (hm³)": fields.Float(description="Volume armazenado, em hectômetros cúbicos", example=120.0),
        "Volume (%)": fields.Float(description="Volume armazenado, em percentual do volume total", example=50.5),
        "Chuva (mm)": fields.Float(description="Precipitação acumulada das últimas 24 horas, em milímetros", example=10.0),
        "Vazão natural (m³/s)": fields.Float(description="Vazão média diária afluente, em metros cúbicos por segundo", example=20.8),
        "Vazão a jusante (m³/s)": fields.Float(description="Vazão média diária descarregada, em metros cúbicos por segundo", example=17.2),
    },
)

reservatorio = api.model(
    "Reservatório",
    {
        "Data": fields.Date(description="Data do registro", example="2000-12-31"),
        "Nível": fields.Float(description="Indica o nível de água no reservatório, em metros", example=20.0),
        "Volume (hm³)": fields.Float(description="Volume armazenado, em hectômetros cúbicos", example=120.0),
        "Volume (%)": fields.Float(description="Volume armazenado, em percentual do volume total", example=50.5),
        "Chuva (mm)": fields.Float(description="Precipitação acumulada das últimas 24 horas, em milímetros", example=10.0),
        "Vazão natural (m³/s)": fields.Float(description="Vazão média diária afluente, em metros cúbicos por segundo", example=20.8),
        "Vazão a jusante (m³/s)": fields.Float(description="Vazão média diária descarregada, em metros cúbicos por segundo", example=17.2),
        "Reservatório": fields.String(description="Indica o reservatório ao qual o registro se refere", example='cantareira')
    },
)

@ns_sis.route("/<inicio>&<fim>&<sistema>")
@ns_sis.response(400, "Solicitação inválida. Verifique a sintaxe da requisição")
@api.doc(params={
	'inicio': 'Data (no formato AAAA-MM-DD, por exemplo 2000-12-31) de início da consulta',
	'fim': 'Data (no formato AAAA-MM-DD, por exemplo 2000-12-31) de final da consulta',
	'sistema': 'Nome do sistema. Opções: cantareira, alto_tiete, rio_claro, rio_grande, guarapiranga, cotia, sao_lourenco'
})
class DadosSistemas(Resource):
	@ns_sis.doc("list_sistemas")
	@ns_sis.marshal_list_with(sistema)
	def get(self, inicio, fim, sistema):
		"""Dados do sistema no período especificado"""
		if sistema not in SISTEMAS:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		try:
			inicio_dt = date.fromisoformat(inicio)
			fim_dt = date.fromisoformat(fim)
		except Exception:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		df = pd.read_csv(f'{DIR_DADOS}/{sistema}.csv')
		df['Data'] = pd.to_datetime(df['Data']).dt.date
		df = df[(df['Data'] >= inicio_dt) & (df['Data'] <= fim_dt)]
		return df.to_dict('records')

@ns_sis.route("/<sistema>")
@ns_sis.response(400, "Solicitação inválida. Verifique a sintaxe da requisição")
@ns_sis.response(404, "Os dados de hoje ainda não foram atualizados")
@api.doc(params={
	'sistema': 'Nome do sistema. Opções: cantareira, alto_tiete, rio_claro, rio_grande, guarapiranga, cotia, sao_lourenco'
})
class DadosSistema(Resource):		
	@ns_sis.doc("get_sistema")
	@ns_sis.marshal_with(sistema)
	def get(self, sistema):
		"""Dados de hoje do sistema especificado, caso haja"""
		if sistema not in SISTEMAS:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		df = pd.read_csv(f'{DIR_DADOS}/{sistema}.csv')
		df['Data'] = pd.to_datetime(df['Data']).dt.date
		hoje = date.today()
		df = df[(df['Data'] == hoje)]
		if len(df) >= 1:
			return df.to_dict('records')
		api.abort(404, "Os dados de hoje ainda não foram atualizados. Tente novamente mais tarde")

@ns_res.route("/<inicio>&<fim>&<sistema>")
@ns_res.response(400, "Solicitação inválida. Verifique a sintaxe da requisição")
@api.doc(params={
	'inicio': 'Data (no formato AAAA-MM-DD, por exemplo 2000-12-31) de início da consulta',
	'fim': 'Data (no formato AAAA-MM-DD, por exemplo 2000-12-31) de final da consulta',
	'sistema': 'Nome do sistema. Opções: cantareira, alto_tiete, rio_claro, rio_grande, guarapiranga, cotia, sao_lourenco'
})
class DadosReservatorios(Resource):
	@ns_res.doc("list_reservatorios")
	@ns_res.marshal_list_with(reservatorio)
	def get(self, inicio, fim, sistema):
		"""Dados dos reservatórios do sistema no período especificado"""
		if sistema not in SISTEMAS:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		try:
			inicio_dt = date.fromisoformat(inicio)
			fim_dt = date.fromisoformat(fim)
		except Exception:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		df = pd.read_csv(f'{DIR_DADOS}/{sistema}_reservatorios.csv')
		df['Data'] = pd.to_datetime(df['Data']).dt.date
		df = df[(df['Data'] >= inicio_dt) & (df['Data'] <= fim_dt)]
		return df.to_dict('records')

@ns_res.route("/<sistema>")
@ns_res.response(400, "Solicitação inválida. Verifique a sintaxe da requisição")
@ns_res.response(404, "Os dados de hoje ainda não foram atualizados")
@api.doc(params={
	'sistema': 'Nome do sistema. Opções: cantareira, alto_tiete, rio_claro, rio_grande, guarapiranga, cotia, sao_lourenco'
})
class DadosReservatoriosHoje(Resource):		
	@ns_res.doc("get_reservatorios")
	@ns_res.marshal_list_with(reservatorio)
	def get(self, sistema):
		"""Dados de hoje dos reservatórios do sistema especificado, caso haja"""
		if sistema not in SISTEMAS:
			api.abort(400, "Solicitação inválida. Verifique a sintaxe da requisição")
		
		df = pd.read_csv(f'{DIR_DADOS}/{sistema}_reservatorios.csv')
		df['Data'] = pd.to_datetime(df['Data']).dt.date
		hoje = date.today()
		df = df[(df['Data'] == hoje)]
		if len(df) >= 1:
			return df.to_dict('records')
		api.abort(404, "Os dados de hoje ainda não foram atualizados. Tente novamente mais tarde")

if __name__ == "__main__":
	app.run(debug=True)