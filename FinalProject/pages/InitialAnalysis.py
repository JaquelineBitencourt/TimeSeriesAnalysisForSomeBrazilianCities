import streamlit as st
import altair as alt
import pandas as pd

st.title("Comparing temperatures from Brazilian cities")

# Função que cria o gráfico de seleção de um único usuário


def plot_cidade(dataframe, cidade, eixo):

    dados_plot = dataframe.query('CITY == @cidade')

    fig = alt.Chart(dados_plot).mark_line().encode(
        alt.X('YEAR', title='Year'),
        alt.Y(eixo, title='Temperature', scale=alt.Scale(zero=False)),
        color=alt.Color(field="CITY", type="nominal",  title='City')

    ).properties(width='container', title=f'Selected season: "{eixo}"')

    return fig


# Importando todas as tabelas para criar apenas um dataframe com todas as cidades
df_belem = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_belem.csv", sep=';')

df_boavista = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_boavista.csv", sep=';')

df_brasilia = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_brasilia.csv", sep=';')

df_cuiaba = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_cuiaba.csv", sep=';')

df_curitiba = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_curitiba.csv", sep=';')

df_florianopolis = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_florianopolis.csv", sep=';')

df_fortaleza = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_fortaleza.csv", sep=';')

df_goiania = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_goiania.csv", sep=';')

df_macapa = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_macapa.csv", sep=';')

df_natal = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_natal.csv", sep=';')

df_recife = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_recife.csv", sep=';')

df_riobranco = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_riobranco.csv", sep=';')

df_salvador = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_salvador.csv", sep=';')

df_saoluis = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_saoluis.csv", sep=';')

df_saopaulo = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_saopaulo.csv", sep=';')

df_vitoria = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_vitoria.csv", sep=';')

df_canoas = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_canoas.csv", sep=';')

df_cidades = pd.concat([df_belem, df_boavista, df_brasilia, df_cuiaba, df_curitiba, df_florianopolis, df_fortaleza,
                        df_goiania, df_macapa, df_natal, df_recife, df_riobranco, df_salvador, df_saoluis, df_saopaulo, df_vitoria, df_canoas])

# st.dataframe(df_cidades)

# st.markdown('## Tabela dos logs de eventos do Windows')

# df_cidades.query('usuario == @usuario')

# Renomeio algumas colunas
columns = {
    'D-J-F': 'Summer',
    'M-A-M': 'Autumn',
    'J-J-A': 'Winter',
    'S-O-N': 'Spring',
    'metANN': 'AnnualAvarage'


}

df_cidades = df_cidades.rename(columns=columns)


st.sidebar.markdown('## Choose the parameters')

cidades = list(df_cidades['CITY'].unique().tolist())
cidades.append('Select')


# Selectbox com todas as opções de cidades do dataset para gerar o primeiro gráfico
cidade1 = st.sidebar.selectbox(
    '**First city**', options=cidades, index=17, key=0)


# Cria a lista com as opções para o eixo y para montar o gráfico
eixoY = pd.DataFrame(df_cidades, columns=[
    'Select', 'Summer', 'Autumn', 'Winter', 'Spring', 'AnnualAvarage']).columns


# Selectbox com opções para o eixo Y do primeiro gráfico
optionY = st.sidebar.selectbox(
    '**Period of the year**', options=eixoY, key=1)

# Lógica para gerar o gráfico 1 depois da seleção
if cidade1 != 'Select' and optionY != 'Select':
    option2 = plot_cidade(df_cidades, cidade1, optionY)
    st.altair_chart(option2, theme='streamlit',
                    use_container_width=True)

else:
    option2 = ""


# Selectbox com todas as opções de cidades do dataset para gerar o segundo gráfico
cidade2 = st.sidebar.selectbox(
    '**Second city**', options=cidades, index=17, key=2)


# Selectbox com opções para o eixo Y do segundo gráfico
optionY = st.sidebar.selectbox(
    '**Period of the year**', options=eixoY, index=0, key=3)

# Lógica para gerar o gráfico 2 depois da seleção
if cidade2 != 'Select' and optionY != 'Select':
    # cities = pd.concat(cidade1, cidade2)
    option2 = plot_cidade(df_cidades, cidade2, optionY)
    st.altair_chart(option2, theme='streamlit',
                    use_container_width=True)

else:
    option2 = ""
