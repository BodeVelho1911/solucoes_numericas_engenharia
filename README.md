# Soluções Numéricas para Problemas em Engenharia
Repositório para armazenar o conteúdo proposto na disciplina Soluções Numéricas para Problemas em Engenharia do curso de Engenharia Mecânica da UFTM

## Arquivo projeto_final.py
    Contém o projeto final da matéria, que se trata de um simulador da prova de aceleração para projetos de Fórmula SAE. O arquivo utiliza de dados da equipe Taurus Racing UFTM
para a simulação da prova de aceleração em 75 m, mas podem ser utilizados dados de outros projetos SAE para análise de desempenho nesta prova. O script tem como output a 
velocidade ao final da pista e o tempo para o percurso. Também plota os gráficos de velocidade, deslocamento, velocidade angular do motor (RPM), força de arrasto, força de tração 
nas rodas e força de resistência ao rolamento, todas no domínio do tempo. Para a análise foi simulada a troca de marcha em 5100 RPM.

## Arquivo proj_final_RPM.py
    Neste script há importação de algumas funções e variáveis do arquivo projeto_final.py. Foi desenvolvido para fazer a análise de velocidade angular de troca de marcha, onde o 
script varia a mesma entre 4000 e 7500 RPM, para plotar gráficos do tempo total para percorrer os 75 m de pista e a velocidade final, ambos no domínio da velocidade angular 
do motor 
