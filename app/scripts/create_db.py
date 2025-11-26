import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "alimentos.db")

os.makedirs(DATA_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print(f"Criando banco em: {DB_PATH}")

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


alimentos = [

    # --------------------------------------------------------------------------
    # DIETA HIPOCALÓRICA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("hipocalorica", "café da manhã", "Iogurte desnatado", 170, "g", 120, None),
    ("hipocalorica", "café da manhã", "Tapioca", 80, "g", 100, None),
    ("hipocalorica", "café da manhã", "Morango", 100, "g", 32, None),

    # LANCHE DA MANHÃ
    ("hipocalorica", "lanche da manhã", "Maçã", 110, "g", 60, None),
    ("hipocalorica", "lanche da manhã", "Castanha-do-Pará", 6, "g", 40, None),

    # ALMOÇO
    ("hipocalorica", "almoço", "Arroz integral", 100, "g", 120, None),
    ("hipocalorica", "almoço", "Feijão carioca", 80, "g", 90, None),
    ("hipocalorica", "almoço", "Frango grelhado", 120, "g", 200, None),
    ("hipocalorica", "almoço", "Cenoura cozida", 60, "g", 25, None),
    ("hipocalorica", "almoço", "Salada verde", 80, "g", 15, None),

    # LANCHE DA TARDE
    ("hipocalorica", "lanche da tarde", "Banana", 90, "g", 85, None),
    ("hipocalorica", "lanche da tarde", "Iogurte natural", 130, "g", 70, None),

    # JANTAR
    ("hipocalorica", "jantar", "Peixe assado", 120, "g", 150, None),
    ("hipocalalorica", "jantar", "Batata cozida", 100, "g", 90, None),
    ("hipocalorica", "jantar", "Abobrinha", 100, "g", 20, None),
    ("hipocalorica", "jantar", "Salada verde", 60, "g", 12, None),

    # CEIA
    ("hipocalorica", "ceia", "Claras de ovo", 60, "g", 34, None),

    # --------------------------------------------------------------------------
    # DIETA BALANCEADA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("balanceada", "café da manhã", "Aveia", 50, "g", 190, None),
    ("balanceada", "café da manhã", "Banana", 100, "g", 89, None),
    ("balanceada", "café da manhã", "Ovos", 100, "g", 140, None),

    # LANCHE DA MANHÃ
    ("balanceada", "lanche da manhã", "Tangerina", 100, "g", 53, None),
    ("balanceada", "lanche da manhã", "Castanhas", 20, "g", 120, None),

    # ALMOÇO
    ("balanceada", "almoço", "Arroz branco", 150, "g", 195, None),
    ("balanceada", "almoço", "Feijão preto", 100, "g", 130, None),
    ("balanceada", "almoço", "Carne bovina magra", 150, "g", 250, None),
    ("balanceada", "almoço", "Couve cozida", 40, "g", 30, None),
    ("balanceada", "almoço", "Abacaxi", 100, "g", 48, None),

    # LANCHE DA TARDE
    # (ANTES: iogurte com granola 180g → AGORA: separado)
    ("balanceada", "lanche da tarde", "Iogurte natural", 130, "g", 70, None),
    ("balanceada", "lanche da tarde", "Granola", 40, "g", 90, None),

    ("balanceada", "lanche da tarde", "Pão integral", 50, "g", 120, None),

    # JANTAR
    ("balanceada", "jantar", "Peixe grelhado", 180, "g", 240, None),
    ("balanceada", "jantar", "Purê de batata", 150, "g", 150, None),
    ("balanceada", "jantar", "Brócolis", 80, "g", 30, None),

    # CEIA
    # (ANTES: Leite com cacau 250ml → AGORA separado)
    ("balanceada", "ceia", "Leite integral", 250, "ml", 150, None),
    ("balanceada", "ceia", "Cacau em pó", 5, "g", 30, None),

    # --------------------------------------------------------------------------
    # DIETA HIPERCALÓRICA
    # --------------------------------------------------------------------------

    # CAFÉ DA MANHÃ
    ("hipercalorica", "café da manhã", "Pão francês", 60, "g", 160, None),
    ("hipercalorica", "café da manhã", "Pasta de amendoim", 30, "g", 180, None),
    ("hipercalorica", "café da manhã", "Abacate", 100, "g", 160, None),

    # LANCHE DA MANHÃ
    ("hipercalorica", "lanche da manhã", "Batata doce", 130, "g", 110, None),
    ("hipercalorica", "lanche da manhã", "Ovos mexidos", 120, "g", 180, None),

    # ALMOÇO
    ("hipercalorica", "almoço", "Arroz branco", 200, "g", 260, None),
    ("hipercalorica", "almoço", "Carne moída", 180, "g", 320, None),
    ("hipercalorica", "almoço", "Feijão", 120, "g", 160, None),
    ("hipercalorica", "almoço", "Batata inglesa", 150, "g", 130, None),

    # LANCHE DA TARDE
    ("hipercalorica", "lanche da tarde", "Whey", 30, "g", 120, None),
    ("hipercalorica", "lanche da tarde", "Aveia", 50, "g", 190, None),
    ("hipercalorica", "lanche da tarde", "Banana", 120, "g", 110, None),

    # JANTAR
    ("hipercalorica", "jantar", "Macarrão ao molho branco", 300, "g", 450, None),
    ("hipercalorica", "jantar", "Frango grelhado", 200, "g", 300, None),
    ("hipercalorica", "jantar", "Brócolis cozido", 100, "g", 35, None),

    # CEIA
    ("hipercalorica", "ceia", "Leite integral", 300, "ml", 190, None),
    ("hipercalorica", "ceia", "Aveia", 40, "g", 150, None),
]


cur.executemany("""
INSERT INTO alimentos (tipo_dieta, refeicao, alimento, quantidade, unidade, calorias, substituicoes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", alimentos)

conn.commit()
conn.close()

print(" Banco criado e populado com sucesso!")
