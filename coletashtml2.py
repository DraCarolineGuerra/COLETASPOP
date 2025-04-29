import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Coleta+ 🐾", layout="wide")

# Título e logo
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo_hospital.png", width=80)
with col2:
    st.markdown("<h1 style='color:#4B0082;'>Coleta+ 🐾</h1>", unsafe_allow_html=True)

# Carregamento dos dados
try:
    dados = pd.read_csv('BANCO DE DADOS.csv', encoding='latin1')
    dados.columns = dados.columns.str.strip()
    if 'CONTEÚDO' not in dados.columns:
        dados['CONTEÚDO'] = ''
except Exception as e:
    st.error(f"Erro ao carregar o banco de dados: {e}")
    dados = pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

# Barra de busca
termo = st.text_input("🔍 Buscar exame ou conteúdo:", "")

if termo:
    resultados = dados[dados['EXAMES'].fillna('').str.lower().str.contains(termo.lower()) | 
                       dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo.lower())]
    
    if not resultados.empty:
        exame_selecionado = st.selectbox("Resultados encontrados:", resultados['EXAMES'].tolist())
        resultado = resultados[resultados['EXAMES'] == exame_selecionado].iloc[0]
        
        st.markdown(f"## {resultado['EXAMES']}")
        
        def mostrar_bloco(titulo, valor, emoji):
            if pd.notna(valor) and str(valor).strip():
                st.markdown(f"### {emoji} {titulo}")
                st.markdown(f"<div style='background-color:#f8f5ff;padding:10px;border-left:5px solid #9370db;'>"
                            f"{valor}</div>", unsafe_allow_html=True)

        mostrar_bloco("Código", resultado['CÓDIGO'], "🔢")
        mostrar_bloco("Prazo", resultado['PRAZO'], "📅")
        mostrar_bloco("Tubo", resultado['TUBO'], "💉")
        mostrar_bloco("Cuidados Especiais", resultado['CUIDADOS ESPECIAIS'], "⚠️")
        mostrar_bloco("Laboratório", resultado['LABORATÓRIO'], "🏥")
        mostrar_bloco("Conteúdo", resultado['CONTEÚDO'], "📝")
    else:
        st.warning("Nenhum resultado encontrado.")
else:
    st.info("Digite um termo acima para buscar um exame.")

# Ajuda
with st.expander("ℹ️ Ajuda"):
    st.markdown("""
    Para problemas no programa, entre em contato:

    📧 Email: caroline.guerra@veros.vet  
    📞 Telefone: (11) 98449-8741
    """)

# Rodapé
st.markdown("""
<hr>
<center>© 2025 Coleta+ | Desenvolvido por Caroline Guerra 🐾</center>
""", unsafe_allow_html=True)
