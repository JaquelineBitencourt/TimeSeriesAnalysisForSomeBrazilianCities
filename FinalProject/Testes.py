import os
import glob
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# import statsmodels as sm
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Forecasting App",
    page_icon="👋",
)

st.title("Main Page")
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


def substituiTemps999Media(input_data):
    for i in input_data.keys():
        for j in input_data[i].columns:
            input_data[i][j] = input_data[i][j].replace(999.90, np.NaN)
            input_data[i][j] = input_data[i][j].fillna(
                input_data[i][j].rolling(12, 1).mean())
        return input_data


def destroiEstacoes(input_data):
    for i in input_data.keys():
        input_data[i].drop(
            ['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N'], axis=1, inplace=True)
        df = input_data[i].T
        df.columns = df.iloc[0]
        df.drop(['YEAR'], axis=0, inplace=True)
    return input_data


def reconstroi(input_data):
    for i in input_data.keys():
        input_data[i] = pd.melt(input_data[i], id_vars=['YEAR', 'metANN'], value_vars=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',],
                                var_name='month', value_name='Temp')
        input_data[i]['Date'] = pd.to_datetime(input_data[i]['YEAR'].astype(
            str)+'/'+input_data[i]['month'].astype(str)+'/01')
        input_data[i].drop(['YEAR', 'month'], axis=1, inplace=True)
        input_data[i].sort_values(by='Date', inplace=True)
    return input_data


def fazAlgumaCoisa(input_data):
    temp_data = {}
    metANN_data = {}
    for i in input_data.keys():
        temp_data[i] = input_data[i][['Date', 'Temp']]
        temp_data[i] = temp_data[i].set_index('Date')
        # metANN_data[i] = input_data[i][['Date', 'metANN']]
        # metANN_data[i] = metANN_data[i].groupby(
        # pd.Grouper(key='Date', freq='Y')).mean()
        zero_index = list(temp_data.keys())[0]
        one_index = list(temp_data.keys())[1]
        temp_df = temp_data[zero_index].merge(
            temp_data[one_index], left_on="Date", right_on='Date', suffixes=('_'+zero_index, '_'+one_index))

        for i in list(temp_data.keys())[2:]:
            temp_df = temp_df.merge(temp_data[i], left_on='Date', right_on='Date').rename(
                columns={'Temp': 'Temp_'+i+''})
    return input_data


importa = importaTabelas()
limpa = substituiTemps999Media(importa)
apagaEstacoes = destroiEstacoes(limpa)
reconstruir = reconstroi(apagaEstacoes)

imprimir = substituiTemps999Media(importa)
df = pd.DataFrame(imprimir)
st.dataframe(df)
