import sys
import os

# Ajustar caminho raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
from app.src.decision import inferir_dieta
from app.src.tmb import calcular_tmb
from app.database.recommender import recomendar_alimentos




st.set_page_config(page_title="Sistema Especialista de Dieta", layout="wide")
st.title("🥗 Sistema Especialista com Fuzzy + BFS para Recomendação de Dieta")




st.sidebar.header("⚙️ Entradas do Usuário")

peso = st.sidebar.number_input("Peso (kg)", 30.0, 300.0, 70.0)
altura = st.sidebar.number_input("Altura (m)", 1.20, 2.50, 1.75)
idade = st.sidebar.number_input("Idade", 10, 100, 25)
sexo = st.sidebar.selectbox("Sexo", ["Masculino", "Feminino"])

esforco = st.sidebar.slider("Esforço percebido (RPE – 0 a 10)", 0, 10, 5)

atividade_fisica = st.sidebar.selectbox(
    "Nível de atividade física diária",
    ["Sedentário", "Pouco ativo", "Moderadamente ativo", "Muito ativo"]
)




if st.sidebar.button("🔍 Calcular Recomendação"):

    resultado = inferir_dieta(peso, altura, esforco, atividade_fisica)

    imc = resultado["imc"]
    categoria = resultado["categoria_imc"]
    intensidade = resultado["intensidade"]
    intensidade_cat = resultado["intensidade_cat"]
    tipo_dieta = resultado["dieta"]
    estado_bfs = resultado["estado_usado"]

    
    tmb = calcular_tmb(peso, altura, idade, sexo, atividade_fisica)

    # Ajuste calórico
    meta = (
        tmb - 200 if tipo_dieta == "hipocalorica" else
        tmb + 200 if tipo_dieta == "hipercalorica" else
        tmb
    )

    alimentos, total_dieta_fixa = recomendar_alimentos(tipo_dieta, meta)

    fator = meta / total_dieta_fixa if total_dieta_fixa != 0 else 1

    st.info(f"Fator de ajuste aplicado: {fator:.2f}")

    alimentos_ajustados = []
    total_ajustado = 0

    for refeicao, alimento, qtd, kcal, subs in alimentos:
        kcal_ajustado = int(kcal * fator)
        qtd_ajustada = int(qtd * fator)

        alimentos_ajustados.append(
            (refeicao, alimento, f"{qtd_ajustada}g", kcal_ajustado, subs)
        )

        total_ajustado += kcal_ajustado


    
    
    
    st.subheader("📊 Resultado da Análise")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**IMC:** {imc:.2f} — *{categoria}*")
        st.write(f"**Intensidade:** {intensidade:.2f} — *{intensidade_cat}*")
        st.write(f"**TMB:** {tmb:.0f} kcal/dia")
        st.write(f"**Meta calórica:** {meta:.0f} kcal/dia")

    with col2:
        st.success(f"**Dieta recomendada:** {tipo_dieta.upper()}")
        st.write(f"**Estado BFS escolhido:** {estado_bfs}")
        st.write(f"**Calorias originais:** {total_dieta_fixa} kcal")
        st.write(f"**Calorias ajustadas:** {total_ajustado} kcal")

    st.subheader("🍽️ Cardápio Ajustado")

    refeicoes = ["café da manhã", "lanche da manhã", "almoço", "lanche da tarde", "jantar", "ceia"]

    for ref in refeicoes:
        itens = [i for i in alimentos_ajustados if i[0] == ref]

        if not itens:
            continue

        st.markdown(f"## 🍴 {ref.title()}")

        total_ref = 0
        for _, alimento, qtd, kcal, subs in itens:
            total_ref += kcal
            st.markdown(f"**{alimento}** — {qtd} (**{kcal} kcal**)")
            if subs:
                st.markdown(
                    f"<span style='color:gray'>Substituição: {subs}</span>",
                    unsafe_allow_html=True
                )

        st.markdown(f"### 🔥 Total da refeição: **{total_ref} kcal**")
        st.markdown("---")

    st.markdown(f"# 🔥 Total diário ajustado: **{total_ajustado} kcal**")


else:
    st.info("👈 Preencha os dados e clique em **Calcular Recomendação**.")
