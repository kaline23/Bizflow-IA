import streamlit as st
import sqlite3
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="BizFlow AI - Painel Principal", layout="wide")

# 2. ESTILO VISUAL DA PÁGINA PRINCIPAL (FORÇA LETRAS PRETAS E BANNER AZUL)
st.markdown("""
    <style>
        /* Força todas as letras do menu esquerdo a ficarem grandes e puramente PRETAS */
        [data-testid="stSidebarNavItems"] span {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: #000000 !important;
        }
        /* Banner de destaque no topo */
        .header-box {
            background-color: #0A2540;
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
        }
        .header-box h1 { color: white !important; margin: 0; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 3. BANCO DE DADOS
def inicializar_banco():
    conn = sqlite3.connect('bizflow.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, preco_custo REAL, preco_venda REAL, quantidade INTEGER, nivel_minimo INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora TEXT DEFAULT (datetime('now', 'localtime')), tipo TEXT NOT NULL, descricao TEXT, valor REAL)''')
    conn.commit()
    conn.close()

inicializar_banco()

# 4. BANNER DE DESTAQUE BIZFLOW AI
st.markdown('<div class="header-box"><h1>BizFlow AI</h1><p style="margin: 5px 0 0 0; opacity: 0.9;">Plataforma Integrada de Gestão Operacional e Estratégica</p></div>', unsafe_allow_html=True)
st.subheader("📊 Painel de Visão Geral")

# 5. BUSCA DE DADOS E MÉTRICAS
conn = sqlite3.connect('bizflow.db')
df_produtos = pd.read_sql_query("SELECT * FROM produtos", conn)
df_transacoes = pd.read_sql_query("SELECT tipo, valor FROM transacoes", conn)
df_ultimas_transacoes = pd.read_sql_query("SELECT data_hora as 'Data/Hora', tipo as 'Tipo', descricao as 'Descrição', valor as 'Valor (R$)' FROM transacoes ORDER BY id DESC LIMIT 5", conn)
conn.close()

faturamento_real = df_transacoes[df_transacoes['tipo'] == 'Receita']['valor'].sum() if not df_transacoes.empty else 0.0
despesas_reais = df_transacoes[df_transacoes['tipo'] == 'Despesa']['valor'].sum() if not df_transacoes.empty else 0.0
saldo_real = faturamento_real - despesas_reais
total_itens_estoque = int(df_produtos['quantidade'].sum()) if not df_produtos.empty else 0

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric(label="Faturamento Total", value=f"R$ {faturamento_real:,.2f}".replace('.',',').replace(',','.',1))
with col2: st.metric(label="Despesas Totais", value=f"R$ {despesas_reais:,.2f}".replace('.',',').replace(',','.',1))
with col3: st.metric(label="Saldo de Caixa", value=f"R$ {saldo_real:,.2f}".replace('.',',').replace(',','.',1))
with col4: st.metric(label="Itens no Estoque", value=total_itens_estoque)

st.divider()
st.subheader("⚠️ Alertas de Estoque Crítico")
if not df_produtos.empty:
    criticos = df_produtos[df_produtos['quantidade'] <= df_produtos['nivel_minimo']]
    if not criticos.empty:
        st.error(f"Atenção! Você tem {len(criticos)} produto(s) precisando de reposição urgente:")
        st.dataframe(criticos[['nome', 'quantidade', 'nivel_minimo']], use_container_width=True, hide_index=True)
    else: st.success("Tudo certo! Nenhum produto com estoque crítico.")
else: st.info("Nenhum produto cadastrado.")

st.divider()
st.subheader("🕒 Últimas Transações")
if not df_ultimas_transacoes.empty:
    df_ultimas_transacoes['Valor (R$)'] = df_ultimas_transacoes['Valor (R$)'].map(lambda x: f"R$ {x:,.2f}".replace('.',',').replace(',','.',1))
    st.dataframe(df_ultimas_transacoes, use_container_width=True, hide_index=True)
else: st.info("Nenhuma movimentação registrada.")