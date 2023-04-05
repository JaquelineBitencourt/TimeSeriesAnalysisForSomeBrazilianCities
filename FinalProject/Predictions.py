import streamlit as st
import pandas as pd
import altair as alt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pages.InitialAnalysis import *

# st.title("Predictions")

# st.write("You have entered", st.session_state["my_input"])


def plot_forecast(dataframe, prediction):
    base = alt.Chart(dataframe).encode(
        x='YEAR',
    )

    line = base.mark_line().encode(
        y=alt.Y('metANN:Q', title='Precipitation (mm/month)'))

    band = base.mark_errorband(extent='iqr').encode(
        y=alt.Y(prediction, title='Precipitation (mm/month)'))

    (band + line).properties(width=600, height=300)

    fig = band + line

    return fig


def plot_todas_forecast(dataframe):

    fig = alt.Chart(dataframe).mark_line().encode(
        alt.Y(dataframe.metANN, title='Avarage Temperature',
              scale=alt.Scale(zero=False)),
        alt.X(dataframe.YEAR, title='Year')

    ).properties(title='Avarage Temperature of All Cities')

    return fig


def umAnoPredito(dataframe):
    model = ExponentialSmoothing(
        endog=dataframe.metANN, trend='add', seasonal='add', seasonal_periods=12).fit()
    predictions = model.forecast(steps=31)
    # print(predictions))
    return predictions


df_natal = pd.read_csv(
    "D:/Users/jay_e/Documents/Doutorado/DisciplinaComba/AtividadesEnviadas/FinalProject/TemperaturasBR/station_natal.csv", sep=';', index_col='YEAR', parse_dates=True).asfreq("AS")


# novo_df = pd.DataFrame(df_natal.metANN)

# print(novo_df.metANN)

predicao = umAnoPredito(df_natal)
print(type(predicao))
predito = pd.DataFrame(predicao)

print(predito.columns)

# concatenado = pd.concat(predito, df_natal)

# st.altair_chart(concatenado, theme='streamlit', use_container_width=True)
# print(novo_df)
