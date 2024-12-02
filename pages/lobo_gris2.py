# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:02:07 2024

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
    df["Jerarquía Anterior"] = df["Jerarquía"]  # Guardar la jerarquía actual como anterior
    if iteracion % 2 == 0:  # En iteraciones pares, beneficiar al Omega
        df.loc[df["Jerarquía"] == "Omega", "Rend. (%)"] += np.random.uniform(0.5, 1.0)
    else:  # En iteraciones impares, penalizar al Alfa ligeramente
        df.loc[df["Jerarquía"] == "Alfa", "Rend. (%)"] -= np.random.uniform(0.2, 0.6)
    
    # Actualizar las posiciones de los activos
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
    df["Jerarquía"] = jerarquias[:len(df)]  # Actualizar la jerarquía
    
    df["Distancia al Líder"] = calcular_distancias(df)  # Calcular distancias al líder
    
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
df_lobos["Jerarquía Anterior"] = df_lobos["Jerarquía"]  # Inicializar "Jerarquía Anterior"
df_lobos["Distancia al Líder"] = calcular_distancias(df_lobos)  # Inicializar "Distancia al Líder"

# Título de la aplicación
st.title("Simulación del Algoritmo del Lobo Gris")
st.markdown("""
Esta aplicación muestra cómo el Algoritmo del Lobo Gris actualiza las posiciones, jerarquías y calcula las distancias al líder en cada iteración, asegurando que la suma de los activos sea siempre 200,000.
""")

# Mostrar el DataFrame inicial
st.subheader("Datos Iniciales (Iteración 0)")
st.dataframe(df_lobos)

# Crear listas para almacenar los DataFrames por iteración
dataframes_por_iteracion = [df_lobos.copy()]

# Generar las iteraciones
for iteracion in range(1, 6):
    st.subheader(f"Iteración {iteracion}")
    df_lobos = actualizar_lobos(df_lobos, iteracion)
    st.dataframe(df_lobos)
    dataframes_por_iteracion.append(df_lobos.copy())

# Graficar la evolución
for i in range(1, 6):
    st.subheader(f"Comparación: Iteración {i - 1} vs Iteración {i}")
    
    df_anterior = dataframes_por_iteracion[i - 1]
    df_actual = dataframes_por_iteracion[i]
    
    fig_dispersion = go.Figure()

    # Puntos de la iteración anterior (azul)
    for index, row in df_anterior.iterrows():
        texto = f"Actual: {row['Jerarquía']}" if i > 1 else f"Anterior: {row['Jerarquía Anterior']}<br>Distancia: {row['Distancia al Líder']:.2f}"
        fig_dispersion.add_trace(go.Scatter(
            x=[row["Riesgo (%)"]],  # Cambiar a eje X: Riesgo (%)
            y=[row["Rend. (%)"]],  # Cambiar a eje Y: Rendimiento (%)
            mode="markers+text",
            name=f"{row['Jerarquía Anterior']} (Iteración {i-1})",
            text=[texto],
            textposition="top center",
            marker=dict(size=12, color="blue")
        ))

    # Puntos de la iteración actual (rojo)
    for index, row in df_actual.iterrows():
        fig_dispersion.add_trace(go.Scatter(
            x=[row["Riesgo (%)"]],  # Cambiar a eje X: Riesgo (%)
            y=[row["Rend. (%)"]],  # Cambiar a eje Y: Rendimiento (%)
            mode="markers+text",
            name=f"{row['Jerarquía']} (Iteración {i})",
            text=[f"Actual: {row['Jerarquía']}<br>Anterior: {row['Jerarquía Anterior']}<br>Distancia: {row['Distancia al Líder']:.2f}"],
            textposition="top center",
            marker=dict(size=12, color="red")
        ))

    # Configurar el diseño del gráfico
    fig_dispersion.update_layout(
        title=f"Comparación de Iteración {i - 1} vs Iteración {i}",
        xaxis_title="Riesgo (%)",  # Etiqueta del eje X
        yaxis_title="Rendimiento (%)",  # Etiqueta del eje Y
        template="plotly_dark",
        legend_title="Lobos"
    )

    st.plotly_chart(fig_dispersion)



# Barra lateral
st.sidebar.title("Ayuda")
st.sidebar.markdown("""
Bienvenido a la simulación del Algoritmo del Lobo Gris.

**Algoritmo del Lobo Gris:**
El algoritmo se aplica en varias iteraciones, donde en cada una, los puntos rojos de la iteración anterior se convierten en los puntos azules de la siguiente. Cada iteración actualiza las posiciones y jerarquías de los lobos.

### Datos Iniciales:
Los datos iniciales incluyen las posiciones de cada lobo, su jerarquía, y sus activos (acciones, bonos, bienes raíces, etc.).

### Iteraciones:
En cada iteración, las posiciones se actualizan según el rendimiento de los lobos, y se recalcula la jerarquía (Alfa, Beta, Delta, Omega) de acuerdo con esos cambios.

### Visualización:
- **Eje X:** Riesgo (%)
- **Eje Y:** Rendimiento (%)


 
Javier Horacio Pérez Ricárdez
""")
