import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "alimentos.db")

os.makedirs(DATA_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print(f"📦 Criando banco em: {DB_PATH}")

cur.execute("DROP TABLE IF EXISTS alimentos")

cur.execute("""
CREATE TABLE alimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_dieta TEXT NOT NULL,
    refeicao TEXT NOT NULL,
    alimento TEXT NOT NULL,
    quantidade REAL NOT NULL,
    unidade TEXT NOT NULL,
    calorias REAL NOT NULL,
    substituicoes TEXT
)
""")

print("Tabela criada.")

################################################################################
# LISTA DE ALIMENTOS 
################################################################################

alimentos = [

    # --------------------------------------------------------------------------
    # DIETA HIPOCALÓRICA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("hipocalorica", "café da manhã", "Iogurte desnatado", 170, "g", 120, "iogurte natural 150g"),
    ("hipocalorica", "café da manhã", "Tapioca", 80, "g", 100, "pão integral 30g"),
    ("hipocalorica", "café da manhã", "Morango", 100, "g", 32, "maçã 100g"),

    # LANCHE DA MANHÃ
    ("hipocalorica", "lanche da manhã", "Maçã", 110, "g", 60, "banana 90g"),
    ("hipocalorica", "lanche da manhã", "Castanha-do-Pará", 6, "g", 40, "castanha de caju 10g"),

    # ALMOÇO
    ("hipocalorica", "almoço", "Arroz integral", 100, "g", 120, "purê de batata 100g"),
    ("hipocalorica", "almoço", "Feijão carioca", 80, "g", 90, "lentilha 70g"),
    ("hipocalorica", "almoço", "Frango grelhado", 120, "g", 200, "peixe branco 100g"),
    ("hipocalorica", "almoço", "Cenoura cozida", 60, "g", 25, "abobrinha 50g"),
    ("hipocalorica", "almoço", "Salada verde", 80, "g", 15, "rúcula 80g"),

    # LANCHE DA TARDE
    ("hipocalorica", "lanche da tarde", "Banana", 90, "g", 85, "maçã 110g"),
    ("hipocalorica", "lanche da tarde", "Iogurte natural", 130, "g", 70, "iogurte desnatado 100g"),

    # JANTAR
    ("hipocalorica", "jantar", "Peixe assado", 120, "g", 150, "ovo cozido 50g"),
    ("hipocalorica", "jantar", "Batata cozida", 100, "g", 90, "arroz integral 100g"),
    ("hipocalorica", "jantar", "Abobrinha", 100, "g", 20, "cenoura 80g"),
    ("hipocalorica", "jantar", "Salada verde", 60, "g", 12, "pepino 70g"),

    # CEIA
    ("hipocalorica", "ceia", "Claras de ovo", 60, "g", 34, "iogurte desnatado 100g"),

    # --------------------------------------------------------------------------
    # DIETA BALANCEADA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("balanceada", "café da manhã", "Aveia", 50, "g", 190, "granola 40g"),
    ("balanceada", "café da manhã", "Banana", 100, "g", 89, "maçã 110g"),
    ("balanceada", "café da manhã", "Ovos", 100, "g", 140, "omelete 120g"),

    # LANCHE DA MANHÃ
    ("balanceada", "lanche da manhã", "Tangerina", 100, "g", 53, "laranja 120g"),
    ("balanceada", "lanche da manhã", "Castanhas", 20, "g", 120, "amendoim 20g"),

    # ALMOÇO
    ("balanceada", "almoço", "Arroz branco", 150, "g", 195, "macarrão 150g"),
    ("balanceada", "almoço", "Feijão preto", 100, "g", 130, "grão de bico 80g"),
    ("balanceada", "almoço", "Carne bovina magra", 150, "g", 250, "frango 150g"),
    ("balanceada", "almoço", "Couve cozida", 40, "g", 30, "brócolis 50g"),
    ("balanceada", "almoço", "Abacaxi", 100, "g", 48, "melancia 120g"),

    # LANCHE DA TARDE
    ("balanceada", "lanche da tarde", "Pão integral", 50, "g", 120, "tapioca 60g"),
    ("balanceada", "lanche da tarde", "Iogurte com granola", 180, "g", 160, "leite com aveia 200ml"),

    # JANTAR
    ("balanceada", "jantar", "Peixe grelhado", 180, "g", 240, "frango 180g"),
    ("balanceada", "jantar", "Purê de batata", 150, "g", 150, "arroz 150g"),
    ("balanceada", "jantar", "Brócolis", 80, "g", 30, "cenoura 80g"),

    # CEIA
    ("balanceada", "ceia", "Leite com cacau", 250, "ml", 180, "vitamina 250ml"),

    # --------------------------------------------------------------------------
    # DIETA HIPERCALÓRICA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("hipercalorica", "café da manhã", "Pão francês", 60, "g", 160, "pão integral 60g"),
    ("hipercalorica", "café da manhã", "Pasta de amendoim", 30, "g", 180, "pasta de castanha 30g"),
    ("hipercalorica", "café da manhã", "Abacate", 100, "g", 160, "banana 100g"),

    # LANCHE DA MANHÃ
    ("hipercalorica", "lanche da manhã", "Batata doce", 130, "g", 110, "banana 120g"),
    ("hipercalorica", "lanche da manhã", "Ovos mexidos", 120, "g", 180, "omelete 120g"),

    # ALMOÇO
    ("hipercalorica", "almoço", "Arroz branco", 200, "g", 260, "macarrão 200g"),
    ("hipercalorica", "almoço", "Carne moída", 180, "g", 320, "frango ao molho 200g"),
    ("hipercalorica", "almoço", "Feijão", 120, "g", 160, "lentilha 120g"),
    ("hipercalorica", "almoço", "Batata inglesa", 150, "g", 130, "mandioca 150g"),

    # LANCHE DA TARDE
    ("hipercalorica", "lanche da tarde", "Whey", 30, "g", 120, "leite 200ml"),
    ("hipercalorica", "lanche da tarde", "Aveia", 50, "g", 190, "granola 40g"),
    ("hipercalorica", "lanche da tarde", "Banana", 120, "g", 110, "maçã 120g"),

    # JANTAR
    ("hipercalorica", "jantar", "Macarrão ao molho branco", 300, "g", 450, "lasanha 250g"),
    ("hipercalorica", "jantar", "Frango grelhado", 200, "g", 300, "peixe assado 200g"),
    ("hipercalorica", "jantar", "Brócolis cozido", 100, "g", 35, "cenoura 100g"),

    # CEIA
    ("hipercalorica", "ceia", "Leite integral", 300, "ml", 190, "leite desnatado 300ml"),
    ("hipercalorica", "ceia", "Aveia", 40, "g", 150, "granola 40g"),
]

################################################################################
# INSERÇÃO NO BANCO
################################################################################

cur.executemany("""
INSERT INTO alimentos (tipo_dieta, refeicao, alimento, quantidade, unidade, calorias, substituicoes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", alimentos)

conn.commit()
conn.close()

print(" Banco criado e populado com sucesso!")
