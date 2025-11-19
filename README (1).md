# 🥗 Sistema Inteligente de Recomendação de Dieta  
### *Fuzzy Logic + Sistema Especialista + BFS*

Este projeto implementa um sistema inteligente híbrido para recomendação personalizada de dietas, combinando **Lógica Fuzzy**, **Sistema Especialista baseado em regras** e **Busca em Largura (BFS)**.  
O objetivo é simular a tomada de decisão humana em nutrição, garantindo precisão, interpretabilidade e robustez.

---

# 📌 Visão Geral da Arquitetura

O sistema integra três abordagens clássicas da Inteligência Artificial:

## **1️⃣ Lógica Fuzzy – Interpretação subjetiva da intensidade**

A lógica fuzzy interpreta duas variáveis subjetivas fornecidas pelo usuário:

- **Nível de atividade física (0–10)**
- **Esforço percebido (RPE – 0 a 10)**

Essas entradas passam por um sistema fuzzy que gera:

- intensidade crisp (0–10)
- intensidade linguística: *baixa*, *moderada* ou *alta*

Isso permite lidar com incerteza e subjetividade.

---

## **2️⃣ Sistema Especialista – Base de conhecimento nutricional**

O sistema especialista recebe duas categorias:

- **IMC** → baixo | normal | sobrepeso | obesidade  
- **Intensidade** → baixa | moderada | alta  

E utiliza 12 regras nutricionais:

```
Se IMC = baixo      e intensidade = baixa     → hipercalórica  
Se IMC = normal     e intensidade = alta      → hipercalórica
Se IMC = sobrepeso  e intensidade = baixa     → hipocalórica
...
```

Cada regra representa conhecimento humano de um nutricionista.

---

## **3️⃣ BFS – Busca da regra mais próxima**

Caso o estado `(imc_cat, intensidade_cat)` não tenha regra exata (ex.: intensidade muito-limítrofe), a BFS é usada para navegar em um grafo IMC × Intensidade até encontrar a regra mais próxima semântica e nutricionalmente.

A BFS garante:

- robustez
- decisão sempre possível
- busca mínima (1–3 passos)

---

# 🔍 Fluxo Geral da Decisão

1. Usuário fornece peso, altura, RPE e nível de atividade.  
2. O sistema calcula o **IMC** e classifica a faixa correspondente.  
3. A lógica fuzzy calcula a **intensidade crisp** e sua categoria linguística.  
4. O sistema especialista verifica se existe uma regra exata.  
5. Se não existir, o **BFS encontra o estado válido mais próximo**.  
6. O tipo de dieta é definido.  
7. O banco SQLite gera o cardápio base.  
8. As quantidades dos alimentos são **ajustadas proporcionalmente** à meta calórica.

---

# 🧠 Grafo de Estados (IMC × Intensidade)

```
               Intensidade
           baixa   moderada   alta
             |        |        |
IMC baixo    ●--------●--------●
             |        |        |
IMC normal   ●--------●--------●
             |        |        |
sobrepeso    ●--------●--------●
             |        |        |
obesidade    ●--------●--------●
```

Cada nó representa um estado possível analisado pelo sistema especialista.

---

# Arvore de decisão

        |                                                  ┌───────────────┐
        |                                                  │      IMC      │
        |                                                  └───────┬───────┘
        |            ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
        |            │                                  │                                │                               |
        |
        |         │baixo│                           |normal│                        │sobrepeso│                     │obesidade│
        |
        |             │                                 │                                │                               │
        |
        |        │intensidade│                    │intensidade│                    │intensidade│                   │intensidade│
        |    baixa │ moderada │ alta          baixa │ moderada │ alta          baixa │ moderada │ alta         baixa │ moderada │ alta
        |    │        │         │             │         │         │             │        │        │               │        │        │
        |    │        │         │             │         │         │             │        │        │               │        │        │
        |
        |│hiperc│ │hiperc│ │hiperc│        │balanc│ │balanc│ │hiperc│       │hipoc|  |balanc| |balanc|          |hipoc|  │hipoc|  |hipoc|   
        


# 🔎 Exemplo real da BFS

Entrada do usuário:

- IMC = normal  
- intensidade fuzzy = moderada  
- estado inicial = **("normal", "moderada")**

Como existe regra para esse estado, a BFS resolve imediatamente:

```
Estado encontrado: ("normal","moderada")
Dieta: balanceada
```

Se não houvesse regra exata:

- A BFS navegaria nos vizinhos diretos  
- No máximo 1 ou 2 níveis  
- Até encontrar uma combinação válida

---

# 📁 Estrutura de Pastas Atualizada

```
app/
│
├── src/
│   ├── fuzzy_engine.py        # lógica fuzzy
│   ├── imc.py                 # cálculo e classificação do IMC
│   ├── rules_engine.py        # base de regras do sistema especialista
│   ├── bfs_search.py          # implementação da BFS
│   ├── decision.py            # pipeline principal que integra tudo
│   └── recommender.py         # recomenda alimentos via SQLite
│
├── data/
│   └── alimentos.db           # banco de dados
│
├── scripts/
│   └── create_db.py           # cria e popula o banco
│
└── ui/
    └── interface.py           # interface Streamlit
```

---

# 🔬 Tecnologias Utilizadas

- Python 3.x  
- scikit-fuzzy  
- Streamlit  
- SQLite  
- BFS (collections.deque)  
- NumPy  

---

# 🚀 Execução

```bash
pip install -r requirements.txt
python scripts/create_db.py
streamlit run app/ui/interface.py
```

---

# 🧩 Conclusão

Este sistema combina três técnicas de IA complementares:

- a **lógica fuzzy** trata da incerteza  
- o **sistema especialista** fornece conhecimento humano formalizado  
- o **BFS** garante robustez e tomada de decisão mesmo em estados não conhecidos






