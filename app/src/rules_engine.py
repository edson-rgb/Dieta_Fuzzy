# ===========================================
# CLASSIFICAÇÃO DA INTENSIDADE CRISP
# ===========================================

def classificar_intensidade_categoria(intensidade: float) -> str:
    """
    Converte o valor fuzzy (0–10) em categoria linguística.
    """
    if intensidade < 3.5:
        return "baixa"
    elif intensidade < 6.5:
        return "moderada"
    else:
        return "alta"


# ===========================================
# REGRAS DO SISTEMA ESPECIALISTA
# ===========================================

regras_dieta = [
    {"imc": "baixo",      "intensidade": "baixa",     "dieta": "hipercalorica"},
    {"imc": "baixo",      "intensidade": "moderada",  "dieta": "hipercalorica"},
    {"imc": "baixo",      "intensidade": "alta",      "dieta": "hipercalorica"},

    {"imc": "normal",     "intensidade": "baixa",     "dieta": "balanceada"},
    {"imc": "normal",     "intensidade": "moderada",  "dieta": "balanceada"},
    {"imc": "normal",     "intensidade": "alta",      "dieta": "hipercalorica"},

    {"imc": "sobrepeso",  "intensidade": "baixa",     "dieta": "hipocalorica"},
    {"imc": "sobrepeso",  "intensidade": "moderada",  "dieta": "balanceada"},
    {"imc": "sobrepeso",  "intensidade": "alta",      "dieta": "balanceada"},

    {"imc": "obesidade",  "intensidade": "baixa",     "dieta": "hipocalorica"},
    {"imc": "obesidade",  "intensidade": "moderada",  "dieta": "hipocalorica"},
    {"imc": "obesidade",  "intensidade": "alta",      "dieta": "hipocalorica"},
]


