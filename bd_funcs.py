import sqlite3
import streamlit as st

# Configuración inicial de la base de datos
def create_db():
    #Si no existe, crea el archivo 'sessions'
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            email TEXT PRIMARY KEY,
            page_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para guardar la sesión
def save_session(email, page_name):
    #Conecta al archivo 'sessions'
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    #Inserta el email y la pagina donde se quedó
    c.execute('''
        INSERT OR REPLACE INTO sessions (email, page_name)
        VALUES (?, ?)
    ''', (email, page_name))
    conn.commit()
    conn.close()

# Función para eliminar la sesión de la base de datos
def delete_session(email):
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('DELETE FROM sessions WHERE email = ?', (email,))
    conn.commit()
    conn.close()

    # Función para verificar y cargar la sesión
def check_session():
    if 'email' not in st.session_state:
        # Recuperar la sesión de la base de datos si no hay sesión en el session_state
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('SELECT email, page_name FROM sessions LIMIT 1')
        result = c.fetchone()
        conn.close()

        if result:
            # Restaurar el estado de sesión si hay una sesión en la base de datos
            st.session_state.email = result[0]
            st.session_state.page_name = result[1]
            st.session_state.logged_in = True
            return True
    return False