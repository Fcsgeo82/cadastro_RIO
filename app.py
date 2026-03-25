# =============================================================
# App.py — Cadastro de Linhas com ADC (Application Default Credentials)
# =============================================================

import os
import streamlit as st
from google.cloud import bigquery
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request

import mod_cadastro
import mod_cadastro_ref
import mod_consulta

# --- Configuração da página ---
st.set_page_config(
    page_title="Linhas de Ônibus",
    page_icon="🚌",
    layout="wide",
)

# --- Estado global ---
if "bq_client" not in st.session_state:
    st.session_state.bq_client = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None


def autenticar_gcp_adc():
    """Autentica no GCP usando Application Default Credentials (ADC)."""
    try:
        # Tenta usar ADC (automático quando você fez gcloud auth application-default login)
        credentials, project_id = google_auth_default(scopes=[
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform"
        ])

        # Criar cliente BigQuery
        st.session_state.bq_client = bigquery.Client(project="rj-smtr-dev", credentials=credentials)

        # Obter informações do usuário/credencial
        user_email = "autenticado@google.com"
        user_name = "Usuário"

        if hasattr(credentials, 'service_account_email'):
            # Se for service account
            user_email = credentials.service_account_email
            user_name = "Service Account"
        else:
            # Para ADC de usuário, tentar extrair info
            try:
                user_email = getattr(credentials, 'email', user_email)
                user_name = getattr(credentials, 'name', 'Usuário Google')
            except:
                pass

        st.session_state.user_info = {
            "email": user_email,
            "name": user_name,
            "project": project_id
        }

        return True
    except Exception as e:
        st.error(f"❌ Erro na autenticação GCP/ADC: {e}")
        st.info("""
        Execute este comando no terminal para configurar ADC:
        ```
        gcloud auth application-default login
        ```
        """)
        return False


# --- Autenticação via ADC (Application Default Credentials) ---
if st.session_state.bq_client is None:
    with st.container():
        st.markdown("## 🔐 Autenticando...")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if autenticar_gcp_adc():
                st.success("✅ Autenticado com sucesso!")
            else:
                st.stop()

# --- Usuário autenticado - mostrar info na sidebar ---
with st.sidebar:
    st.markdown("## 👋 Bem-vindo")
    if st.session_state.user_info:
        st.markdown(f"**{st.session_state.user_info.get('name', 'Usuário')}**")
        st.caption(f"📧 {st.session_state.user_info.get('email', 'N/A')}")
        st.caption(f"📦 Projeto: {st.session_state.user_info.get('project', 'rj-smtr-dev')}")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.bq_client = None
            st.session_state.user_info = None
            st.rerun()

# --- CSS customizado ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #1a3a5c 0%, #2d6a9f 100%);
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 18px;
}
.app-header h1 {
    color: white !important;
    font-size: 1.8rem !important;
    margin: 0 !important;
}
.app-header p {
    color: rgba(255,255,255,0.75);
    margin: 4px 0 0;
    font-size: 0.9rem;
}
.header-icon { font-size: 2.5rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #dde3ec;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 22px;
    border-radius: 8px 8px 0 0;
    color: #6b7a99;
}
.stTabs [aria-selected="true"] {
    color: #1a3a5c !important;
    border-bottom: 3px solid #f07d00 !important;
}

/* Botão primário */
.stButton > button[kind="primary"] {
    background: #1a3a5c;
    border: none;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    padding: 10px 24px;
    transition: background 0.2s;
}
.stButton > button[kind="primary"]:hover {
    background: #2d6a9f !important;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    border-radius: 7px !important;
    border: 1px solid #dde3ec !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #2d6a9f !important;
    box-shadow: 0 0 0 3px rgba(45,106,159,0.15) !important;
}

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Footer */
footer { visibility: hidden; }
.custom-footer {
    text-align: center;
    color: #6b7a99;
    font-size: 0.8rem;
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid #dde3ec;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="app-header">
    <span class="header-icon">🚌</span>
    <div>
        <h1>Sistema de Linhas de Ônibus</h1>
        <p>Cadastro e Consulta via BigQuery</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Abas principais ---
aba_cadastro, aba_ref, aba_consulta = st.tabs([
    "➕  Cadastrar Linha",
    "🗂️  Tabelas de Referência",
    "🔍  Consultar Linhas",
])

with aba_cadastro:
    mod_cadastro.render()

with aba_ref:
    mod_cadastro_ref.render()

with aba_consulta:
    mod_consulta.render()

# --- Footer ---
st.markdown(
    '<div class="custom-footer">Sistema de Linhas de Ônibus • Streamlit + BigQuery + ADC</div>',
    unsafe_allow_html=True
)
