import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from app.fuzzy_engine import inferir_dieta, calcular_tmb
from app.recommender import recomendar_alimentos

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(page_title="Sistema Especialista de Dieta", layout="wide")
st.title("🥗 Sistema Especialista com Fuzzy para Recomendação de Dieta")


# ===============================
# ENTRADAS DO USUÁRIO
# ===============================
st.sidebar.header("⚙️ Entradas do Usuário")

peso = st.sidebar.number_input("Peso (kg)", 30.0, 300.0, 70.0)
altura = st.sidebar.number_input("Altura (m)", 1.20, 2.50, 1.75)
idade = st.sidebar.number_input("Idade", 10, 100, 25)
sexo = st.sidebar.selectbox("Sexo", ["Masculino", "Feminino"])

esforco = st.sidebar.slider(
    "Esforço percebido no treino (RPE – 0 a 10)",
    0, 10, 5
)

atividade_fisica = st.sidebar.selectbox(
    "Nível de atividade física diária",
    ["Sedentário", "Pouco ativo", "Moderadamente ativo", "Muito ativo"]
)


# ===================================================
# BOTÃO
# ===================================================
if st.sidebar.button("🔍 Calcular Recomendação"):

    # 1) Fuzzy + regra simples
    imc, categoria, intensidade, tipo_dieta = inferir_dieta(
        peso, altura, esforco, atividade_fisica
    )

    # 2) TMB + meta
    tmb = calcular_tmb(peso, altura, idade, sexo, atividade_fisica)

    meta = (
        tmb - 200 if tipo_dieta == "hipocalorica" else
        tmb + 200 if tipo_dieta == "hipercalorica" else
        tmb
    )

    # 3) Banco de alimentos
    alimentos, total_dieta_fixa = recomendar_alimentos(tipo_dieta, meta)

    # ===============================================
    # AJUSTE PROPORCIONAL DA DIETA
    # ===============================================
    fator = meta / total_dieta_fixa if total_dieta_fixa != 0 else 1
    st.info(f"Fator de ajuste aplicado: {fator:.2f}")

    alimentos_ajustados = []
    total_ajustado = 0

    for refeicao, alimento, qtd, kcal, subs in alimentos:
        kcal_ajustado = int(kcal * fator)
        alimentos_ajustados.append((refeicao, alimento, qtd, kcal_ajustado, subs))
        total_ajustado += kcal_ajustado

    alimentos = alimentos_ajustados

    # ===============================================
    # PAINEL NUMÉRICO
    # ===============================================
    st.subheader("📊 Resultado da Análise")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**IMC:** {imc:.2f} — *{categoria}*")
        st.write(f"**TMB:** {tmb:.0f} kcal/dia")
        st.write(f"**Meta calórica:** {meta:.0f} kcal/dia")

    with col2:
        st.write(f"**Intensidade agregada:** {intensidade:.2f}")
        st.success(f"**Dieta recomendada:** {tipo_dieta.upper()}")
        st.write(f"**Calorias originais:** {total_dieta_fixa} kcal")
        st.write(f"**Calorias ajustadas:** {total_ajustado} kcal")

    # ===============================================
    # CARDÁPIO — MODELO FINAL (AJUSTADO)
    # ===============================================
    st.subheader("🍽️ Cardápio Ajustado Proporcionalmente")

    refeicoes = ["café da manhã", "lanche da manhã", "almoço", "lanche da tarde", "jantar", "ceia"]

    for ref in refeicoes:
        itens_ref = [i for i in alimentos if i[0] == ref]

        if not itens_ref:
            continue

        st.markdown(f"## 🍴 {ref.title()}")
        total_ref = 0

        for _, alimento, qtd, kcal, subs in itens_ref:
            total_ref += kcal

            st.markdown(f"**{alimento}** — {qtd} (**{kcal} kcal**)")

            if subs:
                st.markdown(
                    f"<span style='color:gray'>Substituições: {subs}</span>",
                    unsafe_allow_html=True
                )

        st.markdown(f"### 🔥 Total da refeição: **{total_ref} kcal**")
        st.markdown("---")

    # Total diário ajustado
    st.markdown(f"# 🔥 Total diário ajustado: **{total_ajustado} kcal**")


else:
    st.info("👈 Preencha os dados e clique em **Calcular Recomendação**.")
