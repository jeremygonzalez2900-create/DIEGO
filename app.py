import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Red de Conexiones de Usuarios", page_icon="🕸️", layout="wide"
)

# Inicializar estructura de datos en session_state
# 'usuarios': Diccionario donde la llave es el nombre y el valor es una lista de sus conexiones
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "Admin Principal": [
            "Carlos Pérez",
            "Ana Gómez",
        ]  # Ejemplo inicial de red
    }

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = "Admin Principal"

# Diseño en dos columnas
col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.header("⚙️ Gestión de Usuarios y Conexiones")

    # 1. Crear / Registrar un nuevo usuario global en el sistema
    st.subheader("1. Registrar nuevo usuario en la red")
    with st.form("form_nuevo_usuario"):
        nuevo_user = st.text_input("Nombre del nuevo usuario")
        btn_crear = st.form_submit_button("Crear Usuario")

        if btn_crear:
            if nuevo_user.strip():
                if nuevo_user not in st.session_state.usuarios:
                    st.session_state.usuarios[nuevo_user] = []
                    st.success(f"¡Usuario '{nuevo_user}' registrado con éxito!")
                    st.rerun()
                else:
                    st.warning("Ese usuario ya existe en el sistema.")
            else:
                st.error("Ingresa un nombre válido.")

    st.markdown("---")

    # 2. Seleccionar el usuario principal actual con el que quieres trabajar
    st.subheader("2. Seleccionar tu Usuario Principal")
    lista_nombres = list(st.session_state.usuarios.keys())

    if lista_nombres:
        usuario_seleccionado = st.selectbox(
            "Trabajar como:",
            options=lista_nombres,
            index=lista_nombres.index(st.session_state.usuario_activo)
            if st.session_state.usuario_activo in lista_nombres
            else 0,
        )

        if usuario_seleccionado != st.session_state.usuario_activo:
            st.session_state.usuario_activo = usuario_seleccionado
            st.rerun()

        st.info(f"👤 Usuario principal actual: **{st.session_state.usuario_activo}**")

        # 3. Conectar este usuario principal con otro usuario ya existente
        st.subheader(
            f"3. Agregar conexión a '{st.session_state.usuario_activo}'"
        )

        # Filtrar opciones para no conectarse a sí mismo ni repetir conexiones ya agregadas
        conexiones_actuales = st.session_state.usuarios[
            st.session_state.usuario_activo
        ]
        candidatos = [
            u
            for u in lista_nombres
            if u != st.session_state.usuario_activo and u not in conexiones_actuales
        ]

        if candidatos:
            with st.form("form_conectar"):
                a_conectar = st.selectbox(
                    "Selecciona a quién conectar a la derecha", options=candidatos
                )
                btn_conectar = st.form_submit_button("Conectar usuario")

                if btn_conectar:
                    st.session_state.usuarios[
                        st.session_state.usuario_activo
                    ].append(a_conectar)
                    st.success(
                        f"¡ '{a_conectar}' ahora está conectado a {st.session_state.usuario_activo}!"
                    )
                    st.rerun()
        else:
            st.caption(
                "No hay más usuarios disponibles para conectar directamente (o ya están todos conectados)."
            )
    else:
        st.warning("No hay usuarios registrados todavía.")

# Columna Derecha: Visualización de Conexiones en Cadena
with col_der:
    st.header("🔗 Red de Conexiones en Común")

    if st.session_state.usuario_activo:
        principal = st.session_state.usuario_activo
        st.markdown(
            f"### Usuario Principal: <span style='color: #4CAF50;'>{principal}</span>",
            unsafe_allow_html=True,
        )

        conexiones_directas = st.session_state.usuarios.get(principal, [])

        if not conexiones_directas:
            st.info(
                f"**{principal}** aún no tiene conexiones registradas a su derecha. ¡Agrégalas desde la izquierda!"
            )
        else:
            st.write(
                "#### Conexiones Directas (Nivel 1) y sus sub-conexiones (Nivel 2):"
            )

            for idx, conn in enumerate(conexiones_directas, start=1):
                with st.container(border=True):
                    # Mostrar la conexión directa a la derecha
                    st.markdown(f"**➡️ 1.{idx} Conectado Directo: {conn}**")

                    # Verificar si ESTA conexión a su vez tiene otras conexiones (conexiones de las conexiones)
                    sub_conexiones = st.session_state.usuarios.get(conn, [])

                    if sub_conexiones:
                        st.markdown(
                            f"<div style='margin-left: 20px; border-left: 2px solid #ddd; padding-left: 10px;'>",
                            unsafe_allow_html=True,
                        )
                        st.caption(
                            f"Red de **{conn}** (Conexiones secundarias):"
                        )
                        for sub_idx, sub_c in enumerate(
                            sub_conexiones, start=1
                        ):
                            st.markdown(
                                f"&nbsp;&nbsp;&nbsp;&nbsp;↳ 🔗 {sub_idx}. {sub_c}"
                            )
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"<div style='margin-left: 20px;'><span style='color: gray; font-size: 0.85em;'>Sin conexiones adicionales registradas para {conn}.</span></div>",
                            unsafe_allow_html=True,
                        )

        st.markdown("---")
        st.subheader("💡 ¿Cómo seguir expandiendo?")
        st.write(
            "1. Ve al panel izquierdo, cambia el **'Usuario Principal'** seleccionando a una de tus conexiones (ej. a *Carlos Pérez*)."
        )
        st.write(
            "2. Agrégale conexiones propias a ese usuario. Al hacerlo, verás cómo se despliegan en cadena a la derecha."
        )
    else:
        st.info("Selecciona o crea un usuario principal.")
