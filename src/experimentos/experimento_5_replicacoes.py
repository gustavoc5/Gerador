#!/usr/bin/env python3
"""
EXPERIMENTO 5: REPLICAÇÕES COM ANÁLISE ESTATÍSTICA
Gera múltiplas replicações para cada conjunto de parâmetros, salvando cada grafo 
em arquivo separado e criando resumo com médias das métricas.

FATORES:
- Gerador: Simples, Power-Law
- Tipo de Grafo: Todos os tipos suportados
- Tamanho (numV): 100, 1000, 10000, 100000
- Número de Replicações: 5, 10, 20, 50
- Seed Base: 1000, 2000, 3000

VARIÁVEIS DE RESPOSTA:
Para cada replicação: Todas as métricas detalhadas
Para o resumo: Média, desvio padrão, mínimo, máximo de cada métrica
"""

import os
import sys
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simples.gerador import geraDataset
from simples.utils import criaMatrizAdjacencias, tipoGrafo
from powerlaw.pwl import geraGrafoPwl
from simples.constants import TIPOS_GRAFOS, TIPOS_VALIDOS
from powerlaw.constants import GAMMA_MIN, GAMMA_MAX

def calcula_metricas_detalhadas(matriz, tipo_grafo, tempo_geracao):
    """Calcula métricas detalhadas do grafo."""
    import networkx as nx
    
    # Converte matriz para NetworkX
    if tipo_grafo in [1, 21, 31]:  # Dirigidos
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    for i in range(len(matriz)):
        G.add_node(i)
        for j in range(len(matriz[i])):
            if matriz[i][j] > 0:
                G.add_edge(i, j)
    
    metricas = {}
    
    # Informações básicas
    metricas['num_vertices'] = G.number_of_nodes()
    metricas['num_arestas'] = G.number_of_edges()
    metricas['tipo_detectado'] = tipo_grafo
    metricas['tempo_geracao'] = tempo_geracao
    
    # Densidade
    if G.number_of_nodes() > 1:
        max_arestas = G.number_of_nodes() * (G.number_of_nodes() - 1)
        if not G.is_directed():
            max_arestas //= 2
        metricas['densidade'] = G.number_of_edges() / max_arestas
    else:
        metricas['densidade'] = 0.0
    
    # Grau médio, máximo, mínimo
    if G.number_of_nodes() > 0:
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
        metricas['grau_desvio'] = np.std(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = metricas['grau_desvio'] = 0
    
    # Componentes conexas
    if G.is_directed():
        metricas['num_componentes'] = nx.number_strongly_connected_components(G)
    else:
        metricas['num_componentes'] = nx.number_connected_components(G)
    
    # Métricas de centralidade
    try:
        pagerank = nx.pagerank(G, max_iter=100)
        metricas['pagerank_medio'] = np.mean(list(pagerank.values()))
        metricas['pagerank_max'] = max(pagerank.values())
        metricas['pagerank_min'] = min(pagerank.values())
        metricas['pagerank_desvio'] = np.std(list(pagerank.values()))
    except:
        metricas['pagerank_medio'] = metricas['pagerank_max'] = metricas['pagerank_min'] = metricas['pagerank_desvio'] = 0.0
    
    try:
        closeness = nx.closeness_centrality(G)
        metricas['closeness_medio'] = np.mean(list(closeness.values()))
        metricas['closeness_max'] = max(closeness.values())
        metricas['closeness_min'] = min(closeness.values())
        metricas['closeness_desvio'] = np.std(list(closeness.values()))
    except:
        metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = metricas['closeness_desvio'] = 0.0
    
    try:
        betweenness = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        metricas['betweenness_medio'] = np.mean(list(betweenness.values()))
        metricas['betweenness_max'] = max(betweenness.values())
        metricas['betweenness_min'] = min(betweenness.values())
        metricas['betweenness_desvio'] = np.std(list(betweenness.values()))
    except:
        metricas['betweenness_medio'] = metricas['betweenness_max'] = metricas['betweenness_min'] = metricas['betweenness_desvio'] = 0.0
    
    # Métricas de distância
    try:
        if G.is_connected() or (G.is_directed() and nx.is_strongly_connected(G)):
            metricas['diametro'] = nx.diameter(G)
            metricas['raio'] = nx.radius(G)
            metricas['distancia_media'] = nx.average_shortest_path_length(G)
        else:
            metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    except:
        metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    
    # Métricas de comunidades
    try:
        # Greedy modularity
        comunidades_greedy = nx.community.greedy_modularity_communities(G.to_undirected())
        metricas['num_comunidades_greedy'] = len(comunidades_greedy)
        metricas['modularidade_greedy'] = nx.community.modularity(G.to_undirected(), comunidades_greedy)
    except:
        metricas['num_comunidades_greedy'] = 1
        metricas['modularidade_greedy'] = 0.0
    
    try:
        # Label propagation
        comunidades_label = nx.community.label_propagation_communities(G.to_undirected())
        metricas['num_comunidades_label'] = len(comunidades_label)
        metricas['modularidade_label'] = nx.community.modularity(G.to_undirected(), comunidades_label)
    except:
        metricas['num_comunidades_label'] = 1
        metricas['modularidade_label'] = 0.0
    
    # Conectividade
    if G.is_directed():
        metricas['conectividade'] = 1.0 if nx.is_strongly_connected(G) else 0.0
    else:
        metricas['conectividade'] = 1.0 if nx.is_connected(G) else 0.0
    
    return metricas

def executa_teste_simples(tipo, numV, numA, seed, num_replicacao):
    """Executa teste do gerador simples."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        resultado = geraDataset(tipo, numV, numA, seed=seed)
        
        if not resultado or 'matriz' not in resultado:
            return None
        
        tempo_geracao = time.time() - start_time
        
        # Calcula métricas
        metricas = calcula_metricas_detalhadas(resultado['matriz'], tipo, tempo_geracao)
        
        # Adiciona informações do teste
        metricas.update({
            'gerador': 'Simples',
            'tipo_grafo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'num_replicacao': num_replicacao,
            'sucesso': True
        })
        
        return metricas, resultado['matriz']
        
    except Exception as e:
        return None

def executa_teste_powerlaw(tipo, numV, gamma, seed, num_replicacao):
    """Executa teste do gerador power-law."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        resultado = geraGrafoPwl(tipo, numV, gamma, seed=seed)
        
        if not resultado or 'matriz' not in resultado:
            return None
        
        tempo_geracao = time.time() - start_time
        
        # Calcula métricas
        metricas = calcula_metricas_detalhadas(resultado['matriz'], tipo, tempo_geracao)
        
        # Adiciona métricas específicas do power-law
        try:
            import powerlaw
            graus = [d for n, d in resultado['grafo'].degree()]
            fit = powerlaw.Fit(graus, xmin=2)
            metricas['qualidade_powerlaw_R'] = fit.R
            metricas['qualidade_powerlaw_p_value'] = fit.p
        except:
            metricas['qualidade_powerlaw_R'] = 0.0
            metricas['qualidade_powerlaw_p_value'] = 1.0
        
        # Adiciona informações do teste
        metricas.update({
            'gerador': 'Power-Law',
            'tipo_grafo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'num_replicacao': num_replicacao,
            'sucesso': True
        })
        
        return metricas, resultado['matriz']
        
    except Exception as e:
        return None

def salva_grafo_individual(metricas, matriz, output_dir, config_id, num_replicacao):
    """Salva um grafo individual com suas métricas."""
    
    # Cria diretório para esta configuração
    config_dir = os.path.join(output_dir, f"config_{config_id}")
    os.makedirs(config_dir, exist_ok=True)
    
    # Nome do arquivo
    filename = f"replicacao_{num_replicacao:03d}.json"
    filepath = os.path.join(config_dir, filename)
    
    # Prepara dados para salvar
    dados_grafo = {
        'metadata': {
            'gerador': metricas['gerador'],
            'tipo_grafo': metricas['tipo_grafo'],
            'numV': metricas['numV'],
            'seed': metricas['seed'],
            'num_replicacao': num_replicacao,
            'timestamp': datetime.now().isoformat()
        },
        'parametros': {
            'numV': metricas['numV'],
            'seed': metricas['seed']
        },
        'metricas': metricas,
        'matriz': matriz.tolist() if hasattr(matriz, 'tolist') else matriz
    }
    
    # Adiciona parâmetros específicos
    if metricas['gerador'] == 'Simples':
        dados_grafo['parametros']['numA'] = metricas['numA']
    else:  # Power-Law
        dados_grafo['parametros']['gamma'] = metricas['gamma']
    
    # Salva arquivo JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dados_grafo, f, indent=2, ensure_ascii=False)
    
    return filepath

def calcula_estatisticas_replicacoes(replicacoes):
    """Calcula estatísticas das replicações."""
    if not replicacoes:
        return {}
    
    # Converte para DataFrame
    df = pd.DataFrame(replicacoes)
    
    # Métricas numéricas para calcular estatísticas
    metricas_numericas = [
        'tempo_geracao', 'num_vertices', 'num_arestas', 'densidade',
        'grau_medio', 'grau_max', 'grau_min', 'grau_desvio',
        'num_componentes', 'pagerank_medio', 'pagerank_max', 'pagerank_min', 'pagerank_desvio',
        'closeness_medio', 'closeness_max', 'closeness_min', 'closeness_desvio',
        'betweenness_medio', 'betweenness_max', 'betweenness_min', 'betweenness_desvio',
        'num_comunidades_greedy', 'modularidade_greedy',
        'num_comunidades_label', 'modularidade_label', 'conectividade'
    ]
    
    # Adiciona métricas específicas do power-law se aplicável
    if 'gamma' in df.columns:
        metricas_numericas.extend(['qualidade_powerlaw_R', 'qualidade_powerlaw_p_value'])
    
    estatisticas = {}
    
    for metrica in metricas_numericas:
        if metrica in df.columns:
            valores = df[metrica].dropna()
            if len(valores) > 0:
                estatisticas[f"{metrica}_media"] = valores.mean()
                estatisticas[f"{metrica}_desvio"] = valores.std()
                estatisticas[f"{metrica}_min"] = valores.min()
                estatisticas[f"{metrica}_max"] = valores.max()
                estatisticas[f"{metrica}_mediana"] = valores.median()
    
    # Estatísticas gerais
    estatisticas['num_replicacoes_sucesso'] = len(replicacoes)
    estatisticas['taxa_sucesso'] = len(replicacoes) / len(replicacoes)  # Sempre 1.0 se chegou aqui
    
    return estatisticas

def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento 5: Replicações com análise estatística')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp5_replicacoes',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000],
                       help='Lista de seeds base')
    parser.add_argument('--replicacoes', nargs='+', type=int, default=[5, 10, 20],
                       help='Número de replicações por configuração')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa versão rápida do experimento')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    GERADORES = ['Simples', 'Power-Law']
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]  # Todos os tipos
    
    if args.teste_rapido:
        TAMANHOS = [100, 1000]
        REPLICACOES = [5, 10]
        SEEDS = [1000, 2000]
    else:
        TAMANHOS = [100, 1000, 10000]
        if args.max_vertices >= 100000:
            TAMANHOS.append(100000)
        REPLICACOES = args.replicacoes
        SEEDS = args.seeds
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO 5: REPLICAÇÕES COM ANÁLISE ESTATÍSTICA")
    print("=" * 80)
    print(f"Geradores: {GERADORES}")
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Replicações: {REPLICACOES}")
    print(f"Seeds base: {SEEDS}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    # Lista para armazenar todos os resultados
    todos_resultados = []
    config_id = 0
    
    start_time_experimento = time.time()
    
    for gerador in GERADORES:
        for tipo in TIPOS_GRAFOS:
            for numV in TAMANHOS:
                for num_replicacoes in REPLICACOES:
                    for seed_base in SEEDS:
                        config_id += 1
                        
                        print(f"\n🔬 Configuração {config_id}: {gerador} - Tipo {tipo} - V={numV} - {num_replicacoes} replicações - Seed={seed_base}")
                        
                        replicacoes_config = []
                        
                        for rep in range(1, num_replicacoes + 1):
                            # Gera seed única para cada replicação
                            seed = seed_base + rep * 1000
                            
                            print(f"  📊 Replicação {rep:2d}/{num_replicacoes} (Seed={seed})", end=" ")
                            
                            if gerador == 'Simples':
                                # Calcula número de arestas para simples
                                max_arestas = numV * (numV - 1) // 2
                                numA = random.randint(max(1, numV-1), max_arestas)
                                resultado = executa_teste_simples(tipo, numV, numA, seed, rep)
                            else:  # Power-Law
                                # Gamma fixo para comparação
                                gamma = 2.5
                                resultado = executa_teste_powerlaw(tipo, numV, gamma, seed, rep)
                            
                            if resultado:
                                metricas, matriz = resultado
                                replicacoes_config.append(metricas)
                                
                                # Salva grafo individual
                                arquivo_salvo = salva_grafo_individual(metricas, matriz, args.output_dir, config_id, rep)
                                print(f"✅ Salvo: {os.path.basename(arquivo_salvo)}")
                            else:
                                print("❌ Falha")
                        
                        # Calcula estatísticas das replicações
                        if replicacoes_config:
                            estatisticas = calcula_estatisticas_replicacoes(replicacoes_config)
                            
                            # Adiciona informações da configuração
                            estatisticas.update({
                                'config_id': config_id,
                                'gerador': gerador,
                                'tipo_grafo': tipo,
                                'numV': numV,
                                'num_replicacoes': num_replicacoes,
                                'seed_base': seed_base
                            })
                            
                            # Adiciona parâmetros específicos
                            if gerador == 'Simples':
                                estatisticas['numA'] = replicacoes_config[0]['numA']
                            else:  # Power-Law
                                estatisticas['gamma'] = replicacoes_config[0]['gamma']
                            
                            todos_resultados.append(estatisticas)
                            
                            # Salva resumo da configuração
                            resumo_config_file = os.path.join(args.output_dir, f"config_{config_id}", "resumo_config.json")
                            with open(resumo_config_file, 'w', encoding='utf-8') as f:
                                json.dump(estatisticas, f, indent=2, ensure_ascii=False)
                            
                            print(f"  📋 Resumo salvo: {os.path.basename(resumo_config_file)}")
    
    end_time_experimento = time.time()
    tempo_total = end_time_experimento - start_time_experimento
    
    # Salva resumo geral
    if todos_resultados:
        # DataFrame com todos os resumos
        df_resumos = pd.DataFrame(todos_resultados)
        
        # Arquivo CSV com resumos
        csv_file = os.path.join(args.output_dir, 'resumos_todas_configuracoes.csv')
        df_resumos.to_csv(csv_file, index=False)
        
        # Arquivo de resumo geral
        resumo_geral_file = os.path.join(args.output_dir, 'resumo_geral_experimento5.txt')
        with open(resumo_geral_file, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 5: REPLICAÇÕES COM ANÁLISE ESTATÍSTICA\n")
            f.write("=" * 60 + "\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de configurações: {len(todos_resultados)}\n")
            f.write(f"Tempo total: {tempo_total:.2f} segundos\n\n")
            
            # Estatísticas por gerador
            for gerador in GERADORES:
                df_gerador = df_resumos[df_resumos['gerador'] == gerador]
                f.write(f"GERADOR: {gerador}\n")
                f.write(f"  Configurações: {len(df_gerador)}\n")
                f.write(f"  Tempo médio por configuração: {df_gerador['tempo_geracao_media'].mean():.3f}s\n")
                f.write(f"  Densidade média: {df_gerador['densidade_media'].mean():.4f}\n")
                f.write(f"  Grau médio: {df_gerador['grau_medio_media'].mean():.2f}\n\n")
            
            # Estatísticas por número de replicações
            for num_rep in REPLICACOES:
                df_rep = df_resumos[df_resumos['num_replicacoes'] == num_rep]
                f.write(f"REPLICAÇÕES: {num_rep}\n")
                f.write(f"  Configurações: {len(df_rep)}\n")
                f.write(f"  Tempo médio por configuração: {df_rep['tempo_geracao_media'].mean():.3f}s\n\n")
        
        print("\n" + "=" * 80)
        print("✅ EXPERIMENTO 5 CONCLUÍDO!")
        print(f"📊 Resumos salvos em: {csv_file}")
        print(f"📋 Resumo geral salvo em: {resumo_geral_file}")
        print(f"📁 Grafos individuais salvos em: {args.output_dir}/config_*/")
        print(f"⏱️  Tempo total: {tempo_total:.2f} segundos")
        print(f"🎯 Total de configurações: {len(todos_resultados)}")
        print("=" * 80)
    else:
        print("❌ Nenhum resultado válido foi gerado!")

if __name__ == "__main__":
    main()
