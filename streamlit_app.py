import streamlit as st
import google_auth as ga
import bd_funcs as db

#Llamados iniciales [BD, Estados de sesión, Place holder de titulo]
st.set_page_config(page_title="IA CapTech", page_icon=":robot_face:")
db.create_db()
if 'page_title' not in st.session_state:
    st.session_state.page_title = 'Login'
if 'page_name' not in st.session_state:
    st.session_state.page_name = 'Login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
title_placeholder = st.empty()

#Mostrar datos en la sidebar
def sidebar_data(title, message):
    st.sidebar.title(title)
    st.sidebar.write(message)

# Función para actualizar el título
def update_title():
    title_placeholder.title(st.session_state.page_title)

# Mostrar el título actual desde session_state
update_title()

def go_to_page(page_name):
    # Actualizar el título en session_state
    st.session_state.page_title = page_name
    update_title()  # Actualizar el título visible

# Función de autenticación que solo se ejecuta si no hay sesión activa
def add_auth(
    login_button_text: str = "Login with Google",
    login_button_color: str = "#3383FF",
    login_sidebar: bool = True,
    page_name: str = 'Inicio'
):
    # Autenticación del usuario si no hay una sesión activa
    user_email = ga.get_logged_in_user_email()

    # Si no hay email registrado, mostrar botón de login
    if not user_email:
        ga.show_login_button(
            text=login_button_text, color=login_button_color, sidebar=login_sidebar
        )
        st.stop()
    else:
        # Si el usuario está loggeado, almacenar el estado de login
        sidebar_data("Inicio", f"Sesión activa para {st.session_state.email}.")
        st.session_state.logged_in = True
        st.session_state.email = user_email
        # Guardar la sesión actual en la base de datos
        db.save_session(user_email, page_name)
        # Redirigir al usuario a la página deseada
        go_to_page(page_name)
        # Mostrar el email de usuario
        st.write(f"Email del usuario: {user_email}")

    # Botón de logout en la barra lateral
    if st.sidebar.button("Logout", type="primary"):
        # Al hacer logout, limpiar el estado de sesión
        if 'email' in st.session_state:
            #Elimina la sesion de la DB y del session_state
            db.delete_session(st.session_state.email)
            del st.session_state.email
        #Login en false
        st.session_state.logged_in = False
        st.session_state.page_title = 'Login'  # Establecer el título a 'Login'
        go_to_page('Login')  # Cambiar el título visible
        # Forzar el reinicio de la aplicación
        st.rerun()

# Primero verificar si hay una sesión activa en la base de datos
if not db.check_session():
    # Si no hay sesión, proceder con la autenticación
    add_auth(page_name='Inicio')
else:
    # Si hay una sesión activa, restaurarla y muestrala
    sidebar_data("Inicio", f"Sesión activa para {st.session_state.email}.")
    go_to_page(st.session_state.page_name)
    #Si hay sesion activa, mostrar boton de logout
    if st.sidebar.button("Logout", type="primary"):
        # Al hacer logout, limpiar el estado de sesión y elimina de la DB
        if 'email' in st.session_state:
            db.delete_session(st.session_state.email)
            del st.session_state.email
        st.session_state.logged_in = False
        st.session_state.page_title = 'Login'  # Establecer el título a 'Login'
        go_to_page('Login')  # Cambiar el título visible
        # Forzar el reinicio de la aplicación
        st.rerun()