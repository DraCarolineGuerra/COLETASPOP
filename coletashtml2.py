import streamlit as st
import pandas as pd
from PIL import Image
import os

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================
st.set_page_config(
    page_title="Coleta+ 🐾",
    page_icon="🐾",
    layout="wide"
)

# ======================================
# FUNÇÃO PARA CARREGAR DADOS (SIMPLES!)
# ======================================
@st.cache_data
def load_data():
    """Carrega dados de uma planilha pública do Google Sheets"""
    try:
        # URL pública da sua planilha (formato CSV)
        sheet_id = "14iqQIJS11Fq7B1jPVxI_7Pkl4FMn2buu"  # ID da sua planilha
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        dados = pd.read_csv(url)
        dados.columns = dados.columns.str.strip()
        
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
            
        return dados
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 
                                   'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

# ... (mantenha as funções load_logo() e display_detalhes() do seu código original)

# ======================================
# INTERFACE PRINCIPAL (igual à anterior)
# ======================================
dados = load_data()

# Sidebar (mantenha igual)
with st.sidebar:
    logo = Image.open('logo_hospital.png') if os.path.exists('logo_hospital.png') else None
    if logo:
        st.image(logo, width=100)
    
    st.title("Coleta+ 🐾")
    termo_busca = st.text_input("🔍 Buscar exame:")

# ... (restante do seu código de exibição permanece igual)
