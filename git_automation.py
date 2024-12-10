
import os

# Função para executar comandos do Git
def run_git_commands(repo_dir, message):
    try:
        # Navegar para o diretório do repositório
        os.chdir(repo_dir)
        print(f"Diretório atual: {os.getcwd()}")

        # Adicionar todos os arquivos modificados
        os.system("git add .")
        print("Arquivos adicionados.")

        # Commit com a mensagem fornecida
        os.system(f'git commit -m "{message}"')
        print(f'Commit feito com a mensagem: "{message}"')

        # Push para o repositório remoto
        os.system("git push origin main")
        print("Alterações enviadas para o GitHub.")
    except Exception as e:
        print(f"Erro: {e}")

# Configurações
repo_dir = "/content/solucoes_numericas_engenharia"  # Caminho do repositório no Colab
commit_message = "Colab updates"  # Mensagem de commit padrão

# Executando os comandos Git
run_git_commands(repo_dir, commit_message)
