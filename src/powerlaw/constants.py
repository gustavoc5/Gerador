"""
Constantes compartilhadas para o módulo powerlaw.
"""

# Tipos de grafos suportados
TIPOS_GRAFOS = {
    0: 'Simples',
    1: 'Digrafo', 
    20: 'Multigrafo',
    21: 'Multigrafo-Dirigido',
    30: 'Pseudografo',
    31: 'Pseudografo-Dirigido'
}

# Tipos de grafos dirigidos
TIPOS_DIRIGIDOS = [1, 21, 31]

# Tipos de multigrafos
TIPOS_MULTIGRAFOS = [20, 21, 30, 31]

# Tipos de pseudografos (com laços)
TIPOS_PSEUDOGRAFOS = [30, 31]

# Parâmetros padrão
GAMMA_MIN = 2.0
GAMMA_MAX = 3.0
GRAU_MIN_PADRAO = 1
XMIN_POWERLAW = 2
KS_THRESHOLD = 0.1

# Configurações de teste
NUM_EXECUCOES_PADRAO = 5
VERTICES_LISTA_PADRAO = [1000, 5000]
MAX_AMOSTRAS_HOP = 10000

# Configurações de visualização
MAX_NOS_VISUALIZACAO = 300
TAMANHO_NOS_PEQUENOS = 100 