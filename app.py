import streamlit as st
import pandas as pd

# Configuración del título de la aplicación
st.title("📊 Calculadora de Regresión Lineal ($B_1$ y $B_0$)")

# 1. Ingreso del número de muestras (n)
st.header("1. Configuración de la Muestra")
n = st.number_input("Ingrese el número de muestras (n):", min_value=1, value=5, step=1)

st.header("2. Ingreso de Datos")
st.write("Modifique los valores directamente en las tablas siguientes:")

# Crear dos columnas para mostrar las tablas independientes lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Valores de X")
    df_x_init = pd.DataFrame({"X": [0.0] * n})
    edited_df_x = st.data_editor(df_x_init, num_rows="fixed", key="tabla_x")
    x_values = edited_df_x["X"].tolist()

with col2:
    st.subheader("Valores de Y")
    df_y_init = pd.DataFrame({"Y": [0.0] * n})
    edited_df_y = st.data_editor(df_y_init, num_rows="fixed", key="tabla_y")
    y_values = edited_df_y["Y"].tolist()

# 3. Cálculos matemáticos
sum_x = sum(x_values)
sum_y = sum(y_values)
promedio_x = sum_x / n if n > 0 else 0
promedio_y = sum_y / n if n > 0 else 0

# X al cuadrado y su sumatoria
x_cuadrado = [x ** 2 for x in x_values]
sum_x_cuadrado = sum(x_cuadrado)

# Producto X*Y y su sumatoria
x_por_y = [x * y for x, y in zip(x_values, y_values)]
sum_xy = sum(x_por_y)

# Cálculo de la pendiente (B1) e Intercepto (B0)
# Fórmula B1 = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - (sum(x))^2)
# Fórmula B0 = promedio_y - (B1 * promedio_x)
denominador = (n * sum_x_cuadrado) - (sum_x ** 2)

if denominador != 0:
    b1 = ((n * sum_xy) - (sum_x * sum_y)) / denominador
    b0 = promedio_y - (b1 * promedio_x)
else:
    b1 = None
    b0 = None

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

st.subheader("Coeficientes de Regresión")
coef_col1, coef_col2 = st.columns(2)

with coef_col1:
    if b1 is not None:
        st.metric(label="Pendiente ($B_1$)", value=f"{b1:.4f}")
    else:
        st.metric(label="Pendiente ($B_1$)", value="Indefinida")

with coef_col2:
    if b0 is not None:
        st.metric(label="Intercepto ($B_0$)", value=f"{b0:.4f}")
    else:
        st.metric(label="Intercepto ($B_0$)", value="Indefinido")

# Mostrar la ecuación final en formato matemático
st.subheader("Ecuación de la Recta")
if b1 is not None and b0 is not None:
    signo = "+" if b1 >= 0 else "-"
    st.latex(f"Y = {b0:.4f} {signo} {abs(b1):.4f}X")
else:
    st.info("No se puede estructurar la ecuación debido a indeterminación matemática (división por cero).")
