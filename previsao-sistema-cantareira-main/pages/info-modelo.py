import streamlit as st
from st_pages import add_page_title

add_page_title()

st.markdown('''Nesta primeira etapa do modelo, utilizamos o [Prophet](https://facebook.github.io/prophet/) para a elaboração do modelo inicial e, nesta etapa, os dados não foram separados entre dados de treino e teste, que teria como objetivo validar a eficácia do modelo. O aprofundamento da previsão, bem como a utilização de outros modelos e o estudo de correlação entre o volume e as chuvas no Sistema Cantareira, serão aprofundados no trabalho final.

O Prophet é um modelo de regressão aditivo com uma tendência de curva de crescimento linear ou logístico. Trata-se de um algoritmo disponível como um pacote para as linguagens de programação R e Python e é capaz de detectar automaticamente padrões sazonais de uma série, tornando-o bastante acessível.

[Você pode acessar o modelo no GitHub do projeto](https://github.com/GMerencio/previsao-sistema-cantareira/tree/main/modelo-prophet).''')