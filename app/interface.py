import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from app.fuzzy_engine import inferir_dieta, calcular_tmb, dieta
from app.recommender import recomendar_alimentos


# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(page_title="Sistema Fuzzy de Dieta", layout="wide")
st.title("🥗 Sistema Especialista Fuzzy para Recomendação de Dieta")


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

atividade = st.sidebar.selectbox(
    "Nível de atividade física diária",
    ["Sedentário", "Pouco ativo", "Moderadamente ativo", "Muito ativo"]
)


# ===================================================
# BOTÃO
# ===================================================
if st.sidebar.button("🔍 Calcular Recomendação"):

    # 1) Fuzzy
    imc, categoria, intensidade_agregada, valor_fuzzy = inferir_dieta(
        peso, altura, esforco, atividade
    )

    tipo_dieta = (
        "hipocalorica" if valor_fuzzy <= 3 else
        "balanceada"   if valor_fuzzy <= 7 else
        "hipercalorica"
    )

    # 2) TMB + meta
    tmb = calcular_tmb(peso, altura, idade, sexo)

    meta = (
        tmb - 200 if tipo_dieta == "hipocalorica" else
        tmb + 200 if tipo_dieta == "hipercalorica" else
        tmb
    )

    # 3) Banco de alimentos
    alimentos, total_dieta_fixa = recomendar_alimentos(tipo_dieta, meta)


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
        st.write(f"**Intensidade agregada:** {intensidade_agregada:.2f}")
        st.write(f"**Saída fuzzy (0–10):** {valor_fuzzy:.2f}")
        st.success(f"**Dieta recomendada:** {tipo_dieta.upper()}")


    # ===============================================
    # GRÁFICO FUZZY
    # ===============================================
    st.write("### 📈 Funções de Pertinência – Dieta")

    x = np.arange(0, 11, 1)
    fig, ax = plt.subplots()

    ax.plot(x, dieta['hipocalorica'].mf, label='Hipocalórica')
    ax.plot(x, dieta['balanceada'].mf, label='Balanceada')
    ax.plot(x, dieta['hipercalorica'].mf, label='Hipercalórica')

    ax.axvline(valor_fuzzy, color='black', linestyle='--')
    ax.set_xlabel("Nível da dieta")
    ax.set_ylabel("Pertinência")
    ax.legend()

    st.pyplot(fig)


    # ===============================================
    # CARDÁPIO — MODELO FINAL (A)
    # ===============================================
    st.subheader("🍽️ Cardápio Sugerido (Alimentos Individuais)")

    refeicoes = [
        "café da manhã",
        "lanche da manhã",
        "almoço",
        "lanche da tarde",
        "jantar",
        "ceia"
    ]

    total_diario = 0

    for ref in refeicoes:
        itens_ref = [i for i in alimentos if i[0] == ref]

        if not itens_ref:
            continue

        st.markdown(f"## 🍴 {ref.title()}")

        total_ref = 0

        for r, alimento, qtd, kcal, subs in itens_ref:
            total_ref += kcal

            st.markdown(f"**{alimento}** — {qtd} (**{kcal} kcal**)")

            if subs:
                st.markdown(
                    f"<span style='color:gray'>Substituições: {subs}</span>",
                    unsafe_allow_html=True
                )

        total_diario += total_ref
        st.markdown(f"### 🔥 Total da refeição: **{total_ref} kcal**")
        st.markdown("---")

    # Total diário
    st.markdown(f"# 🔥 Total diário sugerido: **{total_diario} kcal**")


else:
    st.info("👈 Preencha os dados e clique em **Calcular Recomendação**.")
