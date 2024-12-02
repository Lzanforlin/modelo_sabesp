# previsao-sistema-cantareira

"Final Project: Ensemble Deep Learning Model for Water Management: Forecasting Sabesp's
Cantareira Reservoir Levels

Project Summary:
This project aims to support water management and prevent supply crises during periods of scarcity by forecasting reservoir levels in Sabesp's Cantareira System. It combines Long Short-Term Memory (LSTM) Recurrent Neural Networks (RNN) with time series data for accurate level prediction. The solution includes API integration for data access and a dashboard for continuous monitoring and visualization of trends, enhancing proactive water resource management."


Projeto TCC da Univesp que visa desenvolver modelos de previsão do volume do Sistema Cantareira utilizando métodos de machine learning e deep learning utilizando API e ferramentas de visualização de dados e Dashboard.

[A aplicação pode ser acessada aqui](https://previsao-cantareira.streamlit.app/).

## Tecnologias

As principais tecnologias usadas no projeto são:

* [Python 3.8](https://www.python.org/)
* [Prophet](https://facebook.github.io/prophet/)
* [Plotly](https://plotly.com/)
* [Streamlit](https://streamlit.io/)

## Estrutura do projeto

Os principais arquivos e diretórios são:

* `streamlit-app.py`: Arquivo de entrada e página principal da aplicação Streamlit responsável pela interface de visualização.
* `plotting_utils.py`: Funções de auxílio para as visualizações de dados.
* `pages`: Diretório contendo as demais páginas da aplicação Streamlit, cada uma em um arquivo.
* `static`: Diretório contendo as imagens, vídeos e outros arquivos estáticos utilizados na aplicação Streamlit.
* `SABESP-sistemas_produtores.xlsx`: Série histórica contendo os dados dos reservatórios Jaguari-Jacareí, Cachoeira, Atibainha e Paiva Castro de 2000 até março de 2023.
* `2023-04-01_a_2023-05-25.xlsx`: Dados dos reservatórios Jaguari-Jacareí, Cachoeira, Atibainha e Paiva Castro de abril de 2023 até maio de 2023.
* `PI_IV.ipynb`: Notebook Jupyter com análise exploratória e tratamento dos dados.
* `modelo-prophet`: Diretório contendo o modelo que utiliza o Prophet para prever valores futuros.

## Setup 

 1. Instale [`pipenv`](https://pypi.org/project/pipenv/).
 2. No diretório do projeto, execute `pipenv install` no terminal.
 3. Para ativar o ambiente virtual, execute `pipenv shell`.
 4. Para rodar a aplicação Streamlit localmente, execute `streamlit run streamlit-app.py` no terminal. Lembre de ativar o ambiente virtual antes.
