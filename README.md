# modelo_sabesp
TCC modelo de ML para previsao de volume do reservatorio São Lourenço

Análise Exploratória dos Dados

O objetivo inicial de modelagem era a criação de modelos que que predizeessem o nível de [agua nos sistemas de abastecimento da SABESP. Ao analisar o site do sistemas produtores da SABESP, identificamos que, temos um total de 7 sistemas de abastecimento e são eles: 
- Alto Tiete
- Cantareira
- Cotia
- Guarapiranga
- Rio Claro 
- Rio Grande
- Sao  Lourenço
Cada sistema é composto por uma certa quantidade de represas que fluente e se unificam no sistema de abastecimento, temos portanto:


Sistema Produtores	Reservatoriios
Alto Iete:	Paratinga, Ponte Nova, Biritiba, Jundiai, Taiaçupeba, Birituba
Cantareira:	Jaguari/Jacarei , Cachoeira , Itibainha, Paiva Castro , Aguas Claras , Jaguari (PBS)
Cotia:	Pedro Beichte, Represa da Graça, Isolina
Guarapiranga:	Guarapiranga, Capivari, Billings
Rio Claro:	Rib. Do Campo
Rio Grande:	Rio Grande, Rib. da Estiva
São Lourenço:	Cachoeira do França


Ao realizar a análise inicial das tabelas percebemos que algumas nao confiam todas as features para a elaboração de um modelo de Machine Learning. Para um análise minuciosa optamos por realizar a modelagem dos dados para o Sistema São Lourenço pois é composto por apenas uma represa. Caso a escolha fosse os demais sistemas teríamos  que criar um modelo por represa dado que cada uma possui suas particularizas especificas.

Para a analise exploratória dos dados, a ideia inicial era a criação de um modelo paramétrico de regressão linear. Esses modelos possuem determinados premissas que precisam ser contempladas portanto logo na EDA alem da observarmos outliers, nulos, misings, duplicados fizemos uma analise para entender a distribuição dos dados e logo foi identificado que nenhuma das features possuíam um distribuição normal; para essa afirmação utilizados o plot de histogramas e o teste de Shapiro-Wilk  que revelou P valor superior a 0.05 para todas as variáveis. As variáveis utilizadas para a o estudo do modelo foram:

"N’vel (m)","Volume (hm_)","Volume (%)","Q Jusante (m_/s)","Q Natural (m_/s)","Chuva (mm), “Data”.

Destacamos ainda que foi incluído um padrão para nomeação das colunas sendo  mnemônicos no inicio da cara coluna do Dataset e CamelCase. As colunas foram transformadas para:

Mnemonics	Significado
Vr:	Colunas onde a informação do seu dado se refere a algum tipo de valor, seja int,flot etc.
Vz:	Colunas onde a informação remete a vazão
Pc:	Percentual % da informação 
Vl:	Volume hm3 (Hectare cúbico)

VrNivel" , "VlVolumeHm", “PcVolume%", "VzQJusante", "VzQNatural","VrChuva", "DdDia", "MmMes", "AaAno”, 

Na coluna data foi realizado um split para quebra  em 3 nos colunas, AaAno , MmMes, e DdDia.

coluna VrNivel 2.5411407243235336e-27. Não Normal
coluna VlVolumeHm 1.0541436849865518e-24. Não Normal
coluna VrVolume% 1.0536989646512335e-24. Não Normal
coluna VlQJusante 1.0517226950027382e-30. Não Normal
coluna VlQNatural 1.6562250020170563e-28. Não Normal
coluna VrChuva 0.0. Não Normal

Fonte: EDA realizado no VSCode

Link: https://psicometriaonline.com.br/o-que-e-o-teste-de-shapiro-wilk/

Como não tem um distribuição normal nos dados, será necessário realizar uma normalização utilizando o Z-Scrore em Python.

