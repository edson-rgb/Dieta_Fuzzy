def calcular_imc(peso: float, altura: float) -> float:
    return peso / (altura ** 2)


def classificar_imc_descritivo(imc: float) -> str:
    if imc < 16:
        return "Magreza extrema"
    elif imc < 18.5:
        return "Magreza"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 40:
        return "Obesidade"
    else:
        return "Obesidade mórbida"


def classificar_imc_faixa(imc: float) -> str:
    """
    Categorias simplificadas para regras e BFS.
    """
    if imc < 18.5:
        return "baixo"
    elif imc < 25:
        return "normal"
    elif imc < 30:
        return "sobrepeso"
    else:
        return "obesidade"


def classificar_imc(imc: float) -> tuple[str, str]:
    """
    Função única chamada pelo sistema.
    Retorna:
    - descrição completa (para UI)
    - categoria simplificada (para BFS)
    """
    return (
        classificar_imc_descritivo(imc),
        classificar_imc_faixa(imc)
    )
