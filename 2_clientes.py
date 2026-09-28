import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="BizFlow AI - Gestão de Clientes", layout="wide")

# FORÇA AS LETRAS PRETAS E ESTILIZA O BANNER DE DESTAQUE
st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] span { font-size: 18px !important; font-weight: 600 !important; color: #000000 !important; }
        .header-box { background-color: #0A2540; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
        .header-box h1 { color: white !important; margin: 0; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>BizFlow AI</h1><p style="margin: 5px 0 0 0; opacity: 0.9;">Plataforma Integrada de Gestão Operacional e Estratégica</p></div>', unsafe_allow_html=True)
st.subheader("👥 Cadastro e Gestão de Clientes")

def inicializar_banco_clientes():
    conn = sqlite3.connect('bizflow.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, telefone TEXT, email TEXT)")
    conn.commit()
    conn.close()

inicializar_banco_clientes()

# Carrega a lista de clientes atualizada
conn = sqlite3.connect('bizflow.db')
df_clientes = pd.read_sql_query("SELECT id, nome as 'Nome', telefone as 'WhatsApp', email as 'E-mail' FROM clientes", conn)
conn.close()

aba_cadastro_cli, aba_lista_cli, aba_excluir_cli = st.tabs(["➕ Cadastrar Cliente", "📋 Lista de Clientes e Contato", "🗑️ Remover Cliente"])

with aba_cadastro_cli:
    with st.form("form_cliente", clear_on_submit=True):
        nome_cliente = st.text_input("Nome do Cliente")
        telefone_cliente = st.text_input("Telefone / WhatsApp (Apenas números com DDD, ex: 11999999999)")
        email_cliente = st.text_input("E-mail")
        
        if st.form_submit_button("Cadastrar Cliente") and nome_cliente:
            conn = sqlite3.connect('bizflow.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)", (nome_cliente, telefone_cliente, email_cliente))
            conn.commit()
            conn.close()
            st.success(f"Cliente '{nome_cliente}' cadastrado!")
            st.rerun()

with aba_lista_cli:
    if not df_clientes.empty:
        # Campo de busca
        busca = st.text_input("🔍 Pesquisar cliente pelo nome:")
        df_filtrado = df_clientes[df_clientes['Nome'].str.contains(busca, case=False)] if busca else df_clientes
        
        st.dataframe(df_filtrado[['Nome', 'WhatsApp', 'E-mail']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("💬 Iniciar Conversa no WhatsApp")
        
        lista_nomes = df_filtrado['Nome'].tolist()
        cli_conversa = st.selectbox("Escolha um cliente para mandar mensagem:", options=lista_nomes, key="zap_cli")
        
        # CORREÇÃO AQUI: Adicionado .iloc[0] para evitar o erro de indexação do Pandas
        dados_zap = df_filtrado[df_filtrado['Nome'] == cli_conversa].iloc[0]
        num_telefone = str(dados_zap['WhatsApp']).strip().replace(" ", "").replace("-", "")
        
        if num_telefone:
            link_zap = f"https://wa.me{num_telefone}"
            st.markdown(f'<a href="{link_zap}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">📲 Abrir Conversa com {cli_conversa}</button></a>', unsafe_allow_html=True)
    else:
        st.info("Nenhum cliente cadastrado ainda. Vá na aba de cadastro.")

with aba_excluir_cli:
    if not df_clientes.empty:
        cli_selecionado = st.selectbox("Escolha o cliente para remover", options=df_clientes['Nome'].tolist(), key="del_cli")
        
        # CORREÇÃO AQUI TAMBÉM: Adicionado .iloc[0]
        dados_cli = df_clientes[df_clientes['Nome'] == cli_selecionado].iloc[0]
        
        if st.button("🗑️ Confirmar Exclusão do Cliente", type="primary"):
            conn = sqlite3.connect('bizflow.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (int(dados_cli['id']),))
            conn.commit()
            conn.close()
            st.success("Cliente removido com sucesso!")
            st.rerun()
    else:
        st.info("Nenhum cliente cadastrado para remover.")