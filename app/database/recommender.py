import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # .../app
DB_PATH = os.path.join(BASE_DIR, "data", "alimentos.db")


def recomendar_alimentos(tipo_dieta: str, meta_calorias: int):
    """
    Retorna alimentos individuais agrupados por refeição,
    filtrados pelo tipo de dieta.
    """

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT refeicao, alimento, quantidade, calorias, substituicoes
        FROM alimentos
        WHERE tipo_dieta = ?
        ORDER BY refeicao
    """, (tipo_dieta,))

    rows = cur.fetchall()
    conn.close()

    resultado = []
    total_kcal = 0

    for refeicao, alimento, qtd, kcal, subs in rows:
        total_kcal += kcal
        resultado.append((refeicao, alimento, qtd, kcal, subs))

    return resultado, total_kcal
