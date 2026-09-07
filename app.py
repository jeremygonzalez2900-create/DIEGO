import streamlit as st
import pandas as pd
import math

# Configuración del título y tema de la aplicación
st.set_page_config(page_title="Calculadora de Regresión Lineal", layout="wide", page_icon="📊")

st.title("📊 Calculadora de Regresión Lineal Completa")
st.caption("Herramienta interactiva para análisis, ajuste de línea y desarrollo matemático paso a paso.")

# Inicialización del estado de sesión
if "x_data" not in st.session_state:
    st.session_state.x_data = [1.0, 2.0, 3.0, 4.0, 5.0]
if "y_data" not in st.session_state:
    st.session_state.y_data = [2.0, 6.0, 10.0, 16.0, 23.0]

# --- SIDEBAR: Entrada de Datos ---
with st.sidebar:
    st.header("⚙️ Configuración de Datos")
    n_default = len(st.session_state.x_data)
    n = st.number_input("Número de muestras (n):", min_value=1, value=n_default, step=1)

    # Ajustar listas de estado al cambiar 'n'
    if len(st.session_state.x_data) < n:
        st.session_state.x_data.extend([0.0] * (n - len(st.session_state.x_data)))
        st.session_state.y_data.extend([0.0] * (n - len(st.session_state.y_data)))
    elif len(st.session_state.x_data) > n:
        st.session_state.x_data = st.session_state.x_data[:n]
        st.session_state.y_data = st.session_state.y_data[:n]

    st.subheader("Tabla de Entrada")
    df_input = pd.DataFrame({
        "X": st.session_state.x_data,
        "Y": st.session_state.y_data
    })
    edited_df = st.data_editor(df_input, num_rows="fixed", key="tabla_input", use_container_width=True)
    
    x_values = edited_df["X"].tolist()
    y_values = edited_df["Y"].tolist()
    
    st.session_state.x_data = x_values
    st.session_state.y_data = y_values

# --- CÁLCULOS MATEMÁTICOS ---
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

# Cálculo de Errores y Estimaciones
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

# --- ESTRUCTURA DE PESTAÑAS (TABS) ---
tab1, tab2, tab3 = st.tabs(["📋 Resumen y Tablas", "📐 Desarrollo de Parámetros", "🔍 Análisis de Residuos"])

with tab1:
    st.subheader("Resultados Principales")
    
    # Ecuación Destacada
    if b1 is not None and b0 is not None:
        signo = "+" if b1 >= 0 else "-"
        st.info(f"### Ecuación Modelo:  $\\hat{{Y}} = {b0:.4f} {signo} {abs(b1):.4f}X$")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Sumatoria X (∑X)", f"{sum_x:.4f}")
    col_m2.metric("Sumatoria Y (∑Y)", f"{sum_y:.4f}")
    col_m3.metric("Promedio X (X̄)", f"{promedio_x:.4f}")
    col_m4.metric("Promedio Y (Ȳ)", f"{promedio_y:.4f}")

    st.divider()
    
    st.subheader("Tabla General de Desarrollo")
    df_resultados = pd.DataFrame({
        "Muestra": [f"#{i+1}" for i in range(n)],
        "X": x_values,
        "Y": y_values,
        "X²": x_cuadrado,
        "X · Y": x_por_y,
        "ŷ (Estimado)": y_estimadas,
        "Error (e)": errores
    })
    st.dataframe(df_resultados, use_container_width=True)

with tab2:
    st.subheader("1. Promedios")
    c1, c2 = st.columns(2)
    with c1:
        st.latex(r"\bar{X} = \frac{\sum X}{n} = \frac{" + f"{sum_x:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_x:.4f}")
    with c2:
        st.latex(r"\bar{Y} = \frac{\sum Y}{n} = \frac{" + f"{sum_y:.4f}" + "}{" + f"{n}" + "} = " + f"{promedio_y:.4f}")

    st.divider()

    st.subheader("2. Pendiente ($B_1$) e Intercepto ($B_0$)")
    if b1 is not None:
        st.latex(r"B_1 = \frac{n\sum(XY) - (\sum X)(\sum Y)}{n\sum(X^2) - (\sum X)^2}")
        st.latex(r"B_1 = \frac{" + f"{n}({sum_xy:.4f}) - ({sum_x:.4f})({sum_y:.4f})" + "}{" + f"{n}({sum_x_cuadrado:.4f}) - ({sum_x:.4f})^2" + "} = " + f"{b1:.4f}")
        
        st.latex(r"B_0 = \bar{Y} - B_1\bar{X}")
        st.latex(r"B_0 = " + f"{promedio_y:.4f} - ({b1:.4f})({promedio_x:.4f}) = {b0:.4f}")
    else:
        st.error("Error: Indeterminación por división entre 0.")

with tab3:
    st.subheader("Desglose Muestra por Muestra")
    
    if b1 is not None and b0 is not None:
        for i in range(n):
            # Resaltado especial para la segunda muestra
            if i == 1:
                with st.expander(f"📌 **Muestra {i+1} (X = {x_values[i]}, Y = {y_values[i]}) - DETALLE COMPLETO**", expanded=True):
                    st.markdown("#### ¿De dónde sale el valor estimado $\\hat{Y}_2$?")
                    st.write(f"Sustituimos el valor de entrada **$X_2 = {x_values[i]}$** en la ecuación del modelo:")
                    st.latex(r"\hat{Y}_2 = B_0 + B_1(X_2)")
                    st.latex(f"\\hat{{Y}}_2 = {b0:.4f} + ({b1:.4f} \\times {x_values[i]:.4f})")
                    st.latex(f"\\hat{{Y}}_2 = {y_estimadas[i]:.4f}")
                    
                    st.markdown("---")
                    st.markdown("#### Cálculo del Residuo y Residuo al Cuadrado:")
                    col_det1, col_det2 = st.columns(2)
                    with col_det1:
                        st.latex(f"e_2 = Y_2 - \\hat{{Y}}_2")
                        st.latex(f"e_2 = {y_values[i]:.4f} - {y_estimadas[i]:.4f} = {errores[i]:.4f}")
                    with col_det2:
                        st.latex(f"e_2^2 = ({errores[i]:.4f})^2 = {errores_cuadrado[i]:.4f}")
            else:
                with st.expander(f"Muestra {i+1} (X = {x_values[i]}, Y = {y_values[i]})", expanded=False):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown("**Valor Estimado y Residuo:**")
                        st.latex(f"\\hat{{Y}}_{{{i+1}}} = {b0:.4f} + ({b1:.4f} \\times {x_values[i]:.4f}) = {y_estimadas[i]:.4f}")
                        st.latex(f"e_{{{i+1}}} = {y_values[i]:.4f} - {y_estimadas[i]:.4f} = {errores[i]:.4f}")
                    with col_e2:
                        st.markdown("**Residuo Cuadrático:**")
                        st.latex(f"e_{{{i+1}}}^2 = ({errores[i]:.4f})^2 = {errores_cuadrado[i]:.4f}")

        st.divider()
        
        # Métricas Globales
        st.subheader("Métricas de Error Global")
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("MAE", f"{mae:.4f}")
        g2.metric("MSE", f"{mse:.4f}")
        g3.metric("RMSE", f"{rmse:.4f}")
        g4.metric("RMSE / MAE", f"{rmse_mae_ratio:.4f}")

        with st.expander("Ver Fórmulas Globables Evaluadas"):
            st.latex(r"MAE = \frac{\sum |e|}{n} = \frac{" + f"{sum_errores_abs:.4f}" + "}{" + f"{n}" + "} = " + f"{mae:.4f}")
            st.latex(r"MSE = \frac{\sum e^2}{n} = \frac{" + f"{sum_errores_cuadrado:.4f}" + "}{" + f"{n}" + "} = " + f"{mse:.4f}")
            st.latex(r"RMSE = \sqrt{MSE} = \sqrt{" + f"{mse:.4f}" + "} = " + f"{rmse:.4f}")
