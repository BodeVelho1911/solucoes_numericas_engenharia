import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from projeto_final import f_RT_cambio, RT_relacao, R_pneu, f_torque, rho, Af, Cd, M, mi, m, g


# CÓDIGO PARA TESTE DO RPM DE TROCA DE MARCHA
# INPUTS INICIAIS
dt = 0.01  # Variação de tempo [s]
t0 = 0  # Tempo inicial [s]
v0 = 0  # Velocidade inicial [m/s]
t_final = 8  # Tempo final [s]
s0 = 0  # Posição inicial [m]
rpm_0 = 1500
rpm_troca = np.arange(4000, 7600, 100)  # Variação de RPM de troca
t_troca = 0.4

# Resultados para cada valor de rpm de troca
tempo_75m = np.zeros(len(rpm_troca))
velocidade_75m = np.zeros(len(rpm_troca))

# LOOP EXTERNO PARA VARIAR O RPM DE TROCA
for n in range(len(rpm_troca)):
    # Reinicializa as variáveis para cada simulação
    t = np.arange(t0, t_final + dt, dt)
    n_t = len(t)
    v = np.zeros(n_t)
    v[0] = v0
    s = np.zeros(n_t)
    s[0] = s0
    trocando_marcha = False
    marcha = 1

    # MÉTODO DE EULER PARA SIMULAÇÃO
    for i in range(0, n_t-1, 1):
        rpm = (60 * v[i] * f_RT_cambio(marcha) * RT_relacao) / (2 * np.pi * R_pneu)
        if rpm < rpm_0:  # Força o rpm ser maior ou igual a 1500
            rpm = rpm_0
        if rpm >= rpm_troca[n] and not trocando_marcha:  # Troca a marcha se rpm for maior ou igual ao rpm de troca
            trocando_marcha = True
            tempo_trocando = 0
        if trocando_marcha:  # Condições durante a troca
            F_tracao = 0
            tempo_trocando += dt
            if tempo_trocando >= t_troca:
                tempo_trocando = 0
                marcha += 1
                if marcha > 5:
                    marcha = 5  # Limitando à marcha máxima (5ª marcha)
                trocando_marcha = False
        else:
            F_tracao = (f_torque(rpm) * f_RT_cambio(marcha) * RT_relacao) / R_pneu  # Cálculo da força de tração

        F_arrasto = 0.5 * rho * ((v[i]) ** 2) * Af * Cd  # Cálculo da força de arrasto
        F_rol = mi * m * g  # Cálculo da força de resistência ao rolamento
        dv_dt = (F_tracao - F_arrasto - F_rol) / M  # EDO da velocidade
        ds_dt = v[i]  # EDO do deslocamento
        v[i + 1] = v[i] + dt * dv_dt  # Cálculo da velocidade
        s[i + 1] = s[i] + dt * ds_dt  # Cálculo do deslocamento

        # Condição de parada
        if s[i + 1] >= 75:
            tempo_75m[n] = t[i + 1]
            velocidade_75m[n] = v[i + 1]
            break

# Cria subgráficos para plotar
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Resultados da Simulação', fontsize=16)

# Gráfico de tempo total para 75 m x rpm de troca
axs[0].plot(rpm_troca, tempo_75m)
axs[0].set_xlabel('RPM de troca [1/min]')
axs[0].set_ylabel('Tempo para 75 m [s]')
axs[0].set_title('Relação do tempo total pelo RPM de troca de marcha')
axs[0].grid(True)

# Gráfico de velocidade x rpm de troca
axs[1].plot(rpm_troca, velocidade_75m)
axs[1].set_xlabel('RPM de troca [1/min]')
axs[1].set_ylabel('Velocidade [m/s]')
axs[1].set_title('Relação da velocidade final pelo RPM de troca de marcha')
axs[1].grid(True)

# Ajustar layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
