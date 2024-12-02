# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:02:21 2024

@author: jperezr
"""

import streamlit as st

# Título de la página
st.set_page_config(page_title="Simulación del Algoritmo del Lobo Gris", layout="wide")
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

¡Disfruta explorando el Algoritmo del Lobo Gris y descubre cómo se comportan los lobos a lo largo de las iteraciones!

""")