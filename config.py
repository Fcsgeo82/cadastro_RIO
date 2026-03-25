# =============================================================
# config.py — Configurações centrais da aplicação
# Dataset: CGR_Cadastro_Sistema_RIO
# =============================================================

import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "rj-smtr-dev")
DATASET_ID = "CGR_Cadastro_Sistema_RIO"


def get_client() -> bigquery.Client:
    """
    Retorna cliente BigQuery autenticado via session state.
    """
    if "bq_client" not in st.session_state or st.session_state.bq_client is None:
        raise ValueError("Cliente BigQuery não autenticado. Faça upload da chave service account.")
    return st.session_state.bq_client
