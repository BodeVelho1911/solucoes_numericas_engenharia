import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# DADOS DO PROJETO
Cd = 0.2 # Coeficiente de arrasto
rho = 1.14 # Densidade do ar atmosférico [kg/m³]
Af = 1.2 # Área frontal do carro [m²]
R_pneu = 0.25 # Raio do pneu [m]
m = 330 # Massa do carro + piloto [kg]
I_motor = 0.022 # Inercia do motor
I_cambio = 0.019 # Inercia do câmbio
I_roda = 0.03 # Inercia das rodas
mi = 0.02 # Coeficiente de resistência ao rolamento
g = 9.81 # Aceleração da gravidade [m/s²]
RT_relacao = 2.625 # Relação de transmissão do conjunto pinhão-coroa

# Relação de transmissão do câmbio em função da marcha
RT_cambio = np.array([4.09, 2.683, 1.95, 1.575, 1.312])
def f_RT_cambio(marcha):
    return RT_cambio[marcha - 1]

# Torque em função do RPM
rpm_motor = np.arange(1500, 8000, 500)
T_motor = np.array([45, 48, 51, 53, 53, 55, 57, 59, 58, 56, 54, 52, 49])

# Interpolação do Torque por RPM
f_torque = CubicSpline(rpm_motor, T_motor)

# Inércia total do carro
M = m + (I_motor + I_cambio + I_roda) / (R_pneu ** 2)

# Função Principal para Simulação
def simular_corrida():
    # INPUTS INICIAIS
    dt = 0.01 # Variação de tempo [s]
    t0 = 0  # Tempo inicial [s]
    v0 = 0 # Velocidade inicial [m/s]
    t_final = 8 # Tempo final [s]
    s0 = 0 # Posição inicial [m]
    rpm_0 = 1500
    rpm_troca = 5100
    t_troca = 0.4
    trocando_marcha = False
    marcha = 1

    # INICIALIZAÇÃO DA SOLUÇÃO DE VELOCIDADE
    t = np.arange(t0, t_final + dt, dt)
    n = len(t)
    v = np.zeros(n)
    v[0] = v0
    s = np.zeros(n)
    s[0] = s0
    rpm_plot = np.zeros(n)
    F_tracao_plot = np.zeros(n)
    F_arrasto_plot = np.zeros(n)
    F_rol_plot = np.zeros(n)

    # MÉTODO DE EULER
    for i in range(0, n-1, 1):
        rpm = (60 * v[i] * f_RT_cambio(marcha) * RT_relacao) / (2 * np.pi * R_pneu)
        if rpm < rpm_0:
            rpm = rpm_0
        if rpm >= rpm_troca and not trocando_marcha:
            trocando_marcha = True
            tempo_trocando = 0
        if trocando_marcha:
            F_tracao = 0
            tempo_trocando += dt
            if tempo_trocando >= t_troca:
                tempo_trocando = 0
                marcha += 1
                if marcha > 5:
                    marcha = 5
                trocando_marcha = False
        else:
            F_tracao = (f_torque(rpm) * f_RT_cambio(marcha) * RT_relacao) / R_pneu

        F_arrasto = 0.5 * rho * ((v[i]) ** 2) * Af * Cd
        F_rol = mi * m * g
        dv_dt = (F_tracao - F_arrasto - F_rol) / M
        ds_dt = v[i]
        v[i + 1] = v[i] + dt * dv_dt
        s[i + 1] = s[i] + dt * ds_dt

        rpm_plot[i] = rpm
        F_tracao_plot[i] = F_tracao
        F_arrasto_plot[i] = F_arrasto
        F_rol_plot[i] = F_rol

        if s[i + 1] >= 75:
            tempo_75m = t[i + 1]
            velocidade_75m = v[i + 1]
            break

    t = t[0 : i + 2]
    v = v[0 : i + 2]
    s = s[0 : i + 2]
    rpm_plot = rpm_plot[0 : i + 2]
    F_tracao_plot = F_tracao_plot[0 : i + 2]
    F_arrasto_plot = F_arrasto_plot[0 : i + 2]
    F_rol_plot = F_rol_plot[0 : i + 2]

    print(f"Tempo para percorrer 75 m: {tempo_75m:.4f} s")
    print(f"Velocidade no final da pista: {velocidade_75m:.4f} m/s")

    # Criar os subgráficos para plotar todos de uma vez
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle('Resultados da Simulação', fontsize=16)

    # Gráfico de velocidade x tempo
    axs[0, 0].plot(t, v)
    axs[0, 0].set_title('Velocidade do Carro')
    axs[0, 0].set_xlabel('Tempo [s]')
    axs[0, 0].set_ylabel('Velocidade [m/s]')
    axs[0, 0].grid(True)

    # Gráfico de deslocamento x tempo
    axs[0, 1].plot(t, s)
    axs[0, 1].set_title('Deslocamento do Carro')
    axs[0, 1].set_xlabel('Tempo [s]')
    axs[0, 1].set_ylabel('Posição [m]')
    axs[0, 1].grid(True)

    # Gráfico de RPM x tempo
    axs[1, 0].plot(t, rpm_plot)
    axs[1, 0].set_title('Rotação do Motor (RPM)')
    axs[1, 0].set_xlabel('Tempo [s]')
    axs[1, 0].set_ylabel('RPM')
    axs[1, 0].grid(True)

    # Gráfico da força de tração x tempo
    axs[1, 1].plot(t, F_tracao_plot)
    axs[1, 1].set_title('Tração nas Rodas')
    axs[1, 1].set_xlabel('Tempo [s]')
    axs[1, 1].set_ylabel('Tração [N]')
    axs[1, 1].grid(True)

    # Gráfico da força de arrasto x tempo
    axs[2, 0].plot(t, F_arrasto_plot)
    axs[2, 0].set_title('Força de Arrasto')
    axs[2, 0].set_xlabel('Tempo [s]')
    axs[2, 0].set_ylabel('Arrasto [N]')
    axs[2, 0].grid(True)

    # Gráfico da força de rolamento x tempo
    axs[2, 1].plot(t, F_rol_plot)
    axs[2, 1].set_title('Resistência ao Rolamento')
    axs[2, 1].set_xlabel('Tempo [s]')
    axs[2, 1].set_ylabel('Resistência [N]')
    axs[2, 1].grid(True)

    # Ajustar layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# Condicional para execução direta
if __name__ == "__main__":
    simular_corrida()
