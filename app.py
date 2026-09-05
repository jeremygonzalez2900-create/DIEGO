import streamlit as st
import pandas as pd

# Configuración del título de la aplicación
st.title("📊 Calculadora de Regresión Lineal con Fórmulas")

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
denominador = (n * sum_x_cuadrado) - (sum_x ** 2)
numerador_b1 = (n * sum_xy) - (sum_x * sum_y)

if denominador != 0:
    b1 = numerador_b1 / denominador
    b0 = promedio_y - (b1 * promedio_x)
else:
    b1 = None
    b0 = None

# 4. Mostrar Resultados Numéricos
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

# Métricas rápidas
metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric(label="Sumatoria de X (∑X)", value=f"{sum_x:.4f}")
    st.metric(label="Sumatoria de Y (∑Y)", value=f"{sum_y:.4f}")
    st.metric(label="Sumatoria de X² (∑X²)", value=f"{sum_x_cuadrado:.4f}")
with metric_col2:
    st.metric(label="Promedio de X (X̄)", value=f"{promedio_x:.4f}")
    st.metric(label="Promedio de Y (Ȳ)", value=f"{promedio_y:.4f}")

# 5. Sección de Fórmulas Sustituidas paso a paso
st.header("4. Desarrollo de Fórmulas (Sustitución)")

# Fórmulas de Promedios
st.subheader("Promedios")
st.latex(r"\bar{X} = \frac{\sum X}{n} = \frac{" + f"{sum_x:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_x:.4f}")
st.latex(r"\bar{Y} = \frac{\sum Y}{n} = \frac{" + f"{sum_y:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_y:.4f}")

# Fórmula y sustitución de B1
st.subheader("Pendiente ($B_1$)")
st.latex(r"B_1 = \frac{n\sum(XY) - (\sum X)(\sum Y)}{n\sum(X^2) - (\sum X)^2}")
if b1 is not None:
    st.latex(r"B_1 = \frac{" + f"{n}({sum_xy:.4f}) - ({sum_x:.4f})({sum_y:.4f})" + "}{" + f"{n}({sum_x_cuadrado:.4f}) - ({sum_x:.4f})^2}")
    st.latex(r"B_1 = \frac{" + f"{numerador_b1:.4f}" + "}{" + f"{denominador:.4f}" + "} = " + f"{b1:.4f}")
else:
    st.error("Error: El denominador es 0. No se puede calcular B1.")

# Fórmula y sustitución de B0
st.subheader("Intercepto ($B_0$)")
st.latex(r"B_0 = \bar{Y} - B_1\bar{X}")
if b0 is not None:
    st.latex(r"B_0 = " + f"{promedio_y:.4f} - ({b1:.4f})({promedio_x:.4f}) = {b0:.4f}")
else:
    st.error("Error: No se puede calcular B0 debido a la indeterminación en B1.")

# Ecuación de la recta final con sombrero de predicción
st.subheader("Ecuación de Regresión Final")
if b1 is not None and b0 is not None:
    signo = "+" if b1 >= 0 else "-"
    # Usamos \hat{Y} para denotar el valor estimado (signo de potencia/sombrero arriba de la Y)
    st.latex(r"\hat{Y} = " + f"{b0:.4f} {signo} {abs(b1):.4f}X")
