import streamlit as st
import requests
from datetime import datetime
from typing import Optional

# Configurações
BACKEND_URL = "http://localhost:8000"  # Altere se necessário
st.set_page_config(page_title="Workouts Tracker", layout="centered")

# Estado da sessão
if "auth" not in st.session_state:
    st.session_state.auth = {
        "token": None,
        "username": None,
        "logged_in": False
    }

# --- Funções de Autenticação ---
def register_user(username: str, password: str) -> bool:
    """Registra um novo usuário no backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 201:
            st.success("Usuário criado com sucesso! Faça login.")
            return True
        else:
            error_detail = response.json().get("detail", "Erro desconhecido")
            st.error(f"Falha no registro: {error_detail}")
            return False
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return False

def login_user(username: str, password: str) -> bool:
    """Autentica o usuário e armazena o token JWT"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/token",
            data={"username": username, "password": password, "grant_type": "password"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.auth = {
                "token": token_data["access_token"],
                "username": username,
                "logged_in": True
            }
            st.success("Login realizado!")
            return True
        else:
            st.error("Credenciais inválidas")
            return False
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return False

def logout():
    """Limpa a sessão"""
    st.session_state.auth = {
        "token": None,
        "username": None,
        "logged_in": False
    }
    st.success("Você foi desconectado")

def get_auth_header() -> Optional[dict]:
    """Retorna os headers de autenticação"""
    if st.session_state.auth["token"]:
        return {"Authorization": f"Bearer {st.session_state.auth['token']}"}
    return None

# --- Páginas ---
def login_register_page():
    """Página de login/registro"""
    tab1, tab2 = st.tabs(["Login", "Registrar"])
    
    with tab1:
        with st.form("login_form"):
            st.header("Login")
            username = st.text_input("Username")
            password = st.text_input("Senha", type="password")
            
            if st.form_submit_button("Entrar"):
                if login_user(username, password):
                    st.rerun()
    
    with tab2:
        with st.form("register_form"):
            st.header("Registrar Novo Usuário")
            new_username = st.text_input("Escolha um username")
            new_password = st.text_input("Crie uma senha", type="password")
            confirm_password = st.text_input("Confirme a senha", type="password")
            
            if st.form_submit_button("Criar Conta"):
                if new_password == confirm_password:
                    register_user(new_username, new_password)
                else:
                    st.error("As senhas não coincidem")

def main_app_page():
    """Página principal após login"""
    st.title(f"📊 Workouts Dashboard - Bem-vindo, {st.session_state.auth['username']}!")
    
    # Botão de logout
    if st.button("Logout"):
        logout()
        st.rerun()
    
    # Seção de upload de workouts
    with st.expander("📤 Upload de Arquivo FIT"):
        uploaded_file = st.file_uploader("Selecione seu arquivo .FIT", type="fit")
        if uploaded_file and st.button("Enviar"):
            try:
                headers = get_auth_header()
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(
                    f"{BACKEND_URL}/upload-workout/",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    st.success("Workout processado com sucesso!")
                else:
                    st.error(f"Erro: {response.json().get('detail', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"Falha no upload: {str(e)}")
    
    # Seção de visualização de dados
    st.header("Seus Workouts")
    try:
        headers = get_auth_header()
        response = requests.get(f"{BACKEND_URL}/workouts/", headers=headers)
        
        if response.status_code == 200:
            workouts = response.json()
            if workouts:
                st.dataframe(workouts)
                
                # Gráficos (exemplo simples)
                if len(workouts) > 0:
                    import pandas as pd
                    import plotly.express as px
                    
                    df = pd.DataFrame(workouts)
                    fig = px.bar(df, x="start_time", y="distance", 
                                color="activity_type", title="Distância por Atividade")
                    st.plotly_chart(fig)
            else:
                st.info("Nenhum workout encontrado. Faça upload de arquivos FIT.")
        else:
            st.error(f"Erro ao buscar workouts: {response.json().get('detail', 'Erro desconhecido')}")
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")

# --- Roteamento ---
if not st.session_state.auth["logged_in"]:
    login_register_page()
else:
    main_app_page()