import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configuração
st.set_page_config(
    page_title="Coleta+ 🐾",
    page_icon="🔍",
    layout="wide"
)

# ⚠️ Use SOMENTE o ID (não a URL completa)
SHEET_ID = "14iqQIJS11Fq7B1jPVxI_7Pkl4FMn2buu"

@st.cache_data(ttl=300)
def load_data():
    try:
        # URL correta para planilhas públicas
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        response = requests.get(url)
        response.raise_for_status()  # Verifica erros
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        st.error(f"Erro ao carregar: {str(e)}")
        return pd.DataFrame()

# Interface
dados = load_data()

if not dados.empty:
    st.title("Catálogo de Exames")
    
    # Barra de busca
    termo = st.text_input("🔍 Buscar:", placeholder="Digite o nome do exame")
    
    # Filtro (atenção à indentação!)
    if termo:
        resultados = dados[
            dados['EXAMES'].str.contains(termo, case=False, na=False) |
            dados['CONTEÚDO'].str.contains(termo, case=False, na=False)
        ]
    else:
        resultados = dados
