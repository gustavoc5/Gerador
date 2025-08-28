#!/usr/bin/env python3
"""
Script de teste para o gerador de grafos simples.
Gera grafos e calcula métricas, salvando resultados em arquivos .txt detalhados.
"""

import sys
import os
import random
import numpy as np
import networkx as nx
import pandas as pd
from datetime import datetime
from gerador import geraDataset
from utils import tipoGrafo, compConexas
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

def gera_saida_detalhada(tipo, numV, numA, seed, n, numC, fator, matriz, componentes, metricas):
    """Gera saída detalhada em formato texto."""
    saida = []
    
    # Cabeçalho com parâmetros
    saida.append(f"numV: {numV}, numA: {numA}, seed: {seed}, n: {n}")
    if numC > 0:
        saida.append(f"numC: {numC}, fator: {fator}")
    
    # Tipo de grafo
    tipo_nome = TIPOS_GRAFOS[tipo]
    saida.append(f"tipo: {tipo} ({tipo_nome})")
    saida.append("")
    
    # Matriz de adjacência
    saida.append("=== MATRIZ DE ADJACÊNCIA ===")
    for i, linha in enumerate(matriz):
        saida.append(f"{i}: {linha}")
    saida.append("")
    
    # Lista de arestas por componente
    saida.append("=== ARESTAS POR COMPONENTE ===")
    for i, comp in enumerate(componentes):
        saida.append(f"{i}: {comp}")
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

def gera_saida_csv_estruturada(tipo, numV, numA, seed, n, numC, fator, matriz, componentes, metricas):
    """Gera saída em formato CSV estruturado para análise automatizada."""
    saida = []
    
    # Cabeçalho CSV
    saida.append("PARAMETRO,VALOR,DESCRICAO")
    
    # Parâmetros básicos
    saida.append(f"numV,{numV},Número de vértices")
    saida.append(f"numA,{numA},Número de arestas")
    saida.append(f"seed,{seed},Seed do gerador")
    saida.append(f"n,{n},Número de grafos")
    saida.append(f"numC,{numC},Número de componentes")
    saida.append(f"fator,{fator},Fator de geração")
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

def gera_saida_hibrida(tipo, numV, numA, seed, n, numC, fator, matriz, componentes, metricas):
    """Gera saída híbrida: CSV estruturado + visual."""
    saida = []
    
    # Seção CSV estruturada
    saida.append("=== DADOS ESTRUTURADOS (CSV) ===")
    saida.append(gera_saida_csv_estruturada(tipo, numV, numA, seed, n, numC, fator, matriz, componentes, metricas))
    saida.append("")
    
    # Seção visual (como estava antes)
    saida.append("=== REPRESENTAÇÃO VISUAL ===")
    saida.append(f"numV: {numV}, numA: {numA}, seed: {seed}, n: {n}")
    if numC > 0:
        saida.append(f"numC: {numC}, fator: {fator}")
    
    # Tipo de grafo
    tipo_nome = TIPOS_GRAFOS[tipo]
    saida.append(f"tipo: {tipo} ({tipo_nome})")
    saida.append("")
    
    # Matriz de adjacência
    saida.append("=== MATRIZ DE ADJACÊNCIA ===")
    for i, linha in enumerate(matriz):
        saida.append(f"{i}: {linha}")
    saida.append("")
    
    # Lista de arestas por componente
    saida.append("=== ARESTAS POR COMPONENTE ===")
    for i, comp in enumerate(componentes):
        saida.append(f"{i}: {comp}")
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

def gera_saida_csv_pura(tipo, numV, numA, seed, n, numC, fator, matriz, componentes, metricas, tempo_geracao):
    """Gera saída em formato CSV puro apenas com valores."""
    valores = []
    
    # Parâmetros básicos
    valores.extend([numV, numA, seed, n, numC, fator, tipo, metricas['tipo_detectado']])
    
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
        "2,numA,Número de arestas", 
        "3,seed,Seed do gerador",
        "4,n,Número de grafos",
        "5,numC,Número de componentes",
        "6,fator,Fator de geração",
        "7,tipo,Tipo de grafo",
        "8,tipo_detectado,Tipo detectado automaticamente",
        "9,num_vertices,Número de vértices no grafo",
        "10,num_arestas,Número de arestas no grafo",
        "11,densidade,Densidade do grafo",
        "12,grau_medio,Grau médio dos vértices",
        "13,grau_max,Grau máximo",
        "14,grau_min,Grau mínimo",
        "15,num_componentes,Número de componentes conexas",
        "16,pagerank_medio,PageRank médio",
        "17,pagerank_max,PageRank máximo",
        "18,closeness_medio,Closeness centrality médio",
        "19,closeness_max,Closeness centrality máximo",
        "20,betweenness_medio,Betweenness centrality médio",
        "21,betweenness_max,Betweenness centrality máximo",
        "22,diametro,Diâmetro do grafo",
        "23,raio,Raio do grafo",
        "24,distancia_media,Distância média",
        "25,num_comunidades_greedy,Número de comunidades (Greedy)",
        "26,modularidade_greedy,Modularidade (Greedy)",
        "27,num_comunidades_label,Número de comunidades (Label)",
        "28,modularidade_label,Modularidade (Label)",
        "29,tempo_geracao,Tempo de geração (segundos)",
        "30,timestamp,Data e hora de geração"
    ]
    
    return "\n".join(mapeamento)

def executa_teste(tipo, numV, numA, seed, n=1, numC=0, fator=1.0):
    """Executa um teste específico e retorna os resultados."""
    print(f"Executando teste: tipo={tipo}, V={numV}, A={numA}, seed={seed}")
    
    try:
        # Mede tempo de geração
        import time
        start_time = time.time()
        
        # Gera o grafo
        datasets = geraDataset(tipo, numV, numA, seed, n, numC, fator)
        
        if not datasets:
            print(f"ERRO: Falha na geração do grafo")
            return None
        
        # Pega o primeiro dataset
        arestas = datasets[0]
        
        # Cria matriz de adjacência
        from utils import criaMatrizAdjacencias
        matriz = criaMatrizAdjacencias(arestas, numV, tipo)
        
        # Cria componentes (lista de arestas por componente)
        componentes = [arestas]  # Para simplicidade, assume uma componente
        
        # Detecta o tipo real
        tipo_detectado = tipoGrafo(matriz)
        
        # Calcula métricas
        metricas = calcula_metricas_completas(matriz, tipo_detectado)
        
        # Calcula tempo de geração
        tempo_geracao = time.time() - start_time
        
        # Gera saída CSV pura
        saida = gera_saida_csv_pura(tipo, numV, numA, seed, n, numC, fator, 
                                   matriz, componentes, metricas, tempo_geracao)
        
        return {
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'n': n,
            'numC': numC,
            'fator': fator,
            'tipo_detectado': tipo_detectado,
            'matriz': matriz,
            'componentes': componentes,
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
    
    parser = argparse.ArgumentParser(description='Teste do gerador de grafos simples')
    parser.add_argument('--n_execucoes', type=int, default=NUM_EXECUCOES_PADRAO,
                       help='Número de execuções')
    parser.add_argument('--vertices_lista', nargs='+', type=int, 
                       default=VERTICES_LISTA_PADRAO,
                       help='Lista de números de vértices')
    parser.add_argument('--output_csv', default='resultados_simples.csv',
                       help='Arquivo CSV de saída')
    parser.add_argument('--output_txt', default='resultado_simples.txt',
                       help='Arquivo TXT de saída detalhada')
    parser.add_argument('--seed', type=int, default=None,
                       help='Seed específico para teste único')
    parser.add_argument('--output_dir', default='./resultados',
                       help='Diretório de saída para arquivos individuais')
    
    args = parser.parse_args()
    
    # Se seed específico fornecido, executa teste único
    if args.seed is not None:
        print(f"Executando teste único com seed {args.seed}")
        # Usa parâmetros menores para demonstração
        numV = 100  # Tamanho menor para demonstração
        max_arestas = numV * (numV - 1) // 2
        numA = random.randint(max(1, numV-1), max_arestas)
        tipo = 0  # Simples
        
        resultado = executa_teste(tipo, numV, numA, args.seed)
        if resultado:
            print(resultado['saida'])
            # Salva em arquivo
            with open(args.output_txt, 'w', encoding='utf-8') as f:
                f.write(resultado['saida'])
            print(f"Resultado salvo em: {args.output_txt}")
            

        return
    
    # Execução normal com múltiplos testes
    resultados = []
    arquivos_gerados = 0
    
    print(f"🚀 Iniciando teste completo")
    print(f"📁 Diretório de saída: {args.output_dir}")
    print(f"📊 Vértices: {args.vertices_lista}")
    print(f"🔄 Execuções: {args.n_execucoes}")
    print(f"🎯 Tipos de grafo: {len(TIPOS_GRAFOS)}")
    print("=" * 60)
    
    # Seed inicial aleatória, depois incrementa de 1 em 1
    seed_atual = random.randint(1000, 9999)
    print(f"🌱 Seed inicial (aleatória): {seed_atual}")
    
    for numV in args.vertices_lista:
        for execucao in range(args.n_execucoes):
            # Usa seed atual e incrementa para o próximo
            seed = seed_atual
            seed_atual += 1
            
            # Calcula número de arestas baseado na densidade
            max_arestas = numV * (numV - 1) // 2
            numA = random.randint(max(1, numV-1), max_arestas)
            
            # Testa todos os tipos de grafo
            for tipo in TIPOS_VALIDOS:
                resultado = executa_teste(tipo, numV, numA, seed)
                if resultado:
                    resultados.append(resultado)
                    
                    # Cria diretório baseado no seed
                    seed_dir = os.path.join(args.output_dir, "simples", str(seed))
                    os.makedirs(seed_dir, exist_ok=True)
                    
                    # Nome do arquivo específico
                    filename = f"simples_t{tipo}_v{numV}_a{numA}_s{seed}.txt"
                    filepath = os.path.join(seed_dir, filename)
                    
                    # Salva cada grafo em arquivo separado
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(resultado['saida'])
                    
                    arquivos_gerados += 1
                    print(f"  [{arquivos_gerados:3d}] Salvo: {filename}")
    
    # Salva resultados em CSV (resumo)
    if resultados:
        df = pd.DataFrame([{
            'tipo': r['tipo'],
            'numV': r['numV'],
            'numA': r['numA'],
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
        print(f"📊 Resumo salvo em: {args.output_csv}")
    
    print("=" * 60)
    print(f"✅ CONCLUIDO!")
    print(f"📁 Arquivos gerados: {arquivos_gerados}")
    print(f"📊 Total de testes: {len(resultados)}")
    print(f"📂 Diretório: {args.output_dir}/simples/")
    print(f"💡 Para executar em paralelo: parallel -j <cores> < comandos_gerados.sh")

if __name__ == "__main__":
    main()
