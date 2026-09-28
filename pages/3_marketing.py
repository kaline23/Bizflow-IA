import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="BizFlow AI - Marketing", layout="wide")

# FORÇA AS LETRAS PRETAS E ESTILIZA O BANNER DE DESTAQUE
st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] span { font-size: 18px !important; font-weight: 600 !important; color: #000000 !important; }
        .header-box { background-color: #0A2540; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
        .header-box h1 { color: white !important; margin: 0; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>BizFlow AI</h1><p style="margin: 5px 0 0 0; opacity: 0.9;">Plataforma Integrada de Gestão Operacional e Estratégica</p></div>', unsafe_allow_html=True)
st.subheader("📣 Gerador de Posts e Divulgação")

conn = sqlite3.connect('bizflow.db')
df_prod_mkt = pd.read_sql_query("SELECT nome, preco_venda FROM produtos", conn)
conn.close()

if not df_prod_mkt.empty:
    st.write("Crie textos de venda automáticos baseados nos produtos do seu estoque!")
    with st.form("form_marketing"):
        produto_escolhido = st.selectbox("Selecione o Produto para Promover", options=df_prod_mkt['nome'].tolist())
        beneficios = st.text_area("Principais destakes")
        tom_voz = st.selectbox("Tom da mensagem", ["Amigável", "Urgente (Estoque Baixo!)"])
        gerar_post = st.form_submit_button("✨ Gerar Texto Comercial")
        
    if gerar_post:
        linha_mkt = df_prod_mkt[df_prod_mkt['nome'] == produto_escolhido].iloc
        preco = float(linha_mkt['preco_venda'])
        st.divider()
        st.subheader("📝 Copie o texto gerado abaixo:")
        if tom_voz == "Amigável":
            texto = f"✨ Novidade incrível! ✨\n\nO nosso queridinho *{produto_escolhido}* está disponível por apenas *R$ {preco:.2f}*! 😍\n\n🎯 Diferenciais:\n📌 {beneficios}\n\nGaranta já o seu! Chame no WhatsApp. 🛍️❤️"
        else:
            texto = f"🚨 ATENÇÃO: ÚLTIMAS UNIDADES! 🚨\n\nSe você estava esperando o momento certo para garantir seu *{produto_escolhido}*, a hora é AGORA! 🏃‍♂️💨\n\n🔥 Por apenas *R$ {preco:.2f}*\n✅ Benefícios: {beneficios}\n\n⚠️ O estoque está acabando rápido. Não fique sem o seu!"
        st.text_area("Texto pronto para colar:", value=texto, height=200)
else: st.info("Cadastre pelo menos um produto na aba de Estoque para liberar o Gerador de Marketing.")
