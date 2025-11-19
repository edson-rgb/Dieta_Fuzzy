# app/src/fuzzy_engine.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ===========================================
# VARIÁVEIS FUZZY
# ===========================================

atividade = ctrl.Antecedent(np.arange(0, 11, 1), 'atividade')
esforco = ctrl.Antecedent(np.arange(0, 11, 1), 'esforco')
intensidade_nivel = ctrl.Consequent(np.arange(0, 11, 1), 'intensidade_nivel')

atividade['sedentario'] = fuzz.trimf(atividade.universe, [0, 0, 3])
atividade['pouco_ativo'] = fuzz.trimf(atividade.universe, [2, 4, 6])
atividade['moderadamente_ativo'] = fuzz.trimf(atividade.universe, [5, 7, 9])
atividade['muito_ativo'] = fuzz.trimf(atividade.universe, [7, 10, 10])

esforco['leve'] = fuzz.trimf(esforco.universe, [0, 0, 4])
esforco['moderado'] = fuzz.trimf(esforco.universe, [2, 5, 7])
esforco['pesado'] = fuzz.trimf(esforco.universe, [6, 8, 9])
esforco['muito_pesado'] = fuzz.trimf(esforco.universe, [8, 10, 10])


intensidade_nivel['baixa'] = fuzz.trimf(intensidade_nivel.universe, [0, 0, 4])
intensidade_nivel['moderada'] = fuzz.trimf(intensidade_nivel.universe, [3, 5, 7])
intensidade_nivel['alta'] = fuzz.trimf(intensidade_nivel.universe, [6, 8, 9])
intensidade_nivel['muito_alta'] = fuzz.trimf(intensidade_nivel.universe, [8, 10, 10])



# ===========================================
# REGRAS FUZZY (Matriz completa)
# ===========================================

regras = [
    # Sedentário
    ctrl.Rule(atividade['sedentario'] & esforco['leve'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade['sedentario'] & esforco['moderado'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade['sedentario'] & esforco['pesado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade['sedentario'] & esforco['muito_pesado'], intensidade_nivel['alta']),

    # Pouco ativo
    ctrl.Rule(atividade['pouco_ativo'] & esforco['leve'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade['pouco_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade['pouco_ativo'] & esforco['pesado'], intensidade_nivel['alta']),
    ctrl.Rule(atividade['pouco_ativo'] & esforco['muito_pesado'], intensidade_nivel['muito_alta']),

    # Moderadamente ativo
    ctrl.Rule(atividade['moderadamente_ativo'] & esforco['leve'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade['moderadamente_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade['moderadamente_ativo'] & esforco['pesado'], intensidade_nivel['alta']),
    ctrl.Rule(atividade['moderadamente_ativo'] & esforco['muito_pesado'], intensidade_nivel['muito_alta']),

    # Muito ativo
    ctrl.Rule(atividade['muito_ativo'] & esforco['leve'], intensidade_nivel['alta']),
    ctrl.Rule(atividade['muito_ativo'] & esforco['moderado'], intensidade_nivel['muito_alta']),
    ctrl.Rule(atividade['muito_ativo'] & esforco['pesado'], intensidade_nivel['muito_alta']),
    ctrl.Rule(atividade['muito_ativo'] & esforco['muito_pesado'], intensidade_nivel['muito_alta']),
]


sistema_intensidade = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema_intensidade)


# ===========================================
# FUNÇÃO PRINCIPAL
# ===========================================

def calcular_intensidade_fuzzy(atividade_texto: str, esforco_rpe: float):
    mapa = {
        "Sedentário": 1,
        "Pouco ativo": 4,
        "Moderadamente ativo": 6,
        "Muito ativo": 9,
    }

    simulador.input['atividade'] = mapa[atividade_texto]
    simulador.input['esforco'] = esforco_rpe
    simulador.compute()

    valor = float(simulador.output['intensidade_nivel'])

    if valor < 3.5: categoria = "baixa"
    elif valor < 6.5: categoria = "moderada"
    else: categoria = "alta"

    return valor, categoria
