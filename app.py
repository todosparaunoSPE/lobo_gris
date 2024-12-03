# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:02:21 2024

@author: jperezr
"""

import streamlit as st

from datetime import datetime

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

# Título de la página
st.title("Simulación del Algoritmo del Lobo Gris")

# Descripción de la página
st.markdown("""
**Bienvenido a la Simulación del Algoritmo del Lobo Gris!**

En esta aplicación, mostramos cómo el **Algoritmo del Lobo Gris** es capaz de simular el comportamiento de un grupo de lobos con jerarquías variables y distancias relativas al líder, además de actualizar sus posiciones en función de ciertos criterios de rendimiento.

### ¿Qué es el Algoritmo del Lobo Gris?
El Algoritmo del Lobo Gris es un algoritmo de optimización basado en la **simulación de la caza de lobos**, donde los lobos buscan la mejor solución posible (simulada como la "presa"). Cada lobo tiene una jerarquía (Alfa, Beta, Delta, Omega) que determina su rol en la caza, y la **distancia al líder** es un factor importante para determinar cómo se mueven los lobos dentro del espacio de búsqueda.

### ¿Cómo Funciona la Simulación?
1. **Datos Iniciales**: Comienza con un conjunto de **lobos** con propiedades específicas, como activos en diferentes categorías (acciones, bonos, bienes raíces, etc.) y jerarquías iniciales.
2. **Iteraciones**: En cada iteración:
   - Se actualizan las **posiciones** de los lobos en función de su rendimiento.
   - Se recalculan las **jerarquías** (Alfa, Beta, Delta, Omega).
   - Se calcula la **distancia al líder**.
3. **Visualización**: La aplicación muestra la **evolución de las jerarquías** y las **distancias al líder** en gráficos interactivos, permitiendo ver cómo los lobos cambian de posiciones y jerarquías a lo largo de las iteraciones.

### ¿Cómo Usar Esta Aplicación?
1. **Interactuar con la Simulación**: Puedes visualizar cómo cambian las jerarquías y las distancias de los lobos a medida que avanzan las iteraciones.
2. **Gráficos Interactivos**: Los gráficos muestran las jerarquías de los lobos y las distancias al líder a lo largo de las iteraciones.

### Creado por:
**Javier Horacio Pérez Ricárdez**

#¡Disfruta explorando el Algoritmo del Lobo Gris y descubre cómo se comportan los lobos a lo largo de las iteraciones!
""")


# Mostrar tu nombre en la barra lateral
st.sidebar.write("**Nombre:** Javier Horacio Pérez Ricárdez")

# Mostrar la fecha actual en la barra lateral
fecha_actual = datetime.now().strftime("%d/%m/%Y")
st.sidebar.write(f"**Fecha:** {fecha_actual}")

