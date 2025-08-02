"""
Constantes compartilhadas para o módulo simples.
"""

# Tipos de grafos suportados
TIPOS_GRAFOS = {
    0: "Simples",
    1: "Digrafo",
    20: "Multigrafo",
    21: "Multigrafo-Dirigido",
    30: "Pseudografo",
    31: "Pseudografo-Dirigido",
}

# Tipos de grafos dirigidos
TIPOS_DIRIGIDOS = [1, 21, 31]

# Tipos de multigrafos
TIPOS_MULTIGRAFOS = [20, 21, 30, 31]

# Tipos de pseudografos (com laços)
TIPOS_PSEUDOGRAFOS = [30, 31]

# Tipos de grafos simples (não dirigidos)
TIPOS_SIMPLES = [0, 20, 30]

# Estratégias de geração
GERACAO = {
    0: "Aleatório",
    1: "Parcialmente Balanceado", 
    2: "Balanceado"
}

# Preferências de densidade
DENSIDADE = {
    0: "Sem preferência",
    1: "Esparso (densidade ≤ 0.2)",
    2: "Denso (densidade ≥ 0.8)"
}

# Parâmetros padrão
MAX_TENTATIVAS = 100
MAX_AMOSTRAS_HOP = 10000
PESO_MIN_PADRAO = 1
PESO_MAX_PADRAO = 10

# Configurações de teste
NUM_EXECUCOES_PADRAO = 5
VERTICES_LISTA_PADRAO = [1000, 5000]

# Configurações de densidade
DENSIDADE_ESPARSA_MAX = 0.2
DENSIDADE_DENSA_MIN = 0.8 