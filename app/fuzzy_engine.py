import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ===========================================
# 1) VARIÁVEIS FUZZY
# ===========================================

# ---------- Sistema 1: Atividade + Esforço → Intensidade agregada ----------

atividade_fisica = ctrl.Antecedent(np.arange(0, 11, 1), 'atividade_fisica')
esforco = ctrl.Antecedent(np.arange(0, 11, 1), 'esforco')
intensidade_nivel = ctrl.Consequent(np.arange(0, 11, 1), 'intensidade_nivel')

# Atividade diária
atividade_fisica['sedentario']          = fuzz.trimf(atividade_fisica.universe, [0, 0, 3])
atividade_fisica['pouco_ativo']         = fuzz.trimf(atividade_fisica.universe, [2, 4, 6])
atividade_fisica['moderadamente_ativo'] = fuzz.trimf(atividade_fisica.universe, [5, 7, 9])
atividade_fisica['muito_ativo']         = fuzz.trimf(atividade_fisica.universe, [7, 10, 10])

# Esforço percebido RPE
esforco['leve']         = fuzz.trimf(esforco.universe, [0, 0, 4])
esforco['moderado']     = fuzz.trimf(esforco.universe, [2, 5, 7])
esforco['pesado']       = fuzz.trimf(esforco.universe, [6, 8, 9])
esforco['muito_pesado'] = fuzz.trimf(esforco.universe, [8, 10, 10])

# Intensidade agregada
intensidade_nivel['baixa']      = fuzz.trimf(intensidade_nivel.universe, [0, 0, 4])
intensidade_nivel['moderada']   = fuzz.trimf(intensidade_nivel.universe, [3, 5, 7])
intensidade_nivel['alta']       = fuzz.trimf(intensidade_nivel.universe, [6, 8, 9])
intensidade_nivel['muito_alta'] = fuzz.trimf(intensidade_nivel.universe, [8, 10, 10])

# ---------- Sistema 2: IMC + Intensidade → Tipo de dieta ----------

imc_var = ctrl.Antecedent(np.arange(10, 61, 1), 'imc')
intensidade_final = ctrl.Antecedent(np.arange(0, 11, 1), 'intensidade_final')
dieta = ctrl.Consequent(np.arange(0, 11, 1), 'dieta')

# IMC atualizado com "muito alto"
imc_var['muito_baixo'] = fuzz.trimf(imc_var.universe, [10, 13, 17])
imc_var['baixo']       = fuzz.trimf(imc_var.universe, [15, 18, 21])
imc_var['normal']      = fuzz.trimf(imc_var.universe, [19, 23, 28])
imc_var['alto']        = fuzz.trimf(imc_var.universe, [26, 35, 40])
imc_var['muito_alto']  = fuzz.trimf(imc_var.universe, [38, 50, 60])  # obesidade mórbida

# intensidade final = mesma semântica do sistema 1
intensidade_final['baixa']      = fuzz.trimf(intensidade_final.universe, [0, 0, 4])
intensidade_final['moderada']   = fuzz.trimf(intensidade_final.universe, [3, 5, 7])
intensidade_final['alta']       = fuzz.trimf(intensidade_final.universe, [6, 8, 9])
intensidade_final['muito_alta'] = fuzz.trimf(intensidade_final.universe, [8, 10, 10])

# Dieta
dieta['hipocalorica']  = fuzz.trimf(dieta.universe, [0, 0, 5])
dieta['balanceada']    = fuzz.trimf(dieta.universe, [4, 5, 8])
dieta['hipercalorica'] = fuzz.trimf(dieta.universe, [7, 10, 10])


# ===========================================
# 2) REGRAS FUZZY
# ===========================================

# ---------- Sistema 1: Regras de intensidade ----------
regras_intensidade = [
    ctrl.Rule(atividade_fisica['sedentario'] & esforco['leve'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade_fisica['sedentario'] & esforco['moderado'], intensidade_nivel['baixa']),
    ctrl.Rule(atividade_fisica['pouco_ativo'] & esforco['leve'], intensidade_nivel['baixa']),

    ctrl.Rule(atividade_fisica['pouco_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['leve'], intensidade_nivel['moderada']),
    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['moderado'], intensidade_nivel['moderada']),

    ctrl.Rule(atividade_fisica['moderadamente_ativo'] & esforco['pesado'], intensidade_nivel['alta']),
    ctrl.Rule(atividade_fisica['pouco_ativo'] & esforco['pesado'], intensidade_nivel['alta']),
    ctrl.Rule(atividade_fisica['muito_ativo'] & esforco['leve'], intensidade_nivel['alta']),

    ctrl.Rule(atividade_fisica['muito_ativo'] & esforco['moderado'], intensidade_nivel['muito_alta']),
    ctrl.Rule(atividade_fisica['muito_ativo'] & esforco['pesado'], intensidade_nivel['muito_alta']),
    ctrl.Rule(esforco['muito_pesado'], intensidade_nivel['muito_alta']),
]

sistema_intensidade = ctrl.ControlSystem(regras_intensidade)


# ---------- Sistema 2: Regras da dieta ----------
regras_dieta = [

    ctrl.Rule(imc_var['muito_alto'], dieta['hipocalorica']),  # novo IMC extremo

    ctrl.Rule(imc_var['alto'] & intensidade_final['baixa'], dieta['hipocalorica']),
    ctrl.Rule(imc_var['alto'] & intensidade_final['moderada'], dieta['hipocalorica']),

    ctrl.Rule(imc_var['normal'] & intensidade_final['baixa'], dieta['balanceada']),
    ctrl.Rule(imc_var['normal'] & intensidade_final['moderada'], dieta['balanceada']),
    ctrl.Rule(imc_var['normal'] & intensidade_final['alta'], dieta['hipercalorica']),

    ctrl.Rule(imc_var['baixo'] & intensidade_final['alta'], dieta['hipercalorica']),
    ctrl.Rule(imc_var['baixo'] & intensidade_final['muito_alta'], dieta['hipercalorica']),
    ctrl.Rule(imc_var['muito_baixo'], dieta['hipercalorica']),

    ctrl.Rule(intensidade_final['muito_alta'], dieta['hipercalorica'])
]

sistema_dieta = ctrl.ControlSystem(regras_dieta)


# ===========================================
# 3) FUNÇÕES AUXILIARES
# ===========================================

def classificar_imc(imc):
    if imc < 16: return "Magreza extrema"
    if imc < 18.5: return "Magreza"
    if imc < 25: return "Normal"
    if imc < 30: return "Sobrepeso"
    if imc < 40: return "Obesidade"
    return "Obesidade mórbida"


# Harris–Benedict atualizado
def calcular_tmb(peso, altura, idade, sexo):
    altura_cm = altura * 100
    if sexo == "Masculino":
        return 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * idade)
    else:
        return 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * idade)


# ===========================================
# 4) FUNÇÃO PRINCIPAL
# ===========================================

def inferir_dieta(peso, altura, esforco_rpe, atividade_texto):
    imc = peso / (altura ** 2)
    classificacao = classificar_imc(imc)

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

    motor_d = ctrl.ControlSystemSimulation(sistema_dieta)
    motor_d.input['imc'] = imc
    motor_d.input['intensidade_final'] = intensidade_crisp
    motor_d.compute()

    valor_dieta = motor_d.output['dieta']

    return imc, classificacao, intensidade_crisp, valor_dieta
