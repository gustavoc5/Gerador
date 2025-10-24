#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPERIMENTO SIMPLES COMPLETO
Experimento unificado para o gerador Simples com todas as métricas possíveis.

FATORES:
- Tipo de Grafo: 0, 1, 20, 21, 30, 31 (6 tipos)
- Tamanho (numV): 100, 1000, 10000, 100000, 1000000
- Estratégia de Arestas: Proporcional, Aleatório
- Preferência de Densidade: 0 (Sem preferência), 1 (Esparso), 2 (Denso)
- Número de Componentes: 0, 1, 2, 5, 10
- Fator de Balanceamento: 0, 1, 2
- Seed: 1000, 2000, 3000, 4000, 5000
- Grafos: Sempre 10 grafos por configuração (valor fixo)

MÉTRICAS COLETADAS:
- Todas as métricas básicas, de centralidade, distância, comunidades
- Métricas de performance e memória
- Métricas específicas do gerador simples
- Médias de todas as métricas dos 10 grafos gerados
- Equivalência estrutural entre replicações
"""

import os
import sys
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime
import signal
# Parâmetros ajustáveis (podem ser alterados via CLI em main)
MID_THRESHOLD = 10000
LARGE_THRESHOLD = 100000
CLOSENESS_SAMPLE_FRAC = 0.02  # 2% dos nós
BETWEENNESS_K_FULL = 100
BETWEENNESS_K_MID = 50
PAGERANK_ITER_MID = 50
PAGERANK_ITER_LARGE = 30

# Adiciona o diretório src ao path
sys.path.append(os.path.dirname(__file__))

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    dependencias = {
        'numpy': 'NumPy',
        'networkx': 'NetworkX', 
        'scipy': 'SciPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn'
    }
    
    for modulo, nome in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            print(f"ERRO: {nome} não está instalado")
            print(f"Execute: pip install {modulo}")
            sys.exit(1)

# Importações diretas
import sys
import os
# Prioriza o diretório 'simples' no sys.path para permitir execução direta
simples_dir = os.path.join(os.path.dirname(__file__), '..', 'simples')
if simples_dir not in sys.path:
    sys.path.insert(0, simples_dir)

from gerador import geraDataset  # type: ignore[reportMissingImports]
from utils import criaMatrizAdjacencias, tipoGrafo  # type: ignore[reportMissingImports]
from constants import TIPOS_GRAFOS, TIPOS_VALIDOS, DENSIDADE_ESPARSA_MAX, DENSIDADE_DENSA_MIN  # type: ignore[reportMissingImports]



def calcula_metricas_completas_por_arestas(arestas, num_vertices_total, tipo_grafo, seed_metrics: int | None = None):
    """Calcula todas as métricas possíveis do grafo a partir da lista de arestas (sem matriz)."""
    import networkx as nx
    
    # Cria grafo a partir de arestas
    if tipo_grafo in [1, 21, 31]:  # Dirigidos
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    # Garante todos os nós existentes (0..numV-1)
    G.add_nodes_from(range(num_vertices_total))
    # Adiciona arestas
    G.add_edges_from(arestas)
    
    metricas = {}
    n = int(num_vertices_total)
    # Perfis por tamanho
    perfil_full = n <= MID_THRESHOLD
    perfil_mid = MID_THRESHOLD < n <= LARGE_THRESHOLD
    perfil_large = n > LARGE_THRESHOLD
    
    # ===== MÉTRICAS BÁSICAS =====
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
    
    # ===== MÉTRICAS DE GRAU =====
    if G.number_of_nodes() > 0:
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
        metricas['grau_desvio'] = np.std(graus)
        metricas['grau_mediana'] = np.median(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
        metricas['grau_desvio'] = metricas['grau_mediana'] = 0
    
    # ===== MÉTRICAS DE CONECTIVIDADE =====
    try:
        if G.is_directed():
            metricas['num_componentes'] = nx.number_strongly_connected_components(G)
            metricas['conectividade'] = 1.0 if nx.is_strongly_connected(G) else 0.0
        else:
            metricas['num_componentes'] = nx.number_connected_components(G)
            metricas['conectividade'] = 1.0 if nx.is_connected(G) else 0.0
    except:
        metricas['num_componentes'] = 1
        metricas['conectividade'] = 0.0
    
    # ===== MÉTRICAS DE CENTRALIDADE =====
    try:
        if perfil_large:
            # PageRank leve em grafos muito grandes
            try:
                from networkx.algorithms.link_analysis.pagerank_alg import pagerank_scipy as pr_scipy
                pagerank = pr_scipy(G, max_iter=PAGERANK_ITER_LARGE, tol=1e-4)
            except Exception:
                pagerank = nx.pagerank(G, max_iter=PAGERANK_ITER_LARGE, tol=1e-4)
        elif perfil_mid:
            pagerank = nx.pagerank(G, max_iter=PAGERANK_ITER_MID)
        else:
            pagerank = nx.pagerank(G, max_iter=100)
        metricas['pagerank_medio'] = np.mean(list(pagerank.values()))
        metricas['pagerank_max'] = max(pagerank.values())
        metricas['pagerank_min'] = min(pagerank.values())
        metricas['pagerank_desvio'] = np.std(list(pagerank.values()))
        metricas['pagerank_mediana'] = np.median(list(pagerank.values()))
    except Exception:
        metricas['pagerank_medio'] = metricas['pagerank_max'] = metricas['pagerank_min'] = 0.0
        metricas['pagerank_desvio'] = metricas['pagerank_mediana'] = 0.0
    
    if not perfil_large:
        try:
            if perfil_mid and n > 0:
                # Closeness por amostragem
                amostra = max(1, int(max(1, int(n * CLOSENESS_SAMPLE_FRAC))))
                import random as _rnd
                rnd = _rnd.Random(seed_metrics if seed_metrics is not None else 0)
                nodes = list(G.nodes())
                sample_nodes = rnd.sample(nodes, min(len(nodes), amostra))
                vals = []
                for u in sample_nodes:
                    dist = nx.single_source_shortest_path_length(G, u)
                    s = sum(dist.values())
                    reach = len(dist)
                    if s > 0.0 and n > 1:
                        vals.append((reach - 1) / s * ((reach - 1) / (n - 1)))
                if vals:
                    metricas['closeness_medio'] = float(np.mean(vals))
                    metricas['closeness_max'] = float(np.max(vals))
                    metricas['closeness_min'] = float(np.min(vals))
                    metricas['closeness_desvio'] = float(np.std(vals))
                    metricas['closeness_mediana'] = float(np.median(vals))
                else:
                    metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
                    metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
                metricas['closeness_amostrado'] = True
            else:
                closeness = nx.closeness_centrality(G)
                metricas['closeness_medio'] = np.mean(list(closeness.values()))
                metricas['closeness_max'] = max(closeness.values())
                metricas['closeness_min'] = min(closeness.values())
                metricas['closeness_desvio'] = np.std(list(closeness.values()))
                metricas['closeness_mediana'] = np.median(list(closeness.values()))
                metricas['closeness_amostrado'] = False
        except Exception:
            metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
            metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
    else:
        metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
        metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
    
    if not perfil_large:
        try:
            k_bt = min(BETWEENNESS_K_FULL, G.number_of_nodes()) if perfil_full else min(BETWEENNESS_K_MID, G.number_of_nodes())
            try:
                betweenness = nx.betweenness_centrality(G, k=k_bt, seed=seed_metrics)
            except TypeError:
                betweenness = nx.betweenness_centrality(G, k=k_bt)
            metricas['betweenness_medio'] = np.mean(list(betweenness.values()))
            metricas['betweenness_max'] = max(betweenness.values())
            metricas['betweenness_min'] = min(betweenness.values())
            metricas['betweenness_desvio'] = np.std(list(betweenness.values()))
            metricas['betweenness_mediana'] = np.median(list(betweenness.values()))
        except Exception:
            metricas['betweenness_medio'] = metricas['betweenness_max'] = metricas['betweenness_min'] = 0.0
            metricas['betweenness_desvio'] = metricas['betweenness_mediana'] = 0.0
    else:
        metricas['betweenness_medio'] = metricas['betweenness_max'] = metricas['betweenness_min'] = 0.0
        metricas['betweenness_desvio'] = metricas['betweenness_mediana'] = 0.0
    
    # ===== MÉTRICAS DE DISTÂNCIA =====
    if perfil_full:
        try:
            if G.is_connected() or (G.is_directed() and nx.is_strongly_connected(G)):
                metricas['diametro'] = nx.diameter(G)
                metricas['raio'] = nx.radius(G)
                metricas['distancia_media'] = nx.average_shortest_path_length(G)
            else:
                metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
        except Exception:
            metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    else:
        metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    
    # ===== MÉTRICAS DE COMUNIDADES =====
    if not perfil_large:
        try:
            G_und = G.to_undirected()
            communities_greedy = nx.community.greedy_modularity_communities(G_und)
            metricas['num_comunidades_greedy'] = len(communities_greedy)
            metricas['modularidade_greedy'] = nx.community.modularity(G_und, communities_greedy)
        except Exception:
            metricas['num_comunidades_greedy'] = 1
            metricas['modularidade_greedy'] = 0.0
        
        try:
            # Preferir versão assíncrona com seed
            try:
                communities_label = list(nx.community.asyn_lpa_communities(G_und, seed=seed_metrics))
            except Exception:
                communities_label = list(nx.community.label_propagation_communities(G_und))
            metricas['num_comunidades_label'] = len(communities_label)
            metricas['modularidade_label'] = nx.community.modularity(G_und, communities_label)
        except Exception:
            metricas['num_comunidades_label'] = 1
            metricas['modularidade_label'] = 0.0
    else:
        metricas['num_comunidades_greedy'] = 1
        metricas['modularidade_greedy'] = 0.0
        metricas['num_comunidades_label'] = 1
        metricas['modularidade_label'] = 0.0
    
    # ===== MÉTRICAS ESPECÍFICAS DO SIMPLES =====
    # Razão vértices/arestas
    metricas['razao_vertices_arestas'] = metricas['num_vertices'] / metricas['num_arestas'] if metricas['num_arestas'] > 0 else 0
    
    return metricas

def executa_teste_simples_completo(tipo, numV, numA, seed, estrategia_arestas, preferencia_densidade, numC, output_format='consolidated_csv', output_dir='./resultados', naming_pattern='metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv', num_grafos=50, timeout_por_grafo_s: int = 0):
    """Executa teste completo do gerador simples com 50 grafos."""
    try:
        
        # Analisa grafos (com suporte a timeout por grafo)
        todas_metricas = []
        grafos_networkx = []  # Lista para análise de equivalência estrutural

        def _timeout_handler(signum, frame):
            raise TimeoutError("Timeout por grafo atingido")

        for i in range(num_grafos):
            # Geração por réplica (permite timeout por grafo); usa seed variada
            item = None
            tempo_geracao_s = None
            try:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, _timeout_handler)
                    signal.alarm(int(timeout_por_grafo_s))
                # gera 1 grafo por vez, com seed offset
                item_list = geraDataset(tipo, numV, numA, seed + i, n=1, numC=numC, fator=0, medir_tempo=True)
                if item_list:
                    item = item_list[0]
                if isinstance(item, tuple):
                    arestas, tempo_geracao_s = item
                else:
                    arestas = item
                # Cancela alarme após geração
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
            except TimeoutError:
                # Cancela alarme e segue para próxima réplica
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                continue

            if item is None:
                continue

            if isinstance(item, tuple):
                arestas, tempo_geracao_s = item
            else:
                arestas = item
                tempo_geracao_s = None
            tipo_detectado = tipo  # evitamos reconstrução por matriz
            # Aplica timeout também no bloco de métricas, se configurado
            # Constrói G_nx para equivalência estrutural antes das métricas
            import networkx as nx
            G_nx = nx.DiGraph() if tipo in [1, 21, 31] else nx.Graph()
            G_nx.add_nodes_from(range(numV))
            G_nx.add_edges_from(arestas)
            grafos_networkx.append(G_nx)

            try:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, _timeout_handler)
                    signal.alarm(int(timeout_por_grafo_s))
                metricas_grafo = calcula_metricas_completas_por_arestas(arestas, numV, tipo_detectado, seed_metrics=(seed + i))
            except TimeoutError:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                # Calcula e registra métricas básicas mesmo com timeout
                try:
                    metricas_grafo = {}
                    metricas_grafo['num_vertices'] = G_nx.number_of_nodes()
                    metricas_grafo['num_arestas'] = G_nx.number_of_edges()
                    metricas_grafo['tipo_detectado'] = tipo_detectado
                    # Densidade
                    if G_nx.number_of_nodes() > 1:
                        max_arestas = G_nx.number_of_nodes() * (G_nx.number_of_nodes() - 1)
                        if not G_nx.is_directed():
                            max_arestas //= 2
                        metricas_grafo['densidade'] = G_nx.number_of_edges() / max_arestas
                    else:
                        metricas_grafo['densidade'] = 0.0
                    # Grau básicos
                    graus = [d for n, d in G_nx.degree()]
                    if graus:
                        metricas_grafo['grau_medio'] = float(np.mean(graus))
                        metricas_grafo['grau_max'] = int(max(graus))
                        metricas_grafo['grau_min'] = int(min(graus))
                        metricas_grafo['grau_desvio'] = float(np.std(graus))
                        metricas_grafo['grau_mediana'] = float(np.median(graus))
                    else:
                        metricas_grafo['grau_medio'] = metricas_grafo['grau_max'] = metricas_grafo['grau_min'] = 0
                        metricas_grafo['grau_desvio'] = metricas_grafo['grau_mediana'] = 0
                    metricas_grafo['razao_vertices_arestas'] = (
                        metricas_grafo['num_vertices'] / metricas_grafo['num_arestas']
                        if metricas_grafo['num_arestas'] > 0 else 0.0
                    )
                    metricas_grafo['metricas_incompletas'] = True
                except Exception:
                    continue
            finally:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
            
            # Adiciona parâmetros do teste às métricas
            metricas_grafo.update({
                'gerador': 'Simples',
                'tipo': tipo,
                'numV': numV,
                'numA': numA,
                'seed': seed,
                'estrategia_arestas': estrategia_arestas,
                'preferencia_densidade': preferencia_densidade,
                'numC': numC,
                'numero': i + 1,
                'tempo_geracao_s': tempo_geracao_s if tempo_geracao_s is not None else 0.0
            })
            
            # Se formato individual, salva arquivo CSV imediatamente
            if output_format == 'individual_csv':
                nome_arquivo = naming_pattern.format(
                    seed=seed,
                    tipo=tipo,
                    vertices=numV,
                    densidade=preferencia_densidade,
                    componentes=numC,
                    numero=i + 1
                )
                caminho_arquivo = os.path.join(output_dir, nome_arquivo)
                
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
                
                # Salva CSV individual
                df_individual = pd.DataFrame([metricas_grafo])
                df_individual.to_csv(caminho_arquivo, index=False)
                print(f"  [CSV] Salvo: {nome_arquivo}")
            
            todas_metricas.append(metricas_grafo)
            
            # (já incluído antes das métricas)
        
        # Calcula médias apenas para métricas numéricas
        def _is_numeric(value):
            return isinstance(value, (int, float, np.integer, np.floating)) and not (isinstance(value, float) and np.isnan(value))

        metricas_medias = {}
        for chave in todas_metricas[0].keys():
            valores_numericos = []
            for m in todas_metricas:
                v = m.get(chave)
                if _is_numeric(v):
                    valores_numericos.append(float(v))
            if valores_numericos:
                metricas_medias[chave] = float(np.mean(valores_numericos))

        # Agregados adicionais de tempo de geração (se existir a coluna)
        if 'tempo_geracao_s' in todas_metricas[0]:
            tempos = [float(m.get('tempo_geracao_s', 0.0)) for m in todas_metricas]
            if tempos:
                metricas_medias['tempo_geracao_medio_s'] = float(np.mean(tempos))
                metricas_medias['tempo_geracao_mediana_s'] = float(np.median(tempos))
        

        
        # Analisa equivalência estrutural entre replicações
        try:
            from similaridade import analisar_equivalencia_replicacoes, detectar_outliers_estruturais
            
            metricas_equivalencia = analisar_equivalencia_replicacoes(grafos_networkx)
            outliers, metricas_outliers = detectar_outliers_estruturais(grafos_networkx)
            
            # Adiciona métricas de equivalência estrutural
            metricas_medias.update(metricas_equivalencia)
            metricas_medias.update(metricas_outliers)
            metricas_medias['n_outliers_estruturais'] = len(outliers)
            metricas_medias['indices_outliers'] = str(outliers) if outliers else "[]"
        except Exception as e:
            # Se não conseguir calcular equivalência estrutural, usa valores padrão
            metricas_medias.update({
                'similaridade_media': 0.0,
                'consistencia_estrutural': 0.0,
                'n_outliers_estruturais': 0,
                'indices_outliers': "[]"
            })
        
        # Adiciona métricas básicas
        metricas_medias.update({
            'taxa_sucesso': len(todas_metricas) / num_grafos,
            'limite_atingido': False
        })
        
        # Adiciona parâmetros do teste
        metricas_medias.update({
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': num_grafos
        })
        
        return metricas_medias
        
    except MemoryError:
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': num_grafos,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': 'MemoryError'
        }
    except Exception as e:
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': num_grafos,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def main():
    """Função principal do experimento."""
    # Verificar dependências antes de continuar
    verificar_dependencias()
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento Simples Completo - Todas as métricas')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp_simples_completo',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste (padrão: 10000)')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                       help='Lista de seeds para teste (aceita seed única ou múltiplas)')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa versão reduzida para teste rápido')
    parser.add_argument('--output_format', 
                       choices=['consolidated_csv', 'individual_csv'], 
                       default='consolidated_csv',
                       help='Formato de saída: consolidated_csv (1 arquivo) ou individual_csv (1 arquivo por grafo)')
    parser.add_argument('--timeout_por_grafo_s', type=int, default=600,
                       help='Timeout por grafo (segundos). Padrão: 600 (10 minutos). Use 0 para desativar.')
    parser.add_argument('--naming_pattern', 
                       type=str,
                       default='metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv',
                       help='Padrão de nomeação para arquivos individuais')
    parser.add_argument('--num_grafos', type=int, default=50,
                       help='Número de grafos por combinação (padrão: 50)')
    parser.add_argument('--smoke', action='store_true',
                       help='Executa um smoke test mínimo (parâmetros reduzidos, poucos grafos)')
    parser.add_argument('--tipos', nargs='+', type=int, default=[0, 1, 20, 21, 30, 31],
                       help='Lista de tipos de grafos para teste (padrão: todos os tipos)')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    TIPOS_GRAFOS = args.tipos  # Tipos fornecidos pelo usuário
    
    if args.smoke:
        TAMANHOS = [100]
        PREFERENCIAS_DENSIDADE = [0]
        NUM_COMPONENTES = [0]
        SEEDS = args.seeds
        num_grafos_exec = min(args.num_grafos, 2)
    elif args.teste_rapido:
        TAMANHOS = [100, 1000]
        PREFERENCIAS_DENSIDADE = [0, 1, 2]  # Sem preferência, Esparso, Denso
        NUM_COMPONENTES = [0, 1]  # Aleatório, Conexo
        SEEDS = [1000, 2000]
        num_grafos_exec = args.num_grafos
    else:
        TAMANHOS = [100, 1000, 10000]
        if args.max_vertices >= 100000:
            TAMANHOS.append(100000)
        if args.max_vertices >= 1000000:
            TAMANHOS.append(1000000)
        PREFERENCIAS_DENSIDADE = [0, 1, 2]  # Sem preferência, Esparso, Denso
        NUM_COMPONENTES = [0, 1]  # Aleatório, Conexo
        SEEDS = args.seeds
        num_grafos_exec = args.num_grafos
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO SIMPLES COMPLETO - TODAS AS MÉTRICAS")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Preferências de densidade: {PREFERENCIAS_DENSIDADE} (0=Sem preferência, 1=Esparso, 2=Denso)")
    print(f"Número de componentes: {NUM_COMPONENTES} (0=Aleatório, 1=Conexo)")
    print(f"Grafos por teste: {num_grafos_exec}")
    print(f"Seeds: {SEEDS}")
    print(f"Formato de saída: {args.output_format}")
    if args.output_format == 'individual_csv':
        print(f"Padrão de nomenclatura: {args.naming_pattern}")
    
    # Calcula total de combinações
    total_combinacoes = (len(TIPOS_GRAFOS) * len(TAMANHOS) * 
                        len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES) * 
                        len(SEEDS))
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Total de grafos gerados: {total_combinacoes * 50}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    

    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for pref_dens in PREFERENCIAS_DENSIDADE:
                for numC in NUM_COMPONENTES:
                    for seed in SEEDS:
                        teste_atual += 1
                        
                        # Calcula número de arestas baseado na preferência de densidade
                        max_arestas = numV * (numV - 1) // 2
                        min_arestas = max(1, numV-1)
                        
                        if pref_dens == 0:  # Sem preferência
                            numA = random.randint(min_arestas, max_arestas)
                        elif pref_dens == 1:  # Esparso (d ≤ 0.2)
                            numA = random.randint(min_arestas, int(max_arestas * DENSIDADE_ESPARSA_MAX))
                        else:  # Denso (d ≥ 0.8)
                            numA = random.randint(int(max_arestas * DENSIDADE_DENSA_MIN), max_arestas)
                        
                        # Mapeia preferência para texto
                        pref_texto = {0: "Sem preferência", 1: "Esparso", 2: "Denso"}[pref_dens]
                        comp_texto = {0: "Aleatório", 1: "Conexo"}[numC]
                        
                        print(f"[{teste_atual:6d}/{total_combinacoes}] Tipo {tipo} - V={numV} - {pref_texto} - {comp_texto} - Seed={seed}")
                        
                        # Réplicas por tamanho
                        if numV >= 1000000:
                            num_grafos_combo = 10
                        elif numV >= 100000:
                            num_grafos_combo = 20
                        elif numV >= 10000:
                            num_grafos_combo = 30
                        else:
                            num_grafos_combo = 50

                        resultado = executa_teste_simples_completo(
                            tipo, numV, numA, seed, "Proporcional", pref_dens, 
                            numC, args.output_format, args.output_dir, args.naming_pattern, num_grafos=num_grafos_combo, timeout_por_grafo_s=args.timeout_por_grafo_s
                        )
                        
                        if resultado:
                            resultados.append(resultado)
                            # Escrita incremental no CSV consolidado (append)
                            try:
                                csv_file_inc = os.path.join(args.output_dir, 'resultados_simples_completo.csv')
                                df_inc = pd.DataFrame([resultado])
                                write_header = not os.path.exists(csv_file_inc)
                                # Garante diretório de saída
                                os.makedirs(args.output_dir, exist_ok=True)
                                df_inc.to_csv(csv_file_inc, mode='a', header=write_header, index=False)
                            except Exception as e:
                                print(f"  [AVISO] Falha ao escrever incremental: {e}")
                            if resultado['limite_atingido']:
                                print(f"  [LIMITE] {resultado.get('erro', 'Erro desconhecido')}")
                            else:
                                print(f"  [OK] Sucesso: {resultado['taxa_sucesso']:.1%} - Consistência: {resultado.get('consistencia_estrutural', 0):.3f}")
                        else:
                            print(f"  [ERRO] Falha")
    

    
    # Salva/relata resultados
    if resultados and args.output_format == 'consolidated_csv':
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal (reescreve consolidado final; incremental já ocorreu)
        csv_file = os.path.join(args.output_dir, 'resultados_simples_completo.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo (resiliente a colunas ausentes)
        resumo_file = os.path.join(args.output_dir, 'resumo_simples_completo.csv')
        desejadas_mean = [
            'densidade', 'grau_medio', 'grau_max', 'grau_min', 'grau_desvio', 'grau_mediana',
            'num_componentes', 'conectividade',
            'pagerank_medio', 'pagerank_max', 'pagerank_min', 'pagerank_desvio', 'pagerank_mediana',
            'closeness_medio', 'closeness_max', 'closeness_min', 'closeness_desvio', 'closeness_mediana',
            'betweenness_medio', 'betweenness_max', 'betweenness_min', 'betweenness_desvio', 'betweenness_mediana',
            'diametro', 'raio', 'distancia_media',
            'num_comunidades_greedy', 'modularidade_greedy', 'num_comunidades_label', 'modularidade_label',
            'razao_vertices_arestas', 'taxa_sucesso', 'consistencia_estrutural', 'similaridade_media', 'n_outliers_estruturais'
        ]
        agg_map = {col: 'mean' for col in desejadas_mean if col in df.columns}
        if 'limite_atingido' in df.columns:
            agg_map['limite_atingido'] = 'sum'
        if agg_map:
            resumo_por_tipo = df.groupby('tipo').agg(agg_map).reset_index()
        else:
            resumo_por_tipo = df.groupby('tipo').size().reset_index(name='count')
        resumo_por_tipo.to_csv(resumo_file, index=False)
        
        print("\n" + "=" * 80)
        print("[OK] EXPERIMENTO SIMPLES COMPLETO CONCLUIDO!")
        print(f"[RESULTADOS] Salvos em: {csv_file}")
        print(f"[RESUMO] Salvo em: {resumo_file}")
        print(f"[SUCESSO] Taxa: {len(resultados)/total_combinacoes*100:.1f}%")
        print(f"[GRAFOS] Total gerados: {len(resultados) * num_grafos_exec}")
        if len(resultados) > 0 and 'consistencia_estrutural' in df.columns:
            print(f"[CONSISTÊNCIA] Média: {df['consistencia_estrutural'].mean():.3f}")
        print("=" * 80)
    elif args.output_format == 'individual_csv':
        # Para formato individual, verifica se há arquivos CSV gerados
        csv_files = [f for f in os.listdir(args.output_dir) if f.endswith('.csv')]
        if csv_files:
            print("\n" + "=" * 80)
            print("[OK] EXPERIMENTO SIMPLES (ARQUIVOS INDIVIDUAIS) CONCLUIDO!")
            print(f"[FORMATO] Arquivos individuais salvos em: {args.output_dir}")
            print(f"[ARQUIVOS] {len(csv_files)} arquivos CSV gerados")
            print("=" * 80)
        else:
            print("[ERRO] Nenhum resultado valido foi gerado!")
    else:
        print("[ERRO] Nenhum resultado valido foi gerado!")

if __name__ == "__main__":
    main()
