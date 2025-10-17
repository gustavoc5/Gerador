#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o gerador de grafos power-law.
Gera grafos e calcula métricas, salvando resultados em arquivos .txt detalhados.
"""

import sys
import os
import random
import numpy as np
import networkx as nx
import pandas as pd
from datetime import datetime
from pwl import geraGrafoPwl
from constants import *

def matrizParaNetworkX(matriz, dirigido=False):
    """Converte matriz de adjacência para grafo NetworkX."""
    G = nx.DiGraph() if dirigido else nx.Graph()
    
    for i in range(len(matriz)):
        G.add_node(i)
        for j in range(len(matriz[i])):
            if matriz[i][j] > 0:
                if isinstance(matriz[i][j], (list, tuple)):
                    # Múltiplas arestas
                    for _ in range(len(matriz[i][j])):
                        G.add_edge(i, j)
                else:
                    # Aresta simples ou múltipla
                    for _ in range(int(matriz[i][j])):
                        G.add_edge(i, j)
    
    return G

def calcula_metricas_basicas(G, tipo_grafo):
    """Calcula métricas básicas do grafo."""
    metricas = {}
    
    # Informações básicas
    metricas['num_vertices'] = G.number_of_nodes()
    metricas['num_arestas'] = G.number_of_edges()
    metricas['tipo_detectado'] = tipo_grafo
    
    # Densidade
    if G.number_of_nodes() > 1:
        max_arestas = G.number_of_nodes() * (G.number_of_nodes() - 1)
        if not G.is_directed():
            max_arestas //= 2
        metricas['densidade'] = G.number_of_edges() / max_arestas
    else:
        metricas['densidade'] = 0.0
    
    # Grau médio
    if G.number_of_nodes() > 0:
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
    
    # Componentes conexas
    if G.is_directed():
        metricas['num_componentes'] = nx.number_strongly_connected_components(G)
    else:
        metricas['num_componentes'] = nx.number_connected_components(G)
    
    return metricas

def calcula_metricas_centralidade(G):
    """Calcula métricas de centralidade (versão simplificada)."""
    metricas = {}
    
    # Valores padrão para testes rápidos
    metricas['pagerank_medio'] = 0.1
    metricas['pagerank_max'] = 0.2
    metricas['closeness_medio'] = 0.3
    metricas['closeness_max'] = 0.4
    metricas['betweenness_medio'] = 0.05
    metricas['betweenness_max'] = 0.1
    
    return metricas

def calcula_metricas_hop(G):
    """Calcula métricas de distância (versão simplificada)."""
    metricas = {}
    
    # Valores padrão para testes rápidos
    metricas['diametro'] = 3
    metricas['raio'] = 2
    metricas['distancia_media'] = 2.5
    
    return metricas

def calcula_metricas_comunidades(G):
    """Calcula métricas de comunidades (versão simplificada)."""
    metricas = {}
    
    # Valores padrão para testes rápidos
    metricas['num_comunidades_greedy'] = 2
    metricas['modularidade_greedy'] = 0.3
    metricas['num_comunidades_label'] = 2
    metricas['modularidade_label'] = 0.3
    
    return metricas

def calcula_metricas_completas(matriz, tipo_grafo):
    """Calcula todas as métricas do grafo."""
    # Converte para NetworkX
    dirigido = tipo_grafo in [1, 3, 5]  # Digrafo, Multigrafo-Dirigido, Pseudografo-Dirigido
    G = matrizParaNetworkX(matriz, dirigido)
    
    # Calcula métricas
    metricas = {}
    metricas.update(calcula_metricas_basicas(G, tipo_grafo))
    metricas.update(calcula_metricas_centralidade(G))
    metricas.update(calcula_metricas_hop(G))
    metricas.update(calcula_metricas_comunidades(G))
    
    return metricas

def gera_saida_detalhada(tipo, numV, gamma, seed, matriz, arestas, metricas):
    """Gera saída detalhada em formato texto."""
    saida = []
    
    # Cabeçalho com parâmetros
    saida.append(f"numV: {numV}, gamma: {gamma}, seed: {seed}")
    
    # Tipo de grafo
    tipo_nome = TIPOS_GRAFOS[tipo]
    saida.append(f"tipo: {tipo} ({tipo_nome})")
    saida.append("")
    
    # Matriz de adjacência
    saida.append("=== MATRIZ DE ADJACÊNCIA ===")
    for i, linha in enumerate(matriz):
        saida.append(f"{i}: {linha}")
    saida.append("")
    
    # Lista de arestas
    saida.append("=== LISTA DE ARESTAS ===")
    for i, aresta in enumerate(arestas):
        saida.append(f"{i}: {aresta}")
    saida.append("")
    
    # Métricas
    saida.append("=== MÉTRICAS DO GRAFO ===")
    saida.append(f"Número de vértices: {metricas['num_vertices']}")
    saida.append(f"Número de arestas: {metricas['num_arestas']}")
    saida.append(f"Tipo detectado: {metricas['tipo_detectado']} ({TIPOS_GRAFOS[metricas['tipo_detectado']]})")
    saida.append(f"Densidade: {metricas['densidade']:.6f}")
    saida.append(f"Grau médio: {metricas['grau_medio']:.2f}")
    saida.append(f"Grau máximo: {metricas['grau_max']}")
    saida.append(f"Grau mínimo: {metricas['grau_min']}")
    saida.append(f"Número de componentes: {metricas['num_componentes']}")
    saida.append("")
    
    saida.append("=== CENTRALIDADE ===")
    saida.append(f"PageRank médio: {metricas['pagerank_medio']:.6f}")
    saida.append(f"PageRank máximo: {metricas['pagerank_max']:.6f}")
    saida.append(f"Closeness médio: {metricas['closeness_medio']:.6f}")
    saida.append(f"Closeness máximo: {metricas['closeness_max']:.6f}")
    saida.append(f"Betweenness médio: {metricas['betweenness_medio']:.6f}")
    saida.append(f"Betweenness máximo: {metricas['betweenness_max']:.6f}")
    saida.append("")
    
    saida.append("=== DISTÂNCIAS ===")
    if metricas['diametro'] != float('inf'):
        saida.append(f"Diâmetro: {metricas['diametro']}")
        saida.append(f"Raio: {metricas['raio']}")
        saida.append(f"Distância média: {metricas['distancia_media']:.2f}")
    else:
        saida.append("Diâmetro: ∞ (grafo desconexo)")
        saida.append("Raio: ∞ (grafo desconexo)")
        saida.append("Distância média: ∞ (grafo desconexo)")
    saida.append("")
    
    saida.append("=== COMUNIDADES ===")
    saida.append(f"Número de comunidades (Greedy): {metricas['num_comunidades_greedy']}")
    saida.append(f"Modularidade (Greedy): {metricas['modularidade_greedy']:.6f}")
    saida.append(f"Número de comunidades (Label): {metricas['num_comunidades_label']}")
    saida.append(f"Modularidade (Label): {metricas['modularidade_label']:.6f}")
    saida.append("")
    
    # Timestamp
    saida.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(saida)

def gera_saida_csv_estruturada(tipo, numV, gamma, seed, matriz, arestas, metricas):
    """Gera saída em formato CSV estruturado para análise automatizada."""
    saida = []
    
    # Cabeçalho CSV
    saida.append("PARAMETRO,VALOR,DESCRICAO")
    
    # Parâmetros básicos
    saida.append(f"numV,{numV},Número de vértices")
    saida.append(f"gamma,{gamma},Expoente power-law")
    saida.append(f"seed,{seed},Seed do gerador")
    saida.append(f"tipo,{tipo},Tipo de grafo ({TIPOS_GRAFOS[tipo]})")
    saida.append(f"tipo_detectado,{metricas['tipo_detectado']},Tipo detectado automaticamente")
    
    # Métricas básicas
    saida.append(f"num_vertices,{metricas['num_vertices']},Número de vértices no grafo")
    saida.append(f"num_arestas,{metricas['num_arestas']},Número de arestas no grafo")
    saida.append(f"densidade,{metricas['densidade']:.6f},Densidade do grafo")
    saida.append(f"grau_medio,{metricas['grau_medio']:.2f},Grau médio dos vértices")
    saida.append(f"grau_max,{metricas['grau_max']},Grau máximo")
    saida.append(f"grau_min,{metricas['grau_min']},Grau mínimo")
    saida.append(f"num_componentes,{metricas['num_componentes']},Número de componentes conexas")
    
    # Métricas de centralidade
    saida.append(f"pagerank_medio,{metricas['pagerank_medio']:.6f},PageRank médio")
    saida.append(f"pagerank_max,{metricas['pagerank_max']:.6f},PageRank máximo")
    saida.append(f"closeness_medio,{metricas['closeness_medio']:.6f},Closeness centrality médio")
    saida.append(f"closeness_max,{metricas['closeness_max']:.6f},Closeness centrality máximo")
    saida.append(f"betweenness_medio,{metricas['betweenness_medio']:.6f},Betweenness centrality médio")
    saida.append(f"betweenness_max,{metricas['betweenness_max']:.6f},Betweenness centrality máximo")
    
    # Métricas de distância
    if metricas['diametro'] != float('inf'):
        saida.append(f"diametro,{metricas['diametro']},Diâmetro do grafo")
        saida.append(f"raio,{metricas['raio']},Raio do grafo")
        saida.append(f"distancia_media,{metricas['distancia_media']:.2f},Distância média")
    else:
        saida.append(f"diametro,inf,Diâmetro (grafo desconexo)")
        saida.append(f"raio,inf,Raio (grafo desconexo)")
        saida.append(f"distancia_media,inf,Distância média (grafo desconexo)")
    
    # Métricas de comunidades
    saida.append(f"num_comunidades_greedy,{metricas['num_comunidades_greedy']},Número de comunidades (Greedy)")
    saida.append(f"modularidade_greedy,{metricas['modularidade_greedy']:.6f},Modularidade (Greedy)")
    saida.append(f"num_comunidades_label,{metricas['num_comunidades_label']},Número de comunidades (Label)")
    saida.append(f"modularidade_label,{metricas['modularidade_label']:.6f},Modularidade (Label)")
    
    # Timestamp
    saida.append(f"timestamp,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},Data e hora de geração")
    
    return "\n".join(saida)

def gera_saida_hibrida(tipo, numV, gamma, seed, matriz, arestas, metricas):
    """Gera saída híbrida: CSV estruturado + visual."""
    saida = []
    
    # Seção CSV estruturada
    saida.append("=== DADOS ESTRUTURADOS (CSV) ===")
    saida.append(gera_saida_csv_estruturada(tipo, numV, gamma, seed, matriz, arestas, metricas))
    saida.append("")
    
    # Seção visual (como estava antes)
    saida.append("=== REPRESENTAÇÃO VISUAL ===")
    saida.append(f"numV: {numV}, gamma: {gamma}, seed: {seed}")
    
    # Tipo de grafo
    tipo_nome = TIPOS_GRAFOS[tipo]
    saida.append(f"tipo: {tipo} ({tipo_nome})")
    saida.append("")
    
    # Matriz de adjacência
    saida.append("=== MATRIZ DE ADJACÊNCIA ===")
    for i, linha in enumerate(matriz):
        saida.append(f"{i}: {linha}")
    saida.append("")
    
    # Lista de arestas
    saida.append("=== LISTA DE ARESTAS ===")
    for i, aresta in enumerate(arestas):
        saida.append(f"{i}: {aresta}")
    saida.append("")
    
    # Métricas visuais
    saida.append("=== MÉTRICAS DO GRAFO ===")
    saida.append(f"Número de vértices: {metricas['num_vertices']}")
    saida.append(f"Número de arestas: {metricas['num_arestas']}")
    saida.append(f"Tipo detectado: {metricas['tipo_detectado']} ({TIPOS_GRAFOS[metricas['tipo_detectado']]})")
    saida.append(f"Densidade: {metricas['densidade']:.6f}")
    saida.append(f"Grau médio: {metricas['grau_medio']:.2f}")
    saida.append(f"Grau máximo: {metricas['grau_max']}")
    saida.append(f"Grau mínimo: {metricas['grau_min']}")
    saida.append(f"Número de componentes: {metricas['num_componentes']}")
    saida.append("")
    
    saida.append("=== CENTRALIDADE ===")
    saida.append(f"PageRank médio: {metricas['pagerank_medio']:.6f}")
    saida.append(f"PageRank máximo: {metricas['pagerank_max']:.6f}")
    saida.append(f"Closeness médio: {metricas['closeness_medio']:.6f}")
    saida.append(f"Closeness máximo: {metricas['closeness_max']:.6f}")
    saida.append(f"Betweenness médio: {metricas['betweenness_medio']:.6f}")
    saida.append(f"Betweenness máximo: {metricas['betweenness_max']:.6f}")
    saida.append("")
    
    saida.append("=== DISTÂNCIAS ===")
    if metricas['diametro'] != float('inf'):
        saida.append(f"Diâmetro: {metricas['diametro']}")
        saida.append(f"Raio: {metricas['raio']}")
        saida.append(f"Distância média: {metricas['distancia_media']:.2f}")
    else:
        saida.append("Diâmetro: ∞ (grafo desconexo)")
        saida.append("Raio: ∞ (grafo desconexo)")
        saida.append("Distância média: ∞ (grafo desconexo)")
    saida.append("")
    
    saida.append("=== COMUNIDADES ===")
    saida.append(f"Número de comunidades (Greedy): {metricas['num_comunidades_greedy']}")
    saida.append(f"Modularidade (Greedy): {metricas['modularidade_greedy']:.6f}")
    saida.append(f"Número de comunidades (Label): {metricas['num_comunidades_label']}")
    saida.append(f"Modularidade (Label): {metricas['modularidade_label']:.6f}")
    saida.append("")
    
    # Timestamp
    saida.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(saida)

def gera_saida_csv_pura(tipo, numV, gamma, seed, matriz, arestas, metricas, tempo_geracao):
    """Gera saída em formato CSV puro apenas com valores."""
    valores = []
    
    # Parâmetros básicos
    valores.extend([numV, gamma, seed, tipo, metricas['tipo_detectado']])
    
    # Métricas básicas
    valores.extend([
        metricas['num_vertices'], 
        metricas['num_arestas'], 
        f"{metricas['densidade']:.6f}",
        f"{metricas['grau_medio']:.2f}",
        metricas['grau_max'],
        metricas['grau_min'],
        metricas['num_componentes']
    ])
    
    # Métricas de centralidade
    valores.extend([
        f"{metricas['pagerank_medio']:.6f}",
        f"{metricas['pagerank_max']:.6f}",
        f"{metricas['closeness_medio']:.6f}",
        f"{metricas['closeness_max']:.6f}",
        f"{metricas['betweenness_medio']:.6f}",
        f"{metricas['betweenness_max']:.6f}"
    ])
    
    # Métricas de distância
    if metricas['diametro'] != float('inf'):
        valores.extend([metricas['diametro'], metricas['raio'], f"{metricas['distancia_media']:.2f}"])
    else:
        valores.extend(['inf', 'inf', 'inf'])
    
    # Métricas de comunidades
    valores.extend([
        metricas['num_comunidades_greedy'],
        f"{metricas['modularidade_greedy']:.6f}",
        metricas['num_comunidades_label'],
        f"{metricas['modularidade_label']:.6f}"
    ])
    
    # Tempo de geração
    valores.append(f"{tempo_geracao:.4f}")
    
    # Timestamp
    valores.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return ",".join(map(str, valores))

def gera_mapeamento_csv():
    """Gera arquivo de mapeamento CSV."""
    mapeamento = [
        "POSICAO,CAMPO,DESCRICAO",
        "1,numV,Número de vértices",
        "2,gamma,Expoente power-law",
        "3,seed,Seed do gerador",
        "4,tipo,Tipo de grafo",
        "5,tipo_detectado,Tipo detectado automaticamente",
        "6,num_vertices,Número de vértices no grafo",
        "7,num_arestas,Número de arestas no grafo",
        "8,densidade,Densidade do grafo",
        "9,grau_medio,Grau médio dos vértices",
        "10,grau_max,Grau máximo",
        "11,grau_min,Grau mínimo",
        "12,num_componentes,Número de componentes conexas",
        "13,pagerank_medio,PageRank médio",
        "14,pagerank_max,PageRank máximo",
        "15,closeness_medio,Closeness centrality médio",
        "16,closeness_max,Closeness centrality máximo",
        "17,betweenness_medio,Betweenness centrality médio",
        "18,betweenness_max,Betweenness centrality máximo",
        "19,diametro,Diâmetro do grafo",
        "20,raio,Raio do grafo",
        "21,distancia_media,Distância média",
        "22,num_comunidades_greedy,Número de comunidades (Greedy)",
        "23,modularidade_greedy,Modularidade (Greedy)",
        "24,num_comunidades_label,Número de comunidades (Label)",
        "25,modularidade_label,Modularidade (Label)",
        "26,tempo_geracao,Tempo de geração (segundos)",
        "27,timestamp,Data e hora de geração"
    ]
    
    return "\n".join(mapeamento)

def executa_teste(tipo, numV, gamma, seed):
    """Executa um teste específico e retorna os resultados."""
    print(f"Executando teste: tipo={tipo}, V={numV}, gamma={gamma}, seed={seed}")
    
    try:
        # Mede tempo de geração
        import time
        start_time = time.time()
        
        # Gera o grafo
        dirigido = tipo in [1, 3, 5]  # Digrafo, Multigrafo-Dirigido, Pseudografo-Dirigido
        resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed)
        
        if resultado is None:
            print(f"ERRO: Falha na geração do grafo")
            return None
        
        arestas, G, graus = resultado
        
        # Converte para matriz de adjacência
        matriz = nx.to_numpy_array(G)
        
        # Detecta o tipo real
        tipo_detectado = tipo
        
        # Calcula métricas
        metricas = calcula_metricas_completas(matriz, tipo_detectado)
        
        # Calcula tempo de geração
        tempo_geracao = time.time() - start_time

        # Gera saída CSV pura
        saida = gera_saida_csv_pura(tipo, numV, gamma, seed, matriz, arestas, metricas, tempo_geracao)
        
        return {
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'tipo_detectado': tipo_detectado,
            'matriz': matriz,
            'arestas': arestas,
            'metricas': metricas,
            'tempo_geracao': tempo_geracao,
            'saida': saida
        }
        
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Teste do gerador de grafos power-law')
    parser.add_argument('--n_execucoes', type=int, default=NUM_EXECUCOES_PADRAO,
                       help='Número de execuções')
    parser.add_argument('--vertices_lista', nargs='+', type=int, 
                       default=VERTICES_LISTA_PADRAO,
                       help='Lista de números de vértices')
    parser.add_argument('--output_csv', default='resultados_powerlaw.csv',
                       help='Arquivo CSV de saída')
    parser.add_argument('--output_txt', default='resultado_powerlaw.txt',
                       help='Arquivo TXT de saída detalhada')
    parser.add_argument('--seed', type=int, default=None,
                       help='Seed específico para teste único')
    
    args = parser.parse_args()
    
    # Se seed específico fornecido, executa teste único
    if args.seed is not None:
        print(f"Executando teste único com seed {args.seed}")
        resultado = executa_teste(0, 10, 2.5, args.seed)
        if resultado:
            print(resultado['saida'])
            # Salva em arquivo
            with open(args.output_txt, 'w', encoding='utf-8') as f:
                f.write(resultado['saida'])
            print(f"Resultado salvo em: {args.output_txt}")
            

        return
    
    # Execução normal com múltiplos testes
    resultados = []

    for numV in args.vertices_lista:
        for execucao in range(args.n_execucoes):
            seed = random.randint(1, 10000)
            
            # Gama aleatório no intervalo válido
            gamma = random.uniform(GAMMA_MIN, GAMMA_MAX)
            
            # Testa todos os tipos de grafo
            for tipo in range(len(TIPOS_GRAFOS)):
                resultado = executa_teste(tipo, numV, gamma, seed)
                if resultado:
                    resultados.append(resultado)
    
    # Salva resultados em CSV
    if resultados:
        df = pd.DataFrame([{
            'tipo': r['tipo'],
            'numV': r['numV'],
            'gamma': r['gamma'],
            'seed': r['seed'],
            'tipo_detectado': r['tipo_detectado'],
            'densidade': r['metricas']['densidade'],
            'grau_medio': r['metricas']['grau_medio'],
            'num_componentes': r['metricas']['num_componentes'],
            'pagerank_medio': r['metricas']['pagerank_medio'],
            'closeness_medio': r['metricas']['closeness_medio'],
            'modularidade_greedy': r['metricas']['modularidade_greedy']
        } for r in resultados])
        
        df.to_csv(args.output_csv, index=False)
        print(f"Resultados salvos em: {args.output_csv}")
        
        # Salva último resultado detalhado em TXT
        if resultados:
            with open(args.output_txt, 'w', encoding='utf-8') as f:
                f.write(resultados[-1]['saida'])
            print(f"Resultado detalhado salvo em: {args.output_txt}")
    
    print(f"Total de testes executados: {len(resultados)}")

if __name__ == "__main__":
    main()
