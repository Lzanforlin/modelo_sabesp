# sabesp-api

Projeto parte de um TCC em Ciência de Dados da Univesp que visa aumentar a acessibilidade dos dados de sistemas produtores fornecios pela SABESP. Este repositório foca na extração e disponibilização dos dados através de uma API REST. O [segundo repositório](https://github.com/GMerencio/sabesp-dashboard) foca na visualização dos dados através de um dashboard para a população geral.

[A API pode ser acessada aqui](https://sabesp-api.onrender.com/).

## Tecnologias

As principais tecnologias usadas no projeto são:

* [Python 3.8](https://www.python.org/)
* [Flask 2.3.3](https://flask.palletsprojects.com/en/3.0.x/)
* [Flask RESTX 1.1.0](https://github.com/python-restx/flask-restx)
* [Requests](https://pypi.org/project/requests/)

## Estrutura do projeto

Os principais arquivos e diretórios são:

* `app.py`: Arquivo de entrada da API, contendo os endpoints e a documentação Swagger.
* `dados`: Diretório contendo os dados extraídos da SABESP.
* `dados_2023-10-10`: Diretório contendo os dados extraídos da SABESP até 10/10/2023 para fins de análise.
* `scripts/scraper.py`: Arquivo contendo as principais funções de extração de dados da SABESP.
* `scripts/runner.py`: Script acionado periodicamente para verificar se há novos dados e atualizar os arquivos.
* `scripts/batch.py`: Script usado para obter os dados em batch, permitindo especificar o período, sistemas, modo de escrita dos arquivos e diretório de output através de argumentos de linha de comando.
* `.github/workflows/atualizar_dados.yaml`: Arquivo especificando a rotina de verificação de novos dados através do GitHub Actions.

## Setup 

 1. Instale [`pipenv`](https://pypi.org/project/pipenv/).
 2. No diretório do projeto, execute `pipenv install` no terminal.
 3. Para ativar o ambiente virtual, execute `pipenv shell`.
 4. Para rodar a aplicação Streamlit localmente, execute `python app.py` no terminal. Lembre de ativar o ambiente virtual antes.