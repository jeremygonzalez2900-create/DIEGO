import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Registro y Conexión de Usuarios", page_icon="👥", layout="wide"
)

# Inicializar el estado de la sesión para guardar los usuarios y la sesión actual
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = []

if "usuario_conectado" not in st.session_state:
    st.session_state.usuario_conectado = None

# Diseño en dos columnas: Izquierda (Formulario/Acción), Derecha (Usuarios en común/Conectados)
col_izq, col_der = st.columns([1, 1], gap="large")

with col_izq:
    st.header("Portal de Usuarios")

    # Si no hay un usuario conectado, mostramos opciones de Registro / Iniciar Sesión
    if st.session_state.usuario_conectado is None:
        st.subheader("Registro de Usuario")
        with st.form("form_registro"):
            nuevo_nombre = st.text_input("Nombre de usuario")
            nuevo_correo = st.text_input("Correo electrónico")
            submit_registro = st.form_submit_button("Registrarse y Conectar")

            if submit_registro:
                if nuevo_nombre.strip() and nuevo_correo.strip():
                    # Verificar si ya existe
                    existente = any(
                        u["nombre"] == nuevo_nombre
                        for u in st.session_state.usuarios_registrados
                    )
                    if not existente:
                        nuevo_usuario = {
                            "nombre": nuevo_nombre,
                            "correo": nuevo_correo,
                        }
                        # Guardar en la lista global de usuarios
                        st.session_state.usuarios_registrados.append(
                            nuevo_usuario
                        )
                        # Conectar automáticamente al usuario recién registrado
                        st.session_state.usuario_conectado = nuevo_nombre
                        st.success(
                            f"¡Bienvenido, {nuevo_nombre}! Te has registrado y conectado con éxito."
                        )
                        st.rerun()
                    else:
                        st.error(
                            "Ese nombre de usuario ya está registrado. Elige otro."
                        )
                else:
                    st.warning(
                        "Por favor completa todos los campos para registrarte."
                    )

        st.markdown("---")
        st.subheader("Iniciar Sesión (Usuario Existente)")
        with st.form("form_login"):
            usuario_login = st.selectbox(
                "Selecciona tu usuario",
                options=[
                    u["nombre"]
                    for u in st.session_state.usuarios_registrados
                ],
            )
            submit_login = st.form_submit_button("Conectar")

            if submit_login and usuario_login:
                st.session_state.usuario_conectado = usuario_login
                st.success(f"Te has conectado como: {usuario_login}")
                st.rerun()

    else:
        # Si ya está conectado
        st.success(
            f"🟢 Sesión activa: **{st.session_state.usuario_conectado}**"
        )

        # Botón para cerrar sesión
        if st.button("Cerrar Sesión"):
            st.session_state.usuario_conectado = None
            st.rerun()

        st.info(
            "Estás dentro de la red. Puedes ver los usuarios registrados en común a la derecha."
        )

# Columna Derecha: Panel de Usuarios en Común (Conectados / Red)
with col_der:
    st.header("🌐 Comunidad en Común")
    st.write(
        "Aquí aparecen todos los usuarios que se han registrado y forman parte de la red:"
    )

    total_usuarios = len(st.session_state.usuarios_registrados)
    st.metric(label="Total de usuarios registrados", value=total_usuarios)

    st.markdown("---")

    if total_usuarios == 0:
        st.info(
            "Aún no hay usuarios registrados. ¡Sé el primero en registrarte a la izquierda!"
        )
    else:
        # Mostrar la lista en formato de tarjetas o tabla limpia
        for idx, user in enumerate(
            st.session_state.usuarios_registrados, start=1
        ):
            # Resaltar si es el usuario conectado actualmente
            is_me = user["nombre"] == st.session_state.usuario_conectado

            with st.container(border=True):
                col_info1, col_info2 = st.columns([3, 1])
                with col_info1:
                    st.markdown(f"**👤 {idx}. {user['nombre']}**")
                    st.caption(f"📧 {user['correo']}")
                with col_info2:
                    if is_me:
                        st.markdown(
                            "<p style='color:green; font-weight:bold; text-align:right;'>Tú</p>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            "<p style='color:gray; text-align:right;'>Conectado</p>",
                            unsafe_allow_html=True,
                        )
