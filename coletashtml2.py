import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(
    page_title="Consulta de Exames 🐾",
    page_icon="🔍",
    layout="wide"
)

SHEET_ID = "14iqQIJS11Fq7B1jPVxI_7Pkl4FMn2buu"

@st.cache_data(ttl=300) 
def load_sheet():
    """Carrega dados do Google Sheets público"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

st.title("🔍 Consulta de Exames Veterinários")
dados = load_sheet()

if not dados.empty:
      termo = st.text_input("Pesquisar exame:", placeholder="Digite o nome do exame")
    
       if termo:
        resultados = dados[dados.apply(lambda row: row.astype(str).str.contains(termo, case=False).any(axis=1)]
    else:
        resultados = dados.copy()

        if not resultados.empty:
        st.write(f"🔬 **Resultados encontrados:** {len(resultados)}")
        
        exame = st.selectbox("Selecione um exame:", resultados['EXAMES'].unique())
        
        detalhes = resultados[resultados['EXAMES'] == exame].iloc[0]
        st.json(detalhes.to_dict()) 
        
    else:
        st.warning("Nenhum exame encontrado!")
else:
    st.error("Não foi possível carregar os dados da planilha")

st.divider()
st.caption("📌 Dados carregados do Google Sheets em tempo real")
