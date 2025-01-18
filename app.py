import os
import pulp
from moviepy import VideoFileClip

def obter_duracoes_dos_videos(caminho_pasta):
    # Lista para armazenar as durações dos vídeos
    duracoes = []
    
    # Verificar se o caminho é uma pasta
    if os.path.isdir(caminho_pasta):
        # Iterar pelos arquivos na pasta
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            
            # Verificar se é um arquivo de vídeo
            if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
                try:
                    # Obter a duração do vídeo em segundos
                    with VideoFileClip(caminho_arquivo) as video:
                        duracao = video.duration  # Duração em segundos
                        duracoes.append(duracao)
                except Exception as e:
                    print(f"Erro ao processar o vídeo {arquivo}: {e}")
    else:
        print(f"O caminho '{caminho_pasta}' não é uma pasta válida.")
    
    return duracoes

# Dados de entrada
duracao_comeco = obter_duracoes_dos_videos("./videos/comeco")  # exemplo de durações dos vídeos de "começo"
duracao_meio = obter_duracoes_dos_videos("./videos/meio")  # exemplo de durações dos vídeos de "meio"
duracao_fim = obter_duracoes_dos_videos("./videos/fim")         # exemplo de durações dos vídeos de "fim"
x = 1235                       # duração desejada
print("Duração começo", duracao_comeco)
print("Duração meio", duracao_meio)
print("Duração fim", duracao_fim)
# Criação do problema
problem = LpProblem("Montagem_Videos", LpMinimize)

# Variáveis de decisão
c = [LpVariable(f"c_{i}", cat="Binary") for i in range(len(duracao_comeco))]
m = [LpVariable(f"m_{j}", cat="Binary") for j in range(len(duracao_meio))]
f = [LpVariable(f"f_{k}", cat="Binary") for k in range(len(duracao_fim))]

# Restrições
problem += lpSum(c) == 1, "Uma escolha para começo"
problem += lpSum(f) == 1, "Uma escolha para fim"

# Soma das durações e diferença mínima
duracao_total = (
    lpSum(c[i] * duracao_comeco[i] for i in range(len(duracao_comeco))) +
    lpSum(m[j] * duracao_meio[j] for j in range(len(duracao_meio))) +
    lpSum(f[k] * duracao_fim[k] for k in range(len(duracao_fim)))
)

# Função objetivo
problem += abs(duracao_total - x), "Minimizar diferença"

# Resolver o problema
problem.solve()

# Resultado
print("Vídeos selecionados:")
print("Começo:", [i for i in range(len(c)) if c[i].varValue == 1])
print("Meio:", [j for j in range(len(m)) if m[j].varValue == 1])
print("Fim:", [k for k in range(len(f)) if f[k].varValue == 1])
print("Duração total:", duracao_total.value())