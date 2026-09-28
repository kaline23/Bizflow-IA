import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="BizFlow AI - Produtos", layout="wide")

# FORÇA AS LETRAS PRETAS E ESTILIZA O BANNER DE DESTAQUE
st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] span { font-size: 18px !important; font-weight: 600 !important; color: #000000 !important; }
        .header-box { background-color: #0A2540; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
        .header-box h1 { color: white !important; margin: 0; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>BizFlow AI</h1><p style="margin: 5px 0 0 0; opacity: 0.9;">Plataforma Integrada de Gestão Operacional e Estratégica</p></div>', unsafe_allow_html=True)
st.subheader("📦 Gerenciamento de Produtos e Estoque")

conn = sqlite3.connect('bizflow.db')
df_produtos_carregados = pd.read_sql_query("SELECT id, nome, preco_venda, quantidade FROM produtos", conn)
conn.close()

aba_cadastro, aba_lista, aba_venda, aba_gerenciar = st.tabs(["➕ Cadastrar Novo", "📋 Lista e Gráfico", "💰 Registrar Venda", "🛠️ Editar / Excluir"])

with aba_cadastro:
    with st.form("form_produto", clear_on_submit=True):
        nome_produto = st.text_input("Nome do Produto")
        col1, col2 = st.columns(2)
        with col1:
            preco_custo = st.number_input("Preço de Custo (R$)", min_value=0.0, step=0.50)
            quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1)
        with col2:
            preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.50)
            nivel_minimo = st.number_input("Nível Mínimo", min_value=0, step=1)
        if st.form_submit_button("Salvar Produto") and nome_produto:
            conn = sqlite3.connect('bizflow.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco_custo, preco_venda, quantidade, nivel_minimo) VALUES (?, ?, ?, ?, ?)", (nome_produto, preco_custo, preco_venda, quantidade, nivel_minimo))
            conn.commit()
            conn.close()
            st.success(f"Produto '{nome_produto}' cadastrado!")
            st.rerun()

with aba_lista:
    conn = sqlite3.connect('bizflow.db')
    df_exibir = pd.read_sql_query("SELECT id as 'ID', nome as 'Produto', preco_custo as 'Custo', preco_venda as 'Venda', quantidade as 'Qtd Atual' FROM produtos", conn)
    conn.close()
    if not df_exibir.empty:
        st.dataframe(df_exibir, use_container_width=True, hide_index=True)
        st.bar_chart(data=df_exibir, x="Produto", y="Qtd Atual")
    else: st.info("Nenhum produto cadastrado.")

with aba_venda:
    if not df_produtos_carregados.empty:
        with st.form("form_venda", clear_on_submit=True):
            produto_selecionado = st.selectbox("Selecione o Produto", options=df_produtos_carregados['nome'].tolist())
            qtd_vendida = st.number_input("Quantidade Vendida", min_value=1, step=1)
            if st.form_submit_button("Lançar Venda"):
                linha_prod = df_produtos_carregados[df_produtos_carregados['nome'] == produto_selecionado].iloc[0]
                if qtd_vendida > int(linha_prod['quantidade']): st.error("Estoque insuficiente!")
                else:
                    nova_qtd = int(linha_prod['quantidade']) - qtd_vendida
                    valor_total = float(linha_prod['preco_venda']) * qtd_vendida
                    conn = sqlite3.connect('bizflow.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd, int(linha_prod['id'])))
                    cursor.execute("INSERT INTO transacoes (tipo, descricao, valor) VALUES (?, ?, ?)", ('Receita', f"Venda de {qtd_vendida}x {produto_selecionado}", valor_total))
                    conn.commit()
                    conn.close()
                    st.success("Venda registrada!")
                    st.rerun()

# 🛠️ ABA EDITAR E EXCLUIR CORRIGIDA COM .iloc[0]
with aba_gerenciar:
    if not df_produtos_carregados.empty:
        prod_lista = df_produtos_carregados['nome'].tolist()
        prod_escolhido = st.selectbox("Escolha o produto para alterar", options=prod_lista, key="edit_prod")
        
        # O AJUSTE ESTÁ AQUI: Adicionado o [0] para ler a linha corretamente
        dados_prod = df_produtos_carregados[df_produtos_carregados['nome'] == prod_escolhido].iloc[0]
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            nova_qtd_est = st.number_input("Alterar Estoque Atual", value=int(dados_prod['quantidade']), step=1)
            if st.button("💾 Salvar Alterações", use_container_width=True):
                conn = sqlite3.connect('bizflow.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd_est, int(dados_prod['id'])))
                conn.commit()
                conn.close()
                st.success("Estoque atualizado!")
                st.rerun()
        with col_ed2:
            st.write("🗑️ Zona de Perigo:")
            if st.button("🗑️ Excluir Produto", type="primary", use_container_width=True):
                conn = sqlite3.connect('bizflow.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE id = ?", (int(dados_prod['id']),))
                conn.commit()
                conn.close()
                st.success("Produto removido!")
                st.rerun()
    else:
        st.info("Nenhum produto cadastrado para gerenciar.")