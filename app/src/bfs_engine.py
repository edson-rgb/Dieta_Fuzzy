from collections import deque
from .rules_engine import regras_dieta



# GRAFO DE VIZINHANÇA PARA BFS

vizinhos_imc = {
    "baixo": ["normal"],
    "normal": ["baixo", "sobrepeso"],
    "sobrepeso": ["normal", "obesidade"],
    "obesidade": ["sobrepeso"]
}


vizinhos_intensidade = {
    "baixa": ["moderada"],
    "moderada": ["baixa", "alta"],
    "alta": ["moderada"],

    "muito_baixa": ["baixa"],
    "muito_alta": ["alta"]
}



# NORMALIZAÇÃO DE ESTADOS DESCONHECIDOS

# Normaliza IMC e intensidade garantindo que as categorias usadas
# existam no grafo do BFS. Evita estados inválidos e garante que
# a busca sempre tenha vizinhos para explorar.


def normalizar_estado(imc_cat, intensidade_cat):
    if intensidade_cat not in vizinhos_intensidade:
        if intensidade_cat == "muito_alta":
            intensidade_cat = "muito_alta"   
        elif "alta" in intensidade_cat:
            intensidade_cat = "alta"
        elif "baixa" in intensidade_cat:
            intensidade_cat = "baixa"
        else:
            intensidade_cat = "moderada"

    if imc_cat not in vizinhos_imc:
        if "magreza" in imc_cat or "baixo" in imc_cat:
            imc_cat = "baixo"
        elif "normal" in imc_cat:
            imc_cat = "normal"
        elif "sobrepeso" in imc_cat:
            imc_cat = "sobrepeso"
        else:
            imc_cat = "obesidade"

    return imc_cat, intensidade_cat




# FUNÇÕES AUXILIARES

def gerar_filhos(estado):
    imc_cat, intensidade_cat = estado
    filhos = []
    
    for viz in vizinhos_imc.get(imc_cat, []):
        filhos.append((viz, intensidade_cat))
    
    for viz in vizinhos_intensidade.get(intensidade_cat, []):
        filhos.append((imc_cat, viz))

    return filhos

#Retorna True se existe uma regra válida na base de conhecimento.
def existe_regra(imc_cat, intensidade_cat):
    for regra in regras_dieta:
        if regra["imc"] == imc_cat and regra["intensidade"] == intensidade_cat:
            return True
    return False

#Retorna a dieta correspondente ao estado encontrado.
def obter_dieta(imc_cat, intensidade_cat):
    for regra in regras_dieta:
        if regra["imc"] == imc_cat and regra["intensidade"] == intensidade_cat:
            return regra["dieta"]
    return None



# BFS COMPLETO EM GRAFO DE ESTADOS

"""
Busca em largura para encontrar a dieta mais próxima.
- Estado inicial: (imc_inicial, intensidade_inicial)
- Objetivo: qualquer regra válida no grafo
"""
def bfs_busca_dieta(imc_inicial, intensidade_inicial):
    # Normalizar categorias antes de rodar BFS
    estado_inicial = normalizar_estado(imc_inicial, intensidade_inicial)

    fila = deque([estado_inicial])
    visitados = set([estado_inicial])

    while fila:
        estado = fila.popleft()
        imc_cat, intensidade_cat = estado

        # OBJETIVO: regra encontrada
        if existe_regra(imc_cat, intensidade_cat):
            return {
                "estado_encontrado": estado,
                "dieta": obter_dieta(imc_cat, intensidade_cat)
            }

        # EXPANDIR FILHOS
        for filho in gerar_filhos(estado):
            if filho not in visitados:
                visitados.add(filho)
                fila.append(filho)

    # Se nada for encontrado
    return {
        "estado_encontrado": None,
        "dieta": None
    }
