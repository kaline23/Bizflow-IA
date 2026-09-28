import streamlit as st

st.set_page_config(page_title="BizFlow AI - Atendimento", layout="wide")

# FORÇA AS LETRAS PRETAS E ESTILIZA O BANNER DE DESTAQUE
st.markdown("""
    <style>
        [data-testid="stSidebarNavItems"] span { font-size: 18px !important; font-weight: 600 !important; color: #000000 !important; }
        .header-box { background-color: #0A2540; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; }
        .header-box h1 { color: white !important; margin: 0; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>BizFlow AI</h1><p style="margin: 5px 0 0 0; opacity: 0.9;">Plataforma Integrada de Gestão Operacional e Estratégica</p></div>', unsafe_allow_html=True)
st.subheader("💬 Modelos de Respostas Rápidas")
st.write("Utilize os blocos abaixo para copiar os scripts de atendimento com apenas um clique:")

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📝 Boas-vindas")
    msg1 = "Olá! Seja muito bem-vindo(a) ao nosso atendimento! 😊 Como posso te ajudar hoje?"
    st.text_area("Mensagem:", value=msg1, height=130, disabled=True, key="t1")
    st.code(msg1, language="text")

with col2:
    st.markdown("### 💳 Chave PIX")
    msg2 = "Para confirmar seu pedido, você pode realizar o pagamento via PIX. Segue nossa chave: [SUA CHAVE PIX]."
    st.text_area("Mensagem:", value=msg2, height=130, disabled=True, key="t2")
    st.code(msg2, language="text")

with col3:
    st.markdown("### 📦 Código de Rastreio")
    msg3 = "Passando para avisar que seu pedido já foi embalado com muito carinho e está a caminho! 🚀"
    st.text_area("Mensagem:", value=msg3, height=130, disabled=True, key="t3")
    st.code(msg3, language="text")