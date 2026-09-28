# ASSIM DEVE FICAR O SEU BLOCO DE ESTILO NO INÍCIO DO app.py:
st.markdown("""
    <style>
        /* TRUQUE: Esconde o nome 'app' original e escreve 'Painel Principal' no lugar */
        [data-testid="stSidebarNavItems"] li:first-child span {
            font-size: 0 !important;
        }
        [data-testid="stSidebarNavItems"] li:first-child span::after {
            content: "🏠 Painel Principal" !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            color: #000000 !important;
        }

        /* Garante que todas as outras opções fiquem grandes e pretas */
        [data-testid="stSidebarNavItems"] span {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: #000000 !important;
        }
        
        /* Banner do cabeçalho */
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
