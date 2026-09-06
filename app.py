import streamlit as st
import pandas as pd
import math

# Configuración del título de la aplicación
st.title("Calculadora de Regresión Lineal Completa")

# # 1. Ingreso del número de muestras (n)
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

# # 3. Cálculos matemáticos iniciales
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
numerator_b1 = (n * sum_xy) - (sum_x * sum_y)

if denominador != 0:
    b1 = numerator_b1 / denominador
    b0 = promedio_y - (b1 * promedio_x)
else:
    b1 = None
    b0 = None

# # 4. Cálculo de Errores, Métricas (MSE, MAE, RMSE)
errores = []
errores_abs = []
errores_cuadrado = []
y_estimadas = []

if b1 is not None and b0 is not None:
    for x, y in zip(x_values, y_values):
        y_hat = b0 + (b1 * x)
        y_estimadas.append(y_hat)
        e = y - y_hat
        errores.append(e)
        errores_abs.append(abs(e))
        errores_cuadrado.append(e ** 2)
else:
    y_estimadas = [0.0] * n
    errores = [0.0] * n
    errores_abs = [0.0] * n
    errores_cuadrado = [0.0] * n

sum_errores = sum(errores)
sum_errores_abs = sum(errores_abs)
sum_errores_cuadrado = sum(errores_cuadrado)

# Cálculo de métricas globales de error
mae = sum_errores_abs / n if n > 0 else 0
mse = sum_errores_cuadrado / n if n > 0 else 0
rmse = math.sqrt(mse)

# # 5. Mostrar Resultados Numéricos
st.header("3. Resultados y Cálculos")

# Tabla de desarrollo detallada
df_resultados = pd.DataFrame({
    "X": x_values,
    "Y": y_values,
    "X²": x_cuadrado,
    "X·Y": x_por_y,
    "Ŷ (Estimado)": y_estimadas
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
    st.metric(label="Promedio de Y (Ȳ)", value=f"{promedio_y:.4f}")

# # 6. Sección de Fórmulas Sustituidas paso a paso
st.header("4. Desarrollo de Fórmulas (Sustitución)")

# Fórmulas de Promedios
st.subheader("Promedios")
st.latex(rf"\bar{{X}} = \frac{{\sum X}}{{n}} = \frac{{{sum_x:.4f}}}{{{n}}} = {promedio_x:.4f}")
st.latex(rf"\bar{{Y}} = \frac{{\sum Y}}{{n}} = \frac{{{sum_y:.4f}}}{{{n}}} = {promedio_y:.4f}")

# Fórmula y sustitución de B1
st.subheader("Pendiente (β1)")
st.latex(r"\beta_1 = \frac{n(\sum XY) - (\sum X)(\sum Y)}{n(\sum X^2) - (\sum X)^2}")
if b1 is not None:
    st.latex(rf"\beta_1 = \frac{{{n}({sum_xy:.4f}) - ({sum_x:.4f})({sum_y:.4f})}}{{{n}({sum_x_cuadrado:.4f}) - ({sum_x:.4f})^2}}")
    st.latex(rf"\beta_1 = \frac{{{numerator_b1:.4f}}}{{{denominador:.4f}}} = {b1:.4f}")
else:
    st.error("Error: El denominador es 0. No se puede calcular β1.")

# Fórmula y sustitución de B0
st.subheader("Intercepto (β0)")
st.latex(r"\beta_0 = \bar{{Y}} - \beta_1\bar{{X}}")
if b0 is not None:
    st.latex(rf"\beta_0 = {promedio_y:.4f} - ({b1:.4f})({promedio_x:.4f}) = {b0:.4f}")
else:
    st.error("Error: No se puede calcular β0 debido a la indeterminación en β1.")

# Ecuación de la recta final
st.subheader("Ecuación de Regresión Final")
if b1 is not None and b0 is not None:
    signo = "+" if b1 >= 0 else "-"
    st.latex(rf"\hat{{Y}} = {b0:.4f} {signo} {abs(b1):.4f}X")

# # 7. Desglose de Errores Uno por Uno
st.header("5. Cálculo de Residuos Uno por Uno")
st.write("Fórmulas base: $e = Y - \\hat{{Y}}$ | $e^2 = (Y - \\hat{{Y}})^2$")

if b1 is not None and b0 is not None:
    for i in range(n):
        st.markdown(f"***Muestra {i+1}:***")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.latex(rf"e_{{{i+1}}} = {y_values[i]:.4f} - {y_estimadas[i]:.4f} = {errores[i]:.4f}")
        with col_col_e2:
            st.latex(rf"e_{{{i+1}}}^2 = ({errores[i]:.4f})^2 = {errores_cuadrado[i]:.4f}")

    st.subheader("Sumatorias de Errores")
    col_sum1, col_sum2 = st.columns(2)
    with col_sum1:
        st.latex(rf"\sum e = {sum_errores:.4f}")
    with col_sum2:
        st.latex(rf"\sum e^2 = {sum_errores_cuadrado:.4f}")

# # 8. Evaluación del Modelo (MAE, MSE, RMSE)
st.header("6. Métricas de Evaluación de Errores Globales")

if b1 is not None and b0 is not None:
    err_col1, err_col2, err_col3 = st.columns(3)
    with err_col1:
        st.metric(label="MAE", value=f"{mae:.4f}")
    with err_col2:
        st.metric(label="MSE", value=f"{mse:.4f}")
    with err_col3:
        st.metric(label="RMSE", value=f"{rmse:.4f}")

    st.subheader("Fórmulas y Sustitución de Métricas")

    st.write("***MAE (Error Absoluto Medio):***")
    st.latex(rf"MAE = \frac{{\sum |e|}}{{n}} = \frac{{{sum_errores_abs:.4f}}}{{{n}}} = {mae:.4f}")

    st.write("***MSE (Error Cuadrático Medio):***")
    st.latex(rf"MSE = \frac{{\sum e^2}}{{n}} = \frac{{{sum_errores_cuadrado:.4f}}}{{{n}}} = {mse:.4f}")

    st.write("***RMSE (Raíz del Error Cuadrático Medio):***")
    st.latex(rf"RMSE = \sqrt{{MSE}} = \sqrt{{{mse:.4f}}} = {rmse:.4f}")
else:
    st.error("No se pueden calcular las métricas debido a errores en los coeficientes.")
