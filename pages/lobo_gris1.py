# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 12:35:20 2024

@author: jperezr
"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# Configuración inicial de la página (debe ser la primera llamada)
st.set_page_config(page_title="Simulación del Algoritmo del Lobo Gris", layout="wide")

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)




# Configuración inicial de la página
#st.set_page_config(page_title="Simulación del Algoritmo del Lobo Gris", layout="centered")

# Función para calcular la distancia al líder
def calcular_distancias(df):
    posiciones_lider = df.iloc[0][["Acciones", "Bonos", "Bienes Raíces", "Fondos", "Bajo Riesgo"]]
    distancias = df.apply(
        lambda row: np.sum(np.abs(row[["Acciones", "Bonos", "Bienes Raíces", "Fondos", "Bajo Riesgo"]] - posiciones_lider)),
        axis=1
    )
    return distancias

# Función para ajustar la suma total de activos a 200,000
def ajustar_suma_activos(df):
    total_activos = df[["Acciones", "Bonos", "Bienes Raíces", "Fondos", "Bajo Riesgo"]].sum(axis=1)
    factor_ajuste = 200000 / total_activos
    for col in ["Acciones", "Bonos", "Bienes Raíces", "Fondos", "Bajo Riesgo"]:
        df[col] = df[col] * factor_ajuste
    return df

# Función para actualizar las posiciones y recalcular jerarquías
def actualizar_lobos(df, iteracion):
    df["Jerarquía Anterior"] = df["Jerarquía"]
    if iteracion % 2 == 0:  # En iteraciones pares, beneficiar al Omega
        df.loc[df["Jerarquía"] == "Omega", "Rend. (%)"] += np.random.uniform(0.5, 1.0)
    else:  # En iteraciones impares, penalizar al Alfa ligeramente
        df.loc[df["Jerarquía"] == "Alfa", "Rend. (%)"] -= np.random.uniform(0.2, 0.6)
    
    df["Acciones"] = df["Acciones"] + np.random.randint(-15000, 15000, size=len(df))
    df["Bonos"] = df["Bonos"] + np.random.randint(-15000, 15000, size=len(df))
    df["Bienes Raíces"] = df["Bienes Raíces"] + np.random.randint(-15000, 15000, size=len(df))
    df["Fondos"] = df["Fondos"] + np.random.randint(-10000, 10000, size=len(df))
    df["Bajo Riesgo"] = df["Bajo Riesgo"] + np.random.randint(-8000, 8000, size=len(df))
    df["Rend. (%)"] = df["Rend. (%)"] + np.random.uniform(-1.0, 1.0, size=len(df))
    df["Riesgo (%)"] = df["Riesgo (%)"] + np.random.uniform(-0.5, 0.5, size=len(df))
    
    df = ajustar_suma_activos(df)
    
    df = df.sort_values(by="Rend. (%)", ascending=False).reset_index(drop=True)
    jerarquias = ["Alfa", "Beta", "Delta", "Omega"]
    df["Jerarquía"] = jerarquias[:len(df)]
    
    df["Distancia al Líder"] = calcular_distancias(df)
    
    return df

# Datos iniciales
datos_iniciales = {
    "Jerarquía": ["Alfa", "Beta", "Delta", "Omega"],
    "Acciones": [70000, 60000, 50000, 40000],
    "Bonos": [30000, 40000, 50000, 50000],
    "Bienes Raíces": [40000, 40000, 50000, 60000],
    "Fondos": [30000, 40000, 30000, 30000],
    "Bajo Riesgo": [30000, 20000, 20000, 20000],
    "Rend. (%)": [8.2, 7.8, 7.5, 7.4],
    "Riesgo (%)": [10.1, 9.2, 9.5, 9.7]
}

# Crear DataFrame inicial
df_lobos = pd.DataFrame(datos_iniciales)

# Título de la aplicación
st.title("Simulación del Algoritmo del Lobo Gris")
st.markdown(""" 
Esta aplicación muestra cómo el Algoritmo del Lobo Gris actualiza las asignaciones de activos (posiciones) y las jerarquías de los lobos, además de calcular las distancias al líder en cada iteración, asegurando que la suma total de los activos sea siempre 200,000.
""")

# Mostrar el DataFrame inicial
st.subheader("Datos Iniciales (Iteración 0)")
st.dataframe(df_lobos)

# Crear listas para almacenar los cambios por iteración
jerarquias_por_iteracion = []
distancias_por_iteracion = []

# Iteraciones del algoritmo
for iteracion in range(1, 6):
    st.subheader(f"Iteración {iteracion}")
    df_lobos = actualizar_lobos(df_lobos, iteracion)
    st.dataframe(df_lobos)

    # Guardar jerarquías y distancias para graficar después
    jerarquias_por_iteracion.append(df_lobos[["Jerarquía", "Jerarquía Anterior"]].copy())
    distancias_por_iteracion.append(df_lobos["Distancia al Líder"].tolist())

# Visualización de la evolución de las jerarquías (gráfico de barras)
st.subheader("Evolución de las Jerarquías")
fig_jerarquias = go.Figure()

# Agregar barras para cada lobo
for i, lobo in enumerate(["Alfa", "Beta", "Delta", "Omega"]):
    jerarquias_iteracion = [jerarquias_por_iteracion[j].iloc[i]["Jerarquía"] for j in range(5)]
    jerarquias_anterior = [jerarquias_por_iteracion[j].iloc[i]["Jerarquía Anterior"] for j in range(5)]

    # Etiquetas: "anterior (nombre) - actual (nombre)"
    etiquetas = [f"{anterior} - {actual}" for anterior, actual in zip(jerarquias_anterior, jerarquias_iteracion)]
    
    fig_jerarquias.add_trace(go.Bar(
        x=[1, 2, 3, 4, 5],
        y=[1 if j == lobo else 0 for j in jerarquias_iteracion],
        name=lobo,
        hovertext=etiquetas,  # Agregar etiquetas en el hover
        hoverinfo="text"
    ))

fig_jerarquias.update_layout(
    title="Evolución de las Jerarquías de los Lobos",
    xaxis_title="Iteración",
    yaxis_title="Jerarquía (1=Alfa, 2=Beta, 3=Delta, 4=Omega)",
    legend_title="Lobos",
    barmode="stack",
    template="plotly_dark"
)

st.plotly_chart(fig_jerarquias)

# Visualización de las distancias al líder
st.subheader("Evolución de las Distancias al Líder")
fig_distancias = go.Figure()

for i, lobo in enumerate(["Alfa", "Beta", "Delta", "Omega"]):
    distancias_iteracion = [distancias_por_iteracion[j][i] for j in range(5)]  # Obtener distancias de cada iteración
    fig_distancias.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=distancias_iteracion,
        mode="lines+markers",
        name=lobo
    ))

fig_distancias.update_layout(
    title="Evolución de las Distancias al Líder",
    xaxis_title="Iteración",
    yaxis_title="Distancia",
    legend_title="Lobos",
    template="plotly_dark"
)

st.plotly_chart(fig_distancias)

# Barra lateral para ayuda
st.sidebar.title("Ayuda")
st.sidebar.markdown("""
**Descripción de la Simulación:**
Esta simulación muestra cómo el Algoritmo del Lobo Gris aplica la actualización de posiciones, jerarquías y distancias al líder en cada iteración.

**Funcionamiento del Algoritmo:**
- Las **posiciones** se actualizan basándose en el rendimiento de los lobos, y las **jerarquías** cambian según ese rendimiento.
- El algoritmo asegura que la suma total de los activos siempre sea de **200,000**.

**Iteraciones:**
Cada iteración utiliza los resultados de la iteración anterior como entrada para la siguiente, actualizando continuamente las posiciones y jerarquías.

**Mi nombre:**  
Javier Horacio Pérez Ricárdez
""")
