# -*- coding: utf-8 -*-
"""Avance1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/183V-A_GAroMZZMTSuSIKZdDb7E2run_C
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
st.set_page_config(layout="wide")
import plotly.graph_objs as go
#dataset
#link='https://www.datosabiertos.gob.pe/sites/default/files/tb_medida_estaciones%20%281%29_0.csv'
#Leo el dataset
df = pd.read_csv('tb_medida_estaciones (1)_0.csv')

# Pre procesamiento

df = df.drop('FECHA_CORTE', axis=1)
df = df.drop('UBIGEO', axis=1)
df = df.drop('DEPARTAMENTO', axis=1)
df = df.rename(columns={'CUENTA': 'CUENCA'})


#Filtro para que el usuario elija la "Estación" que quiere ver en el cuadro
option_1 = st.selectbox(
   "Elige una PROVINCIA",
   (df['PROVINCIA'].unique()),
   index=None,
   placeholder="Seleccione una PROVINCIA",
)

#Filtro para que el usuario elija la "Estación" que quiere ver en el cuadro
option_2 = st.selectbox(
   "Elige una DISTRITO",
   (df[df['PROVINCIA'] == option_1]['DISTRITO'].unique()),
   index=None,
   placeholder="Seleccione un DISTRITO",
)


#convierto la FECHA_MUESTRA que es numerico a date y creo una columna tipo DATE para poder usar la herramienta calendario de Streamlit
df['FECHA_MUESTRA'] = pd.to_datetime(df['FECHA_MUESTRA'], format='%Y%m%d')
df.insert(0, "D_FECHA_MUESTRA", df['FECHA_MUESTRA'].dt.date)

#Elimino fecha_muestra porque ya tengo D_FECHA_MUESTRA
df = df.drop('FECHA_MUESTRA', axis=1)

#Saco el minimo y maximo de las fechas de la data para ponerlo por defecto y poder darle la opción que filtre en un rango de fechas
fmax=df['D_FECHA_MUESTRA'].max()
fmin=df['D_FECHA_MUESTRA'].min()

#Filtros de fecha para que escoja su intervalo
d1 = st.date_input("Fecha Inicial", value=fmin)
d2 = st.date_input("Fecha Final", value=fmax)


# Agregar casillas de verificación para las columnas deseadas
show_caudal = st.checkbox('CAUDAL07H')
show_promedio = st.checkbox('PROMEDIO24H')
show_maxima = st.checkbox('MAXIMA24H')
show_precip = st.checkbox('PRECIP24H')

# Filtrar el dataframe según las opciones seleccionadas por el usuario
selected_columns = ['D_FECHA_MUESTRA', 'PROVINCIA','DISTRITO','UNIDAD_MEDIDA']
if show_caudal:
    selected_columns.append('CAUDAL07H')
if show_promedio:
    selected_columns.append('PROMEDIO24H')
if show_maxima:
    selected_columns.append('MAXIMA24H')
if show_precip:
    selected_columns.append('PRECIP24H')




#Filtro el dataframe para que muestre segun los filtros seleccionados
df = df[(df['D_FECHA_MUESTRA'] >= d1) &
        (df['D_FECHA_MUESTRA'] <= d2) &
        (df['PROVINCIA'] == option_1) &
         (df['DISTRITO'] == option_2)][selected_columns]



option = st.sidebar.selectbox("Estación", df['DISTRITO'].unique(), )

#muestro dataset
df

if df.empty:
    st.write("No hay datos para mostrar con los filtros seleccionados.")
else:
    # Crear el gráfico de líneas
    fig = go.Figure()

    for col in selected_columns[4:]:  # Seleccionar desde la quinta columna en adelante ('CAUDAL07H', 'PROMEDIO24H', 'MAXIMA24H', 'PRECIP24H')
        if col in df.columns:
            fig.add_trace(go.Scatter(x=df['D_FECHA_MUESTRA'], y=df[col], mode='lines', name=col))

    # Establecer el diseño del gráfico
    fig.update_layout(
        title='Gráfica',
        xaxis_title='Fechas',
        yaxis_title='Valores',
        showlegend=True
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)