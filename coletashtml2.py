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

SHEET_ID = "14iqQIJS11Fq7B1jPVxI_7Pkl4FMn2buu"

@st.cache_data(ttl=300)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        response = requests.get(url)
        response.raise_for_status()
        
        dados = pd.read_csv(StringIO(response.text))
        
        # Verifica e padroniza colunas
        colunas_necessarias = ['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO']
        for col in colunas_necessarias:
            if col not in dados.columns:
                dados[col] = 'N/A'
        
        # Adiciona coluna CONTEÚDO se não existir
        if 'CONTEÚDO' not in dados.columns:
            dados['CONTEÚDO'] = ''
            
        return dados
    
    except Exception as e:
        st.error(f"Erro ao carregar: {str(e)}")
        return pd.DataFrame()

# Interface
dados = load_data()

if not dados.empty:
    st.title("Catálogo de Exames")
    
    # Debug: mostra colunas disponíveis
    st.write("Colunas disponíveis:", dados.columns.tolist())
    
    termo = st.text_input("🔍 Buscar:", placeholder="Digite o nome do exame")
    
    if termo:
        try:
            # Filtro seguro
            mask = (
                dados['EXAMES'].str.contains(termo, case=False, na=False) |
                dados['CONTEÚDO'].str.contains(termo, case=False, na=False)
            )
            resultados = dados[mask]
        except KeyError as e:
            st.error(f"Coluna não encontrada: {str(e)}")
            resultados = dados.copy()
    else:
        resultados = dados

    if not resultados.empty:
        exame = st.selectbox("Selecione:", resultados['EXAMES'].unique())
        detalhes = resultados[resultados['EXAMES'] == exame].iloc[0]
        
        # Exibe os dados disponíveis
        st.markdown(f"### {detalhes['EXAMES']}")
        colunas_exibir = ['CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO']
        
        for col in colunas_exibir:
            if col in detalhes:
                st.markdown(f"**{col}:** `{detalhes[col]}`")
    else:
        st.warning("Nenhum resultado encontrado!")
else:
    st.error("Não foi possível carregar os dados da planilha")
