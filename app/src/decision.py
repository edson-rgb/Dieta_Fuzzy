from .imc import calcular_imc, classificar_imc
from .fuzzy_engine import calcular_intensidade_fuzzy
from .bfs_engine import bfs_busca_dieta


def inferir_dieta(peso, altura, esforco, atividade):
    imc = calcular_imc(peso, altura)
    descricao_imc, imc_cat = classificar_imc(imc)

    intensidade_valor, intensidade_cat = calcular_intensidade_fuzzy(
        atividade, esforco
    )

    resultado_bfs = bfs_busca_dieta(imc_cat, intensidade_cat)

    return {
        "imc": imc,
        "categoria_imc": descricao_imc,
        "imc_cat": imc_cat,
        "intensidade": intensidade_valor,
        "intensidade_cat": intensidade_cat,
        "dieta": resultado_bfs["dieta"],
        "estado_usado": resultado_bfs["estado_encontrado"],
    }
