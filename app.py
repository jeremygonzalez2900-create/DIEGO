import streamlit as st
import pandas as pd
import math

# ---------------------------------------------------------
# Configuración inicial de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Calculadora de Regresión Lineal", 
    layout="wide", 
    page_icon="📊"
)

st.title("📊 Calculadora de Regresión Lineal Completa")
st.caption("Herramienta paso a paso para el análisis, cálculo de coeficientes y evaluación de residuos.")

# ---------------------------------------------------------
# Estado de Sesión
# ---------------------------------------------------------
if "x_data" not in st.session_state:
    st.session_state.x_data = [1.0, 2.0, 3.0, 4.0, 5.0]
if "y_data" not in st.session_state:
    st.session_state.y_data = [2.0, 6.0, 10.0, 16.0, 23.0]

# ---------------------------------------------------------
# 1. Configuración de Muestra y Tablas de Datos
# ---------------------------------------------------------
st.header("1. Configuración e Ingreso de Datos")

n_default = len(st.session_state.x_data)
n = st.number_input("Número de muestras (n):", min_value=1, value=n_default, step=1)

# Ajustar listas de estado al cambiar 'n'
if len(st.session_state.x_data) < n:
    st.session_state.x_data.extend([0.0] * (n - len(st.session_state.x_data)))
    st.session_state.y_data.extend([0.0] * (n - len(st.session_state.y_data)))
elif len(st.session_state.x_data) > n:
    st.session_state.x_data = st.session_state.x_data[:n]
    st.session_state.y_data = st.session_state.y_data[:n]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Valores de X")
    df_x_init = pd.DataFrame({"X": st.session_state.x_data})
    edited_df_x = st.data_editor(df_x_init, num_rows="fixed", key="tabla_x", use_container_width=True)
    x_values = edited_df_x["X"].tolist()

with col2:
    st.subheader("Valores de Y")
    df_y_init = pd.DataFrame({"Y": st.session_state.y_data})
    edited_df_y = st.data_editor(df_y_init, num_rows="fixed", key="tabla_y", use_container_width=True)
    y_values = edited_df_y["Y"].tolist()

# Actualizar el estado de sesión
st.session_state.x_data = x_values
st.session_state.y_data = y_values

# ---------------------------------------------------------
# 2. Cálculos Matemáticos Iniciales
# ---------------------------------------------------------
sum_x = sum(x_values)
sum_y = sum(y_values)
promedio_x = sum_x / n if n > 0 else 0
promedio_y = sum_y / n if n > 0 else 0

x_cuadrado = [x ** 2 for x in x_values]
sum_x_cuadrado = sum(x_cuadrado)

x_por_y = [x * y for x, y in zip(x_values, y_values)]
sum_xy = sum(x_por_y)

denominador = (n * sum_x_cuadrado) - (sum_x ** 2)
numerador_b1 = (n * sum_xy) - (sum_x * sum_y)

if denominador != 0:
    b1 = numerador_b1 / denominador
    b0 = promedio_y - (b1 * promedio_x)
else:
    b1 = None
    b0 = None

# ---------------------------------------------------------
# 3. Cálculo de Errores y Métricas
# ---------------------------------------------------------
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

mae = sum_errores_abs / n if n > 0 else 0
mse = sum_errores_cuadrado / n if n > 0 else 0
rmse = math.sqrt(mse)
rmse_mae_ratio = (rmse / mae) if mae > 0 else 0.0

st.divider()

# ---------------------------------------------------------
# 4. Mostrar Resultados Numéricos
# ---------------------------------------------------------
st.header("2. Resultados y Cálculos")

df_resultados = pd.DataFrame({
    "Muestra": [f"#{i+1}" for i in range(n)],
    "X": x_values,
    "Y": y_values,
    "X²": x_cuadrado,
    "X · Y": x_por_y,
    "ŷ (Estimado)": y_estimadas
})
st.subheader("Tabla de Desarrollo")
st.dataframe(df_resultados, use_container_width=True)

st.write("")

# Resumen numérico ordenado en tarjetas
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
metric_col1.metric("Sumatoria X (∑X)", f"{sum_x:.4f}")
metric_col2.metric("Sumatoria Y (∑Y)", f"{sum_y:.4f}")
metric_col3.metric("Sumatoria X² (∑X²)", f"{sum_x_cuadrado:.4f}")
metric_col4.metric("Promedio X (X̄)", f"{promedio_x:.4f}")
metric_col5.metric("Promedio Y (Ȳ)", f"{promedio_y:.4f}")

st.divider()

# ---------------------------------------------------------
# 5. Desarrollo de Fórmulas Paso a Paso
# ---------------------------------------------------------
st.header("3. Desarrollo de Fórmulas (Sustitución)")

with st.container():
    st.subheader("Promedios")
    c1, c2 = st.columns(2)
    with c1:
        st.latex(r"\bar{X} = \frac{\sum X}{n} = \frac{" + f"{sum_x:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_x:.4f}")
    with c2:
        st.latex(r"\bar{Y} = \frac{\sum Y}{n} = \frac{" + f"{sum_y:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_y:.4f}")

st.subheader("Pendiente ($B_1$)")
st.latex(r"B_1 = \frac{n\sum(XY) - (\sum X)(\sum Y)}{n\sum(X^2) - (\sum X)^2}")
if b1 is not None:
    st.latex(r"B_1 = \frac{" + f"{n}({sum_xy:.4f}) - ({sum_x:.4f})({sum_y:.4f})" + "}{" + f"{n}({sum_x_cuadrado:.4f}) - ({sum_x:.4f})^2" + "}")
    st.latex(r"B_1 = \frac{" + f"{numerador_b1:.4f}" + "}{" + f"{denominador:.4f}" + "} = " + f"{b1:.4f}")
else:
    st.error("Error: El denominador es 0. No se puede calcular B1.")

st.subheader("Intercepto ($B_0$)")
st.latex(r"B_0 = \bar{Y} - B_1\bar{X}")
if b0 is not None:
    st.latex(r"B_0 = " + f"{promedio_y:.4f} - ({b1:.4f})({promedio_x:.4f}) = {b0:.4f}")

if b1 is not None and b0 is not None:
    signo = "+" if b1 >= 0 else "-"
    st.success(f"### Ecuación de Regresión Final:  $\\hat{{Y}} = {b0:.4f} {signo} {abs(b1):.4f}X$")

st.divider()

# ---------------------------------------------------------
# 6. Residuos Uno por Uno
# ---------------------------------------------------------
st.header("4. Cálculo de Residuos Uno por Uno")
st.caption("Fórmulas base: $e = Y - \\hat{Y}$  |  $e^2 = (Y - \\hat{Y})^2$")

if b1 is not None and b0 is not None:
    for i in range(n):
        st.markdown(f"**Muestra {i+1}:**")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.latex(f"e_{{{i+1}}} = {y_values[i]:.4f} - {y_estimadas[i]:.4f} = {errores[i]:.4f}")
        with col_e2:
            st.latex(f"e_{{{i+1}}}^2 = ({errores[i]:.4f})^2 = {errores_cuadrado[i]:.4f}")
    
    st.subheader("Sumatorias de Errores")
    col_sum1, col_sum2 = st.columns(2)
    with col_sum1:
        st.latex(r"\sum e = " + f"{sum_errores:.4f}")
    with col_sum2:
        st.latex(r"\sum e^2 = " + f"{sum_errores_cuadrado:.4f}")

    st.divider()

    # ---------------------------------------------------------
    # 7. Evaluación del Modelo (MAE, MSE, RMSE, RMSE / MAE)
    # ---------------------------------------------------------
    st.header("5. Métricas de Evaluación de Errores Globales")
    
    err_col1, err_col2, err_col3, err_col4 = st.columns(4)
    err_col1.metric(label="MAE", value=f"{mae:.4f}")
    err_col2.metric(label="MSE", value=f"{mse:.4f}")
    err_col3.metric(label="RMSE", value=f"{rmse:.4f}")
    err_col4.metric(label="RMSE / MAE", value=f"{rmse_mae_ratio:.4f}")

    st.subheader("Fórmulas y Sustitución de Métricas")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.write("**MAE (Error Absoluto Medio):**")
        st.latex(r"MAE = \frac{\sum |e|}{n} = \frac{" + f"{sum_errores_abs:.4f}" + "}{" + f"{n}" + "} = " + f"{mae:.4f}")
        
        st.write("**RMSE (Raíz del Error Cuadrático Medio):**")
        st.latex(r"RMSE = \sqrt{MSE} = \sqrt{" + f"{mse:.4f}" + "} = " + f"{rmse:.4f}")

    with col_m2:
        st.write("**MSE (Error Cuadrático Medio):**")
        st.latex(r"MSE = \frac{\sum e^2}{n} = \frac{" + f"{sum_errores_cuadrado:.4f}" + "}{" + f"{n}" + "} = " + f"{mse:.4f}")

        st.write("**Relación RMSE / MAE:**")
        if mae > 0:
            st.latex(r"\frac{RMSE}{MAE} = \frac{" + f"{rmse:.4f}" + "}{" + f"{mae:.4f}" + "} = " + f"{rmse_mae_ratio:.4f}")
        else:
            st.info("No se puede dividir entre cero (MAE = 0).")

else:
    st.error("No se pueden calcular las métricas debido a errores en los coeficientes.")
