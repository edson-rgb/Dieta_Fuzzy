import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ===========================================
# 1) VARIÁVEIS FUZZY
# ===========================================

atividade_fisica = ctrl.Antecedent(np.arange(0, 11, 1), 'atividade_fisica')
esforco = ctrl.Antecedent(np.arange(0, 11, 1), 'esforco')
intensidade_nivel = ctrl.Consequent(np.arange(0, 11, 1), 'intensidade_nivel')

# Atividade diária
atividade_fisica['sedentario'] = fuzz.trimf(atividade_fisica.universe, [0, 0, 3])
atividade_fisica['pouco_ativo'] = fuzz.trimf(atividade_fisica.universe, [2, 4, 6])
atividade_fisica['moderadamente_ativo'] = fuzz.trimf(atividade_fisica.universe, [5, 7, 9])
atividade_fisica['muito_ativo'] = fuzz.trimf(atividade_fisica.universe, [7, 10, 10])

# Esforço percebido RPE
esforco['leve'] = fuzz.trimf(esforco.universe, [0, 0, 4])
esforco['moderado'] = fuzz.trimf(esforco.universe, [2, 5, 7])
esforco['pesado'] = fuzz.trimf(esforco.universe, [6, 8, 9])
esforco['muito_pesado'] = fuzz.trimf(esforco.universe, [8, 10, 10])

# Intensidade agregada
intensidade_nivel['baixa'] = fuzz.trimf(intensidade_nivel.universe, [0, 0, 4])
intensidade_nivel['moderada'] = fuzz.trimf(intensidade_nivel.universe, [3, 5, 7])
intensidade_nivel['alta'] = fuzz.trimf(intensidade_nivel.universe, [6, 8, 9])
intensidade_nivel['muito_alta'] = fuzz.trimf(intensidade_nivel.universe, [8, 10, 10])

# Sistema de regras para intensidade
regras_intensidade = [
    ctrl.Rule(atividade_fisica['sedentario'] & esforco['leve'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade_fisica['sedentario'] & esforco['moderado'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade_fisica['pouco_ativo'] & esforco['leve'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade_fisica['pouco_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['leve'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['pesado'], intensidade_nivel['alta']),
    ctrl.Rule(atividade_fisica['muito_ativo'] & esforco['leve'], intensidade_nivel['alta']),
    ctrl.Rule(atividade_fisica['muito_ativo'] & esforco['moderado'], intensidade_nivel['muito_alta']),
    ctrl.Rule(esforco['muito_pesado'], intensidade_nivel['muito_alta'])
]

sistema_intensidade = ctrl.ControlSystem(regras_intensidade)


# ===========================================
# 2) FUNÇÕES AUXILIARES
# ===========================================

def classificar_imc(imc):
    if imc < 16: return "Magreza extrema"
    if imc < 18.5: return "Magreza"
    if imc < 25: return "Normal"
    if imc < 30: return "Sobrepeso"
    if imc < 40: return "Obesidade"
    return "Obesidade mórbida"


def determinar_dieta(imc, intensidade):
    if imc < 18.5:
        return "hipercalorica"
    elif imc < 25:
        return "balanceada" if intensidade < 5 else "hipercalorica"
    elif imc < 30:
        return "hipocalorica" if intensidade < 5 else "balanceada"
    else:
        return "hipocalorica"

#Calcular taxa metabólica basal (tmb) de acordo com a fórmula de Mifflin-St Jeor
def calcular_tmb(peso, altura, idade, sexo, atividade_fisica):
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
        "Extremamente ativo": 1.9
    }

    return tmb * fatores.get(atividade_fisica)


# ===========================================
# 3) FUNÇÃO PRINCIPAL
# ===========================================

def inferir_dieta(peso, altura, esforco_rpe, atividade_texto):
    imc = peso / (altura ** 2)
    categoria = classificar_imc(imc)

    mapa_atividade = {
        "Sedentário": 1,
        "Pouco ativo": 4,
        "Moderadamente ativo": 6,
        "Muito ativo": 9,
    }

    motor_i = ctrl.ControlSystemSimulation(sistema_intensidade)
    motor_i.input['atividade_fisica'] = mapa_atividade[atividade_texto]
    motor_i.input['esforco'] = esforco_rpe
    motor_i.compute()

    intensidade_crisp = motor_i.output['intensidade_nivel']
    tipo_dieta = determinar_dieta(imc, intensidade_crisp)

    return imc, categoria, intensidade_crisp, tipo_dieta
