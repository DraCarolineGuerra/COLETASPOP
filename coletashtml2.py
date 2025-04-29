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
@st.cache_data
def load_data():
    """Carrega os dados de um arquivo local Excel"""
    try:
        dados = pd.read_excel("exames.xlsx")
        dados.columns = dados.columns.str.strip()  # Remove espaços extras nos nomes das colunas
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados locais:\n{e}")
        return pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 
                                     'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

dados = load_data()

# Sidebar (mantenha igual)
with st.sidebar:
    logo = Image.open('logo_hospital.png') if os.path.exists('logo_hospital.png') else None
    if logo:
        st.image(logo, width=100)
    
    st.title("Coleta+ 🐾")
    termo_busca = st.text_input("🔍 Buscar exame:")

# ... (restante do seu código de exibição permanece igual)
