previsao-sistema-cantareira
Projeto referente a TCC Univesp que visa desenvolver modelos de previsão do volume do Sistema Cantareira utilizando métodos de machine learning e ferramentas de visualização de dados.

A aplicação pode ser acessada aqui.

Tecnologias
As principais tecnologias usadas no projeto são:

Python 3.8
Prophet
Plotly
Streamlit
Estrutura do projeto
Os principais arquivos e diretórios são:

streamlit-app.py: Arquivo de entrada e página principal da aplicação Streamlit responsável pela interface de visualização.
plotting_utils.py: Funções de auxílio para as visualizações de dados.
pages: Diretório contendo as demais páginas da aplicação Streamlit, cada uma em um arquivo.
static: Diretório contendo as imagens, vídeos e outros arquivos estáticos utilizados na aplicação Streamlit.
SABESP-sistemas_produtores.xlsx: Série histórica contendo os dados dos reservatórios Jaguari-Jacareí, Cachoeira, Atibainha e Paiva Castro de 2000 até março de 2023.
2023-04-01_a_2023-05-25.xlsx: Dados dos reservatórios Jaguari-Jacareí, Cachoeira, Atibainha e Paiva Castro de abril de 2023 até maio de 2023.
PI_IV.ipynb: Notebook Jupyter com análise exploratória e tratamento dos dados.
modelo-prophet: Diretório contendo o modelo que utiliza o Prophet para prever valores futuros.
Setup
Instale pipenv.
No diretório do projeto, execute pipenv install no terminal.
Para ativar o ambiente virtual, execute pipenv shell.
Para rodar a aplicação Streamlit localmente, execute streamlit run streamlit-app.py no terminal. Lembre de ativar o ambiente virtual antes.
