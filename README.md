
# 🥗 Sistema Especialista para Recomendação de Dieta com IA

Este projeto implementa um **sistema especialista híbrido** para recomendação de dietas personalizadas, combinando **Lógica Fuzzy**, **Regras de Decisão**, **Cálculo de TMB** e um **banco de dados de alimentos**.

## 🚀 Funcionalidades Principais

- **Entrada do usuário**: Peso, altura, idade, sexo, nível de atividade e esforço percebido.
- **Cálculo de IMC** (Índice de Massa Corporal), com classificação automática.
- **Lógica Fuzzy** para interpretar a intensidade do estilo de vida com base em:
  - Nível de atividade física
  - Esforço percebido (RPE)
- **Algoritmo de decisão determinístico** para recomendar o tipo de dieta (hipocalórica, balanceada ou hipercalórica), com base em:
  - IMC
  - Intensidade fuzzy
- **Cálculo da TMB** (Taxa Metabólica Basal), ajustado pelo fator de atividade.
- **Busca em banco de alimentos** (SQLite), com cardápios pré-cadastrados.
- **Ajuste proporcional das calorias do cardápio**, garantindo que a dieta final esteja próxima da meta energética.
- **Interface amigável** com `Streamlit`.

## 🧠 Lógica do Sistema

### Lógica Fuzzy (SkFuzzy)

A lógica fuzzy é usada para combinar:
- `atividade_fisica` (sedentário a muito ativo)
- `esforco` (leve a muito pesado)

Resultado: **Intensidade agregada (0 a 10)**.

### Algoritmo Determinístico para Recomendação da Dieta

Usa esta função para combinar IMC e intensidade:

```python
def determinar_dieta(imc, intensidade):
    if imc < 18.5:
        return "hipercalorica"
    elif imc < 25:
        return "balanceada" if intensidade < 5 else "hipercalorica"
    elif imc < 30:
        return "hipocalorica" if intensidade < 5 else "balanceada"
    else:
        return "hipocalorica"
```

### 🌳 Árvore de Decisão

Veja como os critérios são avaliados:

```
                                   [INÍCIO]
                                      |
                                     IMC
        ┌─────────────────────────────┼─────────────────────────────┐
        |                             |                             |
   IMC < 18.5                   18.5 ≤ IMC < 25               25 ≤ IMC < 30                 IMC ≥ 30
        |                             |                             |                        |
 [HIPERCALÓRICA]                Intensidade                       Intensidade            [HIPOCALÓRICA]
                                (0 a 10)                          (0 a 10)
                          ┌──────────┴──────────┐            ┌──────────┴──────────┐
                          |                     |            |                     |
                   Intensidade < 5      Intensidade ≥ 5  Intensidade < 5    Intensidade ≥ 5
                          |                     |            |                     |
                   [BALANCEADA]          [HIPERCALÓRICA] [HIPOCALÓRICA]      [BALANCEADA]
```

## Mapa de Decisão
graph TD
    A[Início] --> B{IMC}

    B --> B1[IMC < 18.5]
    B --> B2[18.5 ≤ IMC < 25]
    B --> B3[25 ≤ IMC < 30]
    B --> B4[IMC ≥ 30]

    B1 --> L1[[Dieta HIPERCALÓRICA]]

    B2 --> C1{Intensidade < 5?}
    C1 --> L2[[Dieta BALANCEADA]]
    C1 --> L3[[Dieta HIPERCALÓRICA]]

    B3 --> C2{Intensidade < 5?}
    C2 --> L4[[Dieta HIPOCALÓRICA]]
    C2 --> L5[[Dieta BALANCEADA]]

    B4 --> L6[[Dieta HIPOCALÓRICA]]


## ⚙️ Estrutura do Projeto

```
.
├── app/
│   ├── fuzzy_engine.py      # Lógica fuzzy + lógica determinística
│   ├── interface.py         # Interface Streamlit
│   ├── recommender.py       # Consulta ao banco de alimentos
│   ├── __init__.py
│   └── create_db.py         # Script para criar e popular o banco
├── data/
│   └── alimentos.db         # Banco de alimentos SQLite
├── main.py                  # Executa a aplicação Streamlit
├── README.md                # Documentação do projeto
```

## 💾 Banco de Dados

O banco `alimentos.db` armazena alimentos individuais classificados em:

- Tipo de dieta
- Refeição
- Grupo (proteína, fruta, carboidrato, etc.)
- Quantidade e calorias
- Sugestões de substituições alimentares

Você pode recriar o banco com:

```bash
python app/create_db.py
```

## 🧮 Ajuste Proporcional das Calorias

A dieta carregada é ajustada proporcionalmente à meta energética calculada:

```python
fator = meta / total_dieta_fixa
kcal_ajustado = int(kcal * fator)
```

Assim, todas as refeições mantêm seus alimentos originais, mas com porções calóricas ajustadas.

## 🖥️ Rodando a Aplicação

### Requisitos

- Python 3.10+
- Pip para instalar dependências

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

Acesse no navegador:

```
http://localhost:8501
```

## 🔧 TODOs

- [ ] Adaptar receitas/capacidades calóricas dinâmicas
- [ ] Adicionar novas fontes de dados nutricionais
- [ ] Permitir exportar o cardápio ou plano alimentar em PDF ou CSV

