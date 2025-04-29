import streamlit as st
import pandas as pd

# Layout da página (PRIMEIRO COMANDO STREAMLIT)
st.set_page_config(page_title="Coleta+ 🐾", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        background-color: #f5f2fc;
        color: #333333 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    input, textarea, select {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    .stApp {
        background-color: #f5f2fc;
    }
    .block-container {
        padding-top: 2rem;
    }
    .title {
        color: #6a0dad;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .box {
        background-color: #ffffff;
        border-left: 6px solid #6a0dad;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .label {
        color: #6a0dad;
        font-weight: bold;
        min-width: 180px;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho com logo e título
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("logo_hospital.png", width=80)
with col_title:
    st.markdown("<div class='title'>Coleta+ 🐾</div>", unsafe_allow_html=True)

# Carregar dados
try:
    dados = pd.read_csv('BANCO DE DADOS.csv', encoding='latin1')
    dados.columns = dados.columns.str.strip()
    if 'CONTEÚDO' not in dados.columns:
        dados['CONTEÚDO'] = ''
except Exception as e:
    st.error(f"Erro ao carregar o banco de dados: {e}")
    dados = pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

# Layout principal com duas colunas
col_esquerda, col_direita = st.columns([1, 2])

# Coluna da esquerda: barra de busca e lista de exames
with col_esquerda:
    termo = st.text_input("🔍 Buscar exame ou palavra-chave:", "")

    exames_filtrados = []
    if termo:
        exames_filtrados = dados[dados['EXAMES'].fillna('').str.lower().str.contains(termo.lower()) |
                                 dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo.lower())]['EXAMES'].unique().tolist()

    exame_selecionado = None
    if exames_filtrados:
        exame_selecionado = st.selectbox("Exames encontrados:", exames_filtrados)
    elif termo:
        st.warning("Nenhum exame encontrado.")

# Coluna da direita: exibir detalhes do exame
with col_direita:
    if exame_selecionado:
        resultado = dados[dados['EXAMES'] == exame_selecionado].iloc[0]

        def box(titulo, valor):
            if pd.notna(valor) and str(valor).strip():
                st.markdown(f"<div class='box'><span class='label'>{titulo}:</span><span>{valor}</span></div>", unsafe_allow_html=True)

        st.subheader(f"📄 Detalhes do exame: {resultado['EXAMES']}")
        box("Código", resultado['CÓDIGO'])
        box("Prazo", resultado['PRAZO'])
        box("Tubo", resultado['TUBO'])
        box("Cuidados Especiais", resultado['CUIDADOS ESPECIAIS'])
        box("Laboratório", resultado['LABORATÓRIO'])
        box("Conteúdo", resultado['CONTEÚDO'])

# Rodapé
st.markdown("""
---
<center>© 2025 Coleta+ | Desenvolvido por Caroline Guerra 🐾</center>
""", unsafe_allow_html=True)

# Ajuda
with st.expander("ℹ️ Ajuda"):
    st.markdown("""
    Para problemas no programa, entre em contato:

    📧 Email: caroline.guerra@veros.vet  
    📞 Telefone: (11) 98449-8741
    """)
