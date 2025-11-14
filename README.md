# 🥗 Sistema Especialista Fuzzy para Recomendação de Dieta
Este projeto implementa um **sistema especialista baseado em lógica fuzzy** para recomendar dietas personalizadas com base em:

- **IMC**
- **Nível de atividade física**
- **Esforço percebido (RPE)**
- **Taxa de Metabolismo Basal (TMB) – fórmula Harris–Benedict**
- **Ajuste calórico automático (+200, -200 ou manutenção)**
- **Recomendação de cardápio** baseada em alimentos cadastrados em um banco SQLite

A interface é criada com **Streamlit**, permitindo visualização intuitiva das funções de pertinência e do cardápio recomendado.

---

# 📂 Estrutura do Projeto

```
Dieta_Fuzzy/
│
├── app/
│   ├── fuzzy_engine.py
│   ├── recommender.py
│   ├── interface.py
│   └── __init__.py
│
├── data/
│   ├── alimentos.db
│
├── create_db.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

---

# 🗃 2. Criando/Recriando o Banco de Dados

```bash
python create_db.py
```

Isso gera automaticamente:

- `data/alimentos.db`
- tabela `alimentos`
- alimentos individuais populados corretamente

Para verificar:

```bash
sqlite3 data/alimentos.db ".tables"
```

---

# ▶️ 3. Executando o Sistema

Use:

```bash
python main.py
```

Isso executa o Streamlit automaticamente.

Depois abra:

```
http://localhost:8501
```

---

# 🧠 4. Funcionamento do Sistema Fuzzy

O sistema possui dois módulos:

---

## 🔸 Sistema 1 — Atividade + Esforço (RPE) → Intensidade Agregada

Variáveis fuzzy:

- atividade_fisica ∈ {sedentário, pouco ativo, moderadamente ativo, muito ativo}
- esforço ∈ {leve, moderado, pesado, muito pesado}

Saída:

- intensidade_nivel ∈ {baixa, moderada, alta, muito alta}

---

## 🔸 Sistema 2 — IMC + Intensidade → Dieta Fuzzy

Variáveis:

- imc ∈ {muito baixo, baixo, normal, alto, muito alto}
- intensidade_final ∈ {baixa, moderada, alta, muito alta}

Saída:

- dieta ∈ {hipocalórica, balanceada, hipercalórica}

---

# 🔥 5. Classificação Final da Dieta

```python
tipo_dieta = (
    "hipocalorica" if valor_fuzzy <= 3 else
    "balanceada"   if valor_fuzzy <= 7 else
    "hipercalorica"
)
```

---

# 🔥 6. Cálculo da TMB (Harris–Benedict Atualizado)

### **Homens**
```
TMB = 88.362 + (13.397×peso) + (4.799×altura_cm) – (5.677×idade)
```

### **Mulheres**
```
TMB = 447.593 + (9.247×peso) + (3.098×altura_cm) – (4.330×idade)
```

---

# 🔥 7. Meta Calórica Automática

```
hipocalórica  → TMB - 200
balanceada    → TMB
hipercalórica → TMB + 200
```

---

# 🍽 8. Recomendação de Alimentos

O banco armazena alimentos **individuais**, incluindo:

- refeição  
- grupo  
- alimento  
- quantidade  
- calorias  
- substituições  
- tipo_de_dieta  

O cardápio exibido separa automaticamente por refeição.

---

# 🔄 9. Atualizando o Banco

Sempre que modificar alimentos, execute:

```bash
python create_db.py
```

---

# ❗ Problemas Comuns

### **Erro: no such table: alimentos**

Solução:

- rodar `python create_db.py`
- garantir que está na **raiz do projeto**
- verificar `data/alimentos.db` criado

---

# ✔ Projeto pronto para uso!
