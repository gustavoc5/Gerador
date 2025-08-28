#!/usr/bin/env python3
"""
MÉTRICAS DE EQUIVALÊNCIA ESTRUTURAL ENTRE REPLICAÇÕES
Analisa a similaridade estrutural entre grafos gerados com os mesmos parâmetros.
"""

import numpy as np
import networkx as nx
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import silhouette_score
import itertools

def calcular_similaridade_entre_grafos(grafo1, grafo2):
    """
    Calcula similaridade estrutural entre dois grafos.
    
    Args:
        grafo1, grafo2: NetworkX Graph ou DiGraph
        
    Returns:
        similaridade: Valor entre 0 e 1
    """
    # Garante que ambos têm o mesmo número de nós
    n1, n2 = grafo1.number_of_nodes(), grafo2.number_of_nodes()
    if n1 != n2:
        return 0.0
    
    n = n1
    
    # Calcula matriz de adjacência para ambos
    adj1 = nx.adjacency_matrix(grafo1).toarray()
    adj2 = nx.adjacency_matrix(grafo2).toarray()
    
    # Calcula similaridade baseada na estrutura de conexões
    # Método 1: Similaridade de Jaccard das matrizes
    intersection = np.sum((adj1 == 1) & (adj2 == 1))
    union = np.sum((adj1 == 1) | (adj2 == 1))
    
    if union == 0:
        return 1.0  # Ambos vazios
    
    similaridade_jaccard = intersection / union
    
    # Método 2: Correlação das matrizes
    if np.std(adj1) > 0 and np.std(adj2) > 0:
        correlacao = np.corrcoef(adj1.flatten(), adj2.flatten())[0, 1]
        if np.isnan(correlacao):
            correlacao = 0.0
    else:
        correlacao = 0.0
    
    # Método 3: Similaridade de distribuição de graus
    graus1 = [d for n, d in grafo1.degree()]
    graus2 = [d for n, d in grafo2.degree()]
    
    if len(graus1) == len(graus2) and len(graus1) > 0:
        graus1 = np.array(graus1)
        graus2 = np.array(graus2)
        
        if np.std(graus1) > 0 and np.std(graus2) > 0:
            correlacao_graus = np.corrcoef(graus1, graus2)[0, 1]
            if np.isnan(correlacao_graus):
                correlacao_graus = 0.0
        else:
            correlacao_graus = 0.0
    else:
        correlacao_graus = 0.0
    
    # Combina as métricas (média ponderada)
    similaridade_final = (0.4 * similaridade_jaccard + 
                         0.3 * max(0, correlacao) + 
                         0.3 * max(0, correlacao_graus))
    
    return similaridade_final

def analisar_equivalencia_replicacoes(lista_grafos):
    """
    Analisa equivalência estrutural entre uma lista de grafos replicados.
    
    Args:
        lista_grafos: Lista de NetworkX Graph/DiGraph
        
    Returns:
        metricas: Dicionário com métricas de equivalência
    """
    n_grafos = len(lista_grafos)
    
    if n_grafos < 2:
        return {
            'n_grafos': n_grafos,
            'similaridade_media': 1.0,
            'similaridade_desvio': 0.0,
            'similaridade_min': 1.0,
            'similaridade_max': 1.0,
            'consistencia_estrutural': 1.0,
            'pares_altamente_similares': 0,
            'pares_medianamente_similares': 0,
            'pares_pouco_similares': 0
        }
    
    # Calcula similaridade entre todos os pares
    similaridades = []
    for i, j in itertools.combinations(range(n_grafos), 2):
        sim = calcular_similaridade_entre_grafos(lista_grafos[i], lista_grafos[j])
        similaridades.append(sim)
    
    similaridades = np.array(similaridades)
    
    # Estatísticas básicas
    metricas = {
        'n_grafos': n_grafos,
        'n_pares': len(similaridades),
        'similaridade_media': np.mean(similaridades),
        'similaridade_mediana': np.median(similaridades),
        'similaridade_desvio': np.std(similaridades),
        'similaridade_min': np.min(similaridades),
        'similaridade_max': np.max(similaridades),
        'similaridade_q25': np.percentile(similaridades, 25),
        'similaridade_q75': np.percentile(similaridades, 75)
    }
    
    # Classificação dos pares
    metricas['pares_altamente_similares'] = np.sum(similaridades > 0.8)
    metricas['pares_medianamente_similares'] = np.sum((similaridades > 0.5) & (similaridades <= 0.8))
    metricas['pares_pouco_similares'] = np.sum(similaridades <= 0.5)
    
    # Frações
    total_pares = len(similaridades)
    metricas['fracao_altamente_similares'] = metricas['pares_altamente_similares'] / total_pares
    metricas['fracao_medianamente_similares'] = metricas['pares_medianamente_similares'] / total_pares
    metricas['fracao_pouco_similares'] = metricas['pares_pouco_similares'] / total_pares
    
    # Consistência estrutural (quão similares são os grafos em geral)
    metricas['consistencia_estrutural'] = metricas['similaridade_media']
    
    # Coeficiente de variação (desvio/mean)
    if metricas['similaridade_media'] > 0:
        metricas['coeficiente_variacao'] = metricas['similaridade_desvio'] / metricas['similaridade_media']
    else:
        metricas['coeficiente_variacao'] = 0.0
    
    return metricas

def comparar_consistencia_geradores(lista_grafos_simples, lista_grafos_powerlaw):
    """
    Compara a consistência estrutural entre geradores.
    
    Args:
        lista_grafos_simples: Lista de grafos do gerador simples
        lista_grafos_powerlaw: Lista de grafos do gerador power-law
        
    Returns:
        comparacao: Dicionário com comparações
    """
    metricas_simples = analisar_equivalencia_replicacoes(lista_grafos_simples)
    metricas_powerlaw = analisar_equivalencia_replicacoes(lista_grafos_powerlaw)
    
    comparacao = {
        'simples': metricas_simples,
        'powerlaw': metricas_powerlaw,
        'diferenca_similaridade_media': metricas_powerlaw['similaridade_media'] - metricas_simples['similaridade_media'],
        'diferenca_consistencia': metricas_powerlaw['consistencia_estrutural'] - metricas_simples['consistencia_estrutural'],
        'diferenca_coeficiente_variacao': metricas_powerlaw['coeficiente_variacao'] - metricas_simples['coeficiente_variacao']
    }
    
    return comparacao

def detectar_outliers_estruturais(lista_grafos, threshold=2.0):
    """
    Detecta grafos que são outliers estruturais entre as replicações.
    
    Args:
        lista_grafos: Lista de grafos replicados
        threshold: Limiar para considerar outlier (desvios padrão)
        
    Returns:
        outliers: Lista de índices dos grafos outliers
        metricas_outliers: Métricas dos outliers
    """
    n_grafos = len(lista_grafos)
    if n_grafos < 3:
        return [], {}
    
    # Calcula similaridade média de cada grafo com os outros
    similaridades_por_grafo = []
    
    for i in range(n_grafos):
        similaridades = []
        for j in range(n_grafos):
            if i != j:
                sim = calcular_similaridade_entre_grafos(lista_grafos[i], lista_grafos[j])
                similaridades.append(sim)
        
        similaridades_por_grafo.append(np.mean(similaridades))
    
    similaridades_por_grafo = np.array(similaridades_por_grafo)
    
    # Detecta outliers usando z-score
    media = np.mean(similaridades_por_grafo)
    desvio = np.std(similaridades_por_grafo)
    
    if desvio == 0:
        return [], {}
    
    z_scores = np.abs((similaridades_por_grafo - media) / desvio)
    outliers = np.where(z_scores > threshold)[0].tolist()
    
    metricas_outliers = {
        'n_outliers': len(outliers),
        'indices_outliers': outliers,
        'similaridade_media_outliers': np.mean(similaridades_por_grafo[outliers]) if len(outliers) > 0 else 0.0,
        'similaridade_media_nao_outliers': np.mean(similaridades_por_grafo[~np.isin(np.arange(n_grafos), outliers)]) if len(outliers) < n_grafos else 0.0
    }
    
    return outliers, metricas_outliers

# Exemplo de uso
if __name__ == "__main__":
    import random
    
    # Exemplo: gera 10 grafos aleatórios similares
    grafos_simples = []
    for i in range(10):
        # Gera grafos com parâmetros similares
        p = 0.3 + random.uniform(-0.05, 0.05)  # Pequena variação
        G = nx.erdos_renyi_graph(20, p)
        grafos_simples.append(G)
    
    # Analisa equivalência entre replicações
    metricas = analisar_equivalencia_replicacoes(grafos_simples)
    
    print("Métricas de Equivalência entre Replicações:")
    for chave, valor in metricas.items():
        print(f"{chave}: {valor}")
    
    # Detecta outliers
    outliers, metricas_outliers = detectar_outliers_estruturais(grafos_simples)
    print(f"\nOutliers detectados: {outliers}")
    print(f"Métricas dos outliers: {metricas_outliers}")
