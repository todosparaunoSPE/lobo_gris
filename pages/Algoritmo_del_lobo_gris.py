# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:23:41 2024

@author: jperezr
"""


import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Datos iniciales
data = {
    "Jerarquía": ["Alfa", "Beta", "Delta", "Omega"],
    "Acciones": [70000, 60000, 50000, 40000],
    "Bonos": [30000, 40000, 50000, 50000],
    "Bienes Raíces": [40000, 40000, 50000, 60000],
    "Fondos": [30000, 40000, 30000, 30000],
    "Bajo Riesgo": [30000, 20000, 20000, 20000],
    "Rend. (%)": [8.2, 7.8, 7.5, 7.4],
    "Riesgo (%)": [10.1, 9.2, 9.5, 9.7],
}
df = pd.DataFrame(data)

# Configuración inicial de Streamlit
st.title("Optimización de Portafolios usando el Algoritmo de Lobo Gris")
iterations = 5  # Número de iteraciones
alpha_weight = 0.4  # Peso de Alfa

# Mostrar datos iniciales
st.subheader("Datos Iniciales")
st.dataframe(df)

# Implementación del Algoritmo GWO
def gwo_optimization(data, iterations, alpha_weight):
    np.random.seed(42)
    n_assets = len(data.columns) - 3  # Excluyendo Jerarquía, Rend., Riesgo
    n_wolves = len(data)

    # Inicialización de posiciones (pesos aleatorios)
    positions = np.random.rand(n_wolves, n_assets)
    positions = positions / positions.sum(axis=1, keepdims=True)  # Normalizar

    # Valores iniciales
    asset_returns = np.array([8.2, 7.8, 7.5, 7.4, 7.0])  # Rendimientos por activo
    asset_risks = np.array([10.1, 9.2, 9.5, 9.7, 8.0])    # Riesgos por activo
    previous_hierarchy = data["Jerarquía"].tolist()       # Jerarquías iniciales

    iteration_dataframes = []

    for t in range(iterations):
        a = 2 - t * (2 / iterations)  # Factor de exploración/explotación

        # Calcular el rendimiento y riesgo dinámico basado en las posiciones actuales
        portfolio_returns = np.dot(positions, asset_returns)
        portfolio_risks = np.dot(positions, asset_risks)

        # Calcular fitness
        fitness = portfolio_returns - alpha_weight * portfolio_risks

        # Identificar Alfa, Beta, Delta
        sorted_indices = np.argsort(-fitness)
        alpha, beta, delta = positions[sorted_indices[:3]]

        # Actualizar posiciones
        distances = {"Alfa": [], "Beta": [], "Delta": []}
        for i in range(n_wolves):
            A1 = 2 * a * np.random.rand() - a
            A2 = 2 * a * np.random.rand() - a
            A3 = 2 * a * np.random.rand() - a
            C1 = 2 * np.random.rand()
            C2 = 2 * np.random.rand()
            C3 = 2 * np.random.rand()

            D_alpha = abs(C1 * alpha - positions[i])
            D_beta = abs(C2 * beta - positions[i])
            D_delta = abs(C3 * delta - positions[i])

            distances["Alfa"].append(np.linalg.norm(D_alpha))
            distances["Beta"].append(np.linalg.norm(D_beta))
            distances["Delta"].append(np.linalg.norm(D_delta))

            X1 = alpha - A1 * D_alpha
            X2 = beta - A2 * D_beta
            X3 = delta - A3 * D_delta

            positions[i] = (X1 + X2 + X3) / 3

        # Normalizar posiciones
        positions = np.clip(positions, 0, 1)
        positions = positions / positions.sum(axis=1, keepdims=True)

        # Actualizar jerarquías
        current_hierarchy = ["Alfa", "Beta", "Delta"] + ["Omega"] * (n_wolves - 3)
        current_hierarchy = [current_hierarchy[i] for i in sorted_indices]

        # Crear DataFrame por iteración
        iteration_df = pd.DataFrame({
            "Riesgo": portfolio_risks,
            "Rendimiento": portfolio_returns,
            "Nombre Actual": current_hierarchy,
            "Nombre Anterior": previous_hierarchy,
            "Distancia Alfa": distances["Alfa"],
            "Distancia Beta": distances["Beta"],
            "Distancia Delta": distances["Delta"],
            "Iteración": t + 1
        })
        iteration_dataframes.append(iteration_df)
        previous_hierarchy = current_hierarchy  # Actualizar para la próxima iteración

    return iteration_dataframes

# Ejecutar optimización
iteration_dataframes = gwo_optimization(df, iterations, alpha_weight)

# Mostrar resultados por iteración
st.subheader("Resultados por Iteración")
for i, iteration_df in enumerate(iteration_dataframes, start=1):
    st.write(f"**Iteración {i}**")
    st.dataframe(iteration_df)

    # Gráficos de dispersión
    fig = px.scatter(
        iteration_df,
        x="Riesgo",
        y="Rendimiento",
        color_discrete_sequence=["red"],
        labels={"Riesgo": "Riesgo (%)", "Rendimiento": "Rendimiento (%)"},
        text=iteration_df.apply(
            lambda row: f"{row['Nombre Actual']}<br>R: {row['Rendimiento']:.2f}, Ri: {row['Riesgo']:.2f}", axis=1
        )
    )
    fig.add_scatter(
        x=df["Riesgo (%)"],
        y=df["Rend. (%)"],
        mode="markers+text",
        marker=dict(color="blue"),
        text=df["Jerarquía"],
        name="Datos Iniciales"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(title=f"Iteración {i} - Riesgo vs Rendimiento", showlegend=False)
    st.plotly_chart(fig)