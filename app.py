import streamlit as st
import pandas as pd

# Configuración del título de la aplicación
st.title("📊 Calculadora de Regresión y Sumatorias")

# 1. Ingreso del número de muestras (n)
st.header("1. Configuración de la Muestra")
n = st.number_input("Ingrese el número de muestras (n):", min_value=1, value=5, step=1)

st.header("2. Ingreso de Datos")
st.write("Modifique los valores directamente en las tablas siguientes:")

# Crear dos columnas para mostrar las tablas independientes lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Valores de X")
    # Crear un DataFrame inicial para X con valores por defecto (0.0)
    df_x_init = pd.DataFrame({"X": [0.0] * n})
    # Tabla interactiva para X
    edited_df_x = st.data_editor(df_x_init, num_rows="fixed", key="tabla_x")
    x_values = edited_df_x["X"].tolist()

with col2:
    st.subheader("Valores de Y")
    # Crear un DataFrame inicial para Y con valores por defecto (0.0)
    df_y_init = pd.DataFrame({"Y": [0.0] * n})
    # Tabla interactiva para Y
    edited_df_y = st.data_editor(df_y_init, num_rows="fixed", key="tabla_y")
    y_values = edited_df_y["Y"].tolist()

# 3. Cálculos matemáticos
# Cálculos básicos y sumatorias
sum_x = sum(x_values)
sum_y = sum(y_values)
promedio_x = sum_x / n if n > 0 else 0
promedio_y = sum_y / n if n > 0 else 0

# X al cuadrado y su sumatoria
x_cuadrado = [x ** 2 for x in x_values]
sum_x_cuadrado = sum(x_cuadrado)

# Producto X*Y y su sumatoria (necesario para la pendiente)
x_por_y = [x * y for x, y in zip(x_values, y_values)]
sum_xy = sum(x_por_y)

# Cálculo de la pendiente (m) de la línea de regresión: y = mx + b
# Fórmula: m = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - (sum(x))^2)
denominador_pendiente = (n * sum_x_cuadrado) - (sum_x ** 2)

if denominador_pendiente != 0:
    pendiente = ((n * sum_xy) - (sum_x * sum_y)) / denominador_pendiente
else:
    pendiente = None  # Evita la división por cero si todos los valores de X son iguales

# 4. Mostrar Resultados
st.header("3. Resultados y Cálculos")

# Tabla de desarrollo detallada
df_resultados = pd.DataFrame({
    "X": x_values,
    "Y": y_values,
    "X²": x_cuadrado,
    "X · Y": x_por_y
})
st.subheader("Tabla de Desarrollo")
st.dataframe(df_resultados)

# Mostrar métricas organizadas en contenedores
st.subheader("Métricas Generales")
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(label="Sumatoria de X (∑X)", value=f"{sum_x:.4f}")
    st.metric(label="Sumatoria de Y (∑Y)", value=f"{sum_y:.4f}")
    st.metric(label="Sumatoria de X² (∑X²)", value=f"{sum_x_cuadrado:.4f}")

with metric_col2:
    st.metric(label="Promedio de X (X̄)", value=f"{promedio_x:.4f}")
    st.metric(label="Promedio de Y (Ȳ)", value=f"{promedio_y:.4f}")
    if pendiente is not None:
        st.metric(label="Pendiente (m)", value=f"{pendiente:.4f}")
    else:
        st.metric(label="Pendiente (m)", value="Indefinida (División por cero)")
