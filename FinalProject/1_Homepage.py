import os
import glob
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json
from urllib.request import urlopen
import geopandas as gpd
import warnings
from PIL import Image
import plotly.express as px


warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Time Series Analysis App",
    page_icon="👋",
)

st.title("Time Series Analysis for some Brazilian Cities")
st.sidebar.success("Select a page above.")

# Importa todas as tabelas disponíveis


def importaTabelas():
    dir_data = "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR"
    input_data = {}
    for filename in os.listdir(dir_data):
        if filename.endswith(".csv"):
            variable_name = filename.split('.')[0]
            input_data[variable_name] = pd.read_csv(
                os.path.join(dir_data, filename))
    return input_data

# Função que cria o gráfico que mostra todos os usuários e os eventos relacionados


def plot_todas_cidades(dataframe):

    fig = alt.Chart(dataframe).mark_line().encode(
        alt.Y('metANN', title='Avarage Temperature',
              scale=alt.Scale(zero=False)),
        alt.X('YEAR', title='Year'),
        color=alt.Color(field="CITY", type="nominal",
                        title='Cities', sort=alt.Sort('-y')),
    ).properties(title='Avarage Temperature of All Cities')

    return fig


def plot_destaque_linhas(dataframe):

    highlight = alt.selection(type='single', on='mouseover',
                              fields=['CITY'], nearest=True)

    fig = alt.Chart(dataframe).mark_line().encode(
        alt.Y('metANN', title='Avarage Temperature',
              scale=alt.Scale(zero=False)),
        alt.X('YEAR', title='Year', scale=alt.Scale(zero=False)),
        color=alt.Color(field="CITY", type="nominal",
                        title='City', sort=alt.Sort('-y')),
    ).properties(title='Avarage Temperature of All Cities')

    points = fig.mark_circle().encode(
        opacity=alt.value(0)
    ).add_selection(
        highlight
    ).properties(
        width=600
    )

    lines = fig.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    figura = points + lines

    return figura


def plot_variacao(dataframe):
    fig = alt.Chart(dataframe).mark_bar().encode(
        alt.X('City', type='nominal', title='City', sort=alt.Sort('-y')),
        alt.Y('Variacao', type='quantitative',
              title='Variation')
    ).properties(title="Temperature Variations")

    return fig


# Criando o mapa do brasil com as temperaturas
# Desabilitanto o limite de 5.000 linhas de df do Altair
alt.data_transformers.enable('default', max_rows=None)


def createMap(dataframe):
    mapa_altair = alt.Chart(dataframe,
                            title='Average Temperature of some Brazilian cities').mark_geoshape(
        stroke='grey',
        strokeWidth=0.1).encode(
        alt.Color(shorthand='metANN',
                  type='quantitative',
                  scale=alt.Scale(scheme='reds'),
                  title="metANN"),
        tooltip=['name', 'id', 'metANN']).properties(
        width=600,
        height=400)

    # fig = mapa_altair.configure_view(strokeWidth=0)

    return mapa_altair


# mapa = "geodataBR/geodata-br-master/geojson/geojs-100-mun.json"

# geo_cidades = gpd.read_file(mapa)


# importa = importaTabelas()
# print(type(importa))

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

# df_teste = pd.read_csv(
#    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_belem.csv", sep=';', encoding='UTF-8',)

# transformando o 'id' para tipo object, o mesmo do geoespacial
# df_cidades['id'] = df_cidades['id'].astype('str')

st.write('Global warming refers to the abnormal increase in the average temperature of the planet recorded in recent decades. Therefore, this work aims to use data from temporal temperature series to analyze the temperature changes of some Brazilian cities over the years.')

# df_cidades.info()

# geo_cidades = pd.merge(
#    left=geo_cidades,
#    right=df_cidades.filter(items=['id', 'metANN']),
#    on='id'
# )

# geo_cidades.info()

st.write('Below we present a graph showing the average temperatures measured of all Brazilian cities analyzed in this work. Based on these data we can identify that the city with the highest average over the years is **Boa Vista** and the lowest average temperature is **Curitiba**.')
all_cities = plot_destaque_linhas(df_cidades)
# teste1 = plot_destaque_linhas(df_cidades)
st.altair_chart(all_cities, theme='streamlit',
                use_container_width=True)


# Exibindo o mapa
# map = createMap(geo_cidades)
# st.altair_chart(map, theme='streamlit', use_container_width=True)

def variacoes(dataframe, city):
    maior = (dataframe['metANN']).max()
    menor = (dataframe['metANN']).min()
    cidade = (city)
    result = (maior - menor)
    arranjo = {'City': cidade, 'Variacao': result}

    return arranjo


varia_belem = variacoes(df_belem, "Belém")
varia_boavista = variacoes(df_boavista, "Boa Vista")
varia_brasilia = variacoes(df_brasilia, "Brasília")
varia_canoas = variacoes(df_canoas, "Canoas")
varia_cuiaba = variacoes(df_cuiaba, "Cuiabá")
varia_curitiba = variacoes(df_curitiba, "Curitiba")
varia_floripa = variacoes(df_florianopolis, "Florianópolis")
varia_fortaleza = variacoes(df_fortaleza, "Fortaleza")
varia_goaiania = variacoes(df_goiania, "Goaiânia")
varia_macapa = variacoes(df_macapa, "Macapá")
varia_natal = variacoes(df_natal, "Natal")
varia_recife = variacoes(df_recife, "Recife")
varia_riobranco = variacoes(df_riobranco, "Rio Branco")
varia_salvador = variacoes(df_salvador, "Salvador")
varia_saoluiz = variacoes(df_saoluis, "São Luiz")
varia_saopaulo = variacoes(df_saopaulo, "São Paulo")
varia_vitoria = variacoes(df_vitoria, "Vitória")


df_transforma = pd.DataFrame([varia_belem, varia_boavista, varia_brasilia, varia_canoas, varia_cuiaba, varia_curitiba, varia_floripa, varia_fortaleza,
                              varia_goaiania, varia_macapa, varia_natal, varia_recife, varia_riobranco, varia_salvador, varia_saoluiz, varia_saopaulo, varia_vitoria])

st.write('The bar graph below presents the temperature variation of each Brazilian city analyzed in this work. The maximum and minimum value of the average annual temperature of cities was used as a parameter. With this, we identified that the cities with the highest temperature variation was **Sao Paulo, Curitiba and Salvador**.')
variacaoTotal = plot_variacao(df_transforma)
st.altair_chart(variacaoTotal, theme='streamlit', use_container_width=True)

st.markdown('## Content')
st.write('The data set used in this work comes from the NASA database. It can be consulted at the following address: https://data.giss.nasa.gov/gistemp/station_data_v4_globe/')
st.dataframe(df_cidades)
