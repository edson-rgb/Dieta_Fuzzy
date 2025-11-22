#Calcula a TMB usando Mifflin-St Jeor e aplica o fator de atividade.
def calcular_tmb(peso: float, altura: float, idade: int, sexo: str, atividade_fisica: str) -> float:
    altura_cm = altura * 100

    if sexo == "Masculino":
        tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) - 161

    fatores = {
        "Sedentário": 1.2,
        "Pouco ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
    }

    return tmb * fatores.get(atividade_fisica, 1.2)
