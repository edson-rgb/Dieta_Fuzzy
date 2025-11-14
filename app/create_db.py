import sqlite3
import os

# ======================================================
#  Caminho correto para salvar o banco dentro de /data
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # raiz do projeto
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "alimentos.db")

# Garante que a pasta data existe
os.makedirs(DATA_DIR, exist_ok=True)

# Conecta ao banco
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print(f"📦 Criando banco em: {DB_PATH}")


# ============================================
#  Remove tabela antiga (se existir)
# ============================================
cur.execute("DROP TABLE IF EXISTS alimentos")


# ============================================
#  Cria nova tabela com estrutura final
# ============================================
cur.execute("""
CREATE TABLE alimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_dieta TEXT NOT NULL,
    refeicao TEXT NOT NULL,
    grupo TEXT NOT NULL,
    alimento TEXT NOT NULL,
    quantidade TEXT NOT NULL,
    calorias INTEGER NOT NULL,
    substituicoes TEXT
)
""")

print(" Tabela 'alimentos' criada com sucesso.")


# ============================================
#  Lista de alimentos INDIVIDUAIS
# ============================================

alimentos = [

    # =========================================================
    #  DIETA HIPOCALÓRICA
    # =========================================================

    # CAFÉ DA MANHÃ
    ('hipocalorica','café da manhã','proteína','Iogurte desnatado','170g',120,'OU kefir 120g OU 2 claras (60g)'),
    ('hipocalorica','café da manhã','carboidrato','Tapioca simples','80g',100,'OU pão integral 30g'),
    ('hipocalorica','café da manhã','fruta','Morango','100g',32,'OU maçã 100g'),

    # LANCHE DA MANHÃ
    ('hipocalorica','lanche da manhã','fruta','Maçã','110g',60,'OU banana 90g'),
    ('hipocalorica','lanche da manhã','oleaginosa','Castanha-do-Pará','6g',40,'OU castanha de caju 10g'),

    # ALMOÇO
    ('hipocalorica','almoço','carboidrato','Arroz integral','100g',120,'OU purê de batata 100g'),
    ('hipocalorica','almoço','leguminosa','Feijão carioca','80g',90,'OU lentilha 70g'),
    ('hipocalorica','almoço','proteína','Frango grelhado','120g',200,'OU peixe branco 100g'),
    ('hipocalorica','almoço','legume','Cenoura cozida','60g',25,'OU abobrinha 50g'),
    ('hipocalorica','almoço','salada','Alface + tomate','80g',15,'OU rúcula 80g'),

    # LANCHE DA TARDE
    ('hipocalorica','lanche da tarde','fruta','Banana','90g',85,'OU maçã 110g'),
    ('hipocalorica','lanche da tarde','proteína','Iogurte natural','130g',70,'OU kefir 100g'),

    # JANTAR
    ('hipocalorica','jantar','proteína','Peixe assado','120g',150,'OU ovo cozido 50g'),
    ('hipocalorica','jantar','carboidrato','Batata cozida','100g',90,'OU arroz integral 100g'),
    ('hipocalorica','jantar','legume','Abobrinha','100g',20,'OU cenoura 80g'),
    ('hipocalorica','jantar','salada','Salada verde','60g',12,'OU pepino 70g'),

    # CEIA
    ('hipocalorica','ceia','proteína','Claras de ovo','60g',34,'OU iogurte desnatado 100g'),


    # =========================================================
    # ⚖️ DIETA BALANCEADA
    # =========================================================

    # CAFÉ DA MANHÃ
    ('balanceada','café da manhã','carboidrato','Aveia','50g',190,'OU granola 40g'),
    ('balanceada','café da manhã','fruta','Banana','100g',89,'OU maçã 110g'),
    ('balanceada','café da manhã','proteína','Omelete','120g',200,'OU ovos cozidos 100g'),

    # LANCHE DA MANHÃ
    ('balanceada','lanche da manhã','fruta','Tangerina','100g',53,'OU laranja 120g'),
    ('balanceada','lanche da manhã','oleaginosa','Castanhas','20g',120,'OU amendoim 20g'),

    # ALMOÇO
    ('balanceada','almoço','carboidrato','Arroz branco','150g',195,'OU macarrão 150g'),
    ('balanceada','almoço','leguminosa','Feijão preto','100g',130,'OU grão de bico 80g'),
    ('balanceada','almoço','proteína','Carne bovina magra','150g',250,'OU frango desfiado 150g'),
    ('balanceada','almoço','legume','Couve cozida','40g',30,'OU brócolis 50g'),
    ('balanceada','almoço','fruta','Abacaxi','100g',48,'OU melancia 120g'),

    # LANCHE DA TARDE
    ('balanceada','lanche da tarde','carboidrato','Pão integral','50g',120,'OU tapioca 60g'),
    ('balanceada','lanche da tarde','proteína','Iogurte com granola','180g',160,'OU leite com aveia 200ml'),

    # JANTAR
    ('balanceada','jantar','proteína','Peixe grelhado','180g',240,'OU frango grelhado 180g'),
    ('balanceada','jantar','carboidrato','Purê de batata','150g',150,'OU arroz 150g'),
    ('balanceada','jantar','legume','Brócolis','80g',30,'OU cenoura 80g'),

    # CEIA
    ('balanceada','ceia','vitamina','Vitamina de banana','250ml',180,'OU leite com cacau 250ml'),


    # =========================================================
    # 💪 DIETA HIPERCALÓRICA
    # =========================================================

    # CAFÉ DA MANHÃ
    ('hipercalorica','café da manhã','carboidrato','Pão com pasta de amendoim','120g',400,'OU pão + manteiga 100g'),
    ('hipercalorica','café da manhã','vitamina','Vitamina de abacate','300ml',450,'OU shake banana + aveia 300ml'),

    # LANCHE DA MANHÃ
    ('hipercalorica','lanche da manhã','carboidrato','Batata doce cozida','130g',110,'OU banana 120g'),
    ('hipercalorica','lanche da manhã','proteína','Ovos mexidos','120g',180,'OU omelete 150g'),

    # ALMOÇO
    ('hipercalorica','almoço','carboidrato','Arroz branco','200g',260,'OU macarrão 200g'),
    ('hipercalorica','almoço','proteína','Carne moída','180g',320,'OU frango ao molho 200g'),
    ('hipercalorica','almoço','leguminosa','Feijão','120g',160,'OU lentilha 120g'),
    ('hipercalorica','almoço','legume','Batata inglesa','150g',130,'OU mandioca 150g'),

    # LANCHE DA TARDE
    ('hipercalorica','lanche da tarde','shake','Whey + aveia','300ml',420,'OU vitamina banana + pasta 300ml'),
    ('hipercalorica','lanche da tarde','oleaginosa','Amendoim torrado','30g',170,'OU castanhas 25g'),

    # JANTAR
    ('hipercalorica','jantar','carboidrato','Macarrão ao molho branco','300g',450,'OU lasanha 250g'),
    ('hipercalorica','jantar','proteína','Frango grelhado','200g',300,'OU peixe assado 200g'),
    ('hipercalorica','jantar','legume','Brócolis cozido','100g',35,'OU cenoura 100g'),

    # CEIA
    ('hipercalorica','ceia','vitamina','Shake hipercalórico','350ml',500,'OU shake caseiro 350ml')
]


# ============================================
# 💾 Inserindo todos os alimentos
# ============================================
cur.executemany("""
INSERT INTO alimentos (tipo_dieta, refeicao, grupo, alimento, quantidade, calorias, substituicoes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", alimentos)

conn.commit()
conn.close()

print("✅ Banco criado e populado com sucesso!")
