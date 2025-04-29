import streamlit as st
import pandas as pd
from PIL import Image
import os
import gspread

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================
st.set_page_config(
    page_title="Coleta+ 🐾",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# FUNÇÕES AUXILIARES
# ======================================
@st.cache_data
def load_data():
    """Carrega os dados do Google Sheets"""
    try:
        # Conectando ao Google Sheets usando o gspread sem autenticação
        gc = gspread.service_account()

        # ID da planilha (substitua pelo seu ID)
        spreadsheet_id = "14iqQIJS11Fq7B1jPVxI_7Pkl4FMn2buu"  # ID do seu Google Sheets
        worksheet = gc.open_by_key(spreadsheet_id).get_worksheet(0)  # Acessa a primeira aba
        
        # Carrega os dados
        dados = pd.DataFrame(worksheet.get_all_records())
        dados.columns = dados.columns.str.strip()  # Remove espaços extras nas colunas
        
        # Verifica se a coluna 'CONTEÚDO' existe, caso contrário, cria
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados do Google Sheets:\n{e}")
        return pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 
                                     'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

def load_logo():
    """Carrega a imagem do logo"""
    try:
        if os.path.exists('logo_hospital.png'):
            return Image.open('logo_hospital.png')
        return None
    except Exception as e:
        st.warning(f"Erro ao carregar logo: {e}")
        return None

def display_detalhes(detalhes):
    """Exibe os detalhes do exame"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("📋 Informações Básicas")
        st.markdown(f"**Código:** `{detalhes['CÓDIGO']}`")
        st.markdown(f"**Prazo:** `{detalhes['PRAZO']}`")
        st.markdown(f"**Tubo:** `{detalhes['TUBO']}`")
    
    with col2:
        st.subheader("📝 Detalhes")
        st.markdown(f"**Cuidados Especiais:**\n> {detalhes['CUIDADOS ESPECIAIS']}")
        st.markdown(f"**Laboratório:** `{detalhes['LABORATÓRIO']}`")
        st.markdown(f"**Conteúdo:**\n> {detalhes['CONTEÚDO']}")

# ======================================
# INTERFACE PRINCIPAL
# ======================================
# Carregar dados
dados = load_data()

# Sidebar
with st.sidebar:
    # Logo
    logo = load_logo()
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown(""" 
        <div style='width:100px; height:100px; background-color:#f0f0f0; 
        border-radius:10px; display:flex; justify-content:center; 
        align-items:center; margin-bottom:20px;'>
        <span style='color:#999;'>Logo</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.title("Coleta+ 🐾")
    
    # Busca
    termo_busca = st.text_input(
        "🔍 Buscar exame:",
        placeholder="Digite o nome do exame",
        help="Busque por nome ou conteúdo do exame"
    )
    
    if st.button("🧹 Limpar busca", use_container_width=True):
        termo_busca = ""


# Área principal
st.header("Catálogo de Exames")

# Filtragem
if termo_busca:
    resultados = dados[
        dados['EXAMES'].fillna('').str.lower().str.contains(termo_busca.lower()) | 
        dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo_busca.lower())
    ]
else:
    resultados = dados.copy()

# Exibição dos resultados
if not resultados.empty:
    exame_selecionado = st.selectbox(
        "Selecione um exame para ver detalhes:",
        resultados['EXAMES'].unique(),
        index=None,
        placeholder="Selecione um exame"
    )
    
    if exame_selecionado:
        detalhes = resultados[resultados['EXAMES'] == exame_selecionado].iloc[0]
        display_detal_
