#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPERIMENTO POWER-LAW COMPLETO
Experimento unificado para o gerador Power-Law com todas as métricas possíveis.

FATORES:
- Tipo de Grafo: 0, 1, 20, 21, 30, 31 (6 tipos)
- Tamanho (numV): 100, 1000, 10000, 100000, 1000000
- Expoente Gamma (γ): 2.0, 2.2, 2.5, 2.8, 3.0
- Seed: 1000, 2000, 3000, 4000, 5000

MÉTRICAS COLETADAS:
- Todas as métricas básicas, de centralidade, distância, comunidades
- Métricas de performance e memória
- Métricas específicas do power-law (qualidade do ajuste)
"""

import os
import sys
import random
import time
import signal
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime
import time

# Adiciona o diretório src ao path
sys.path.append(os.path.dirname(__file__))

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    dependencias = {
        'numpy': 'NumPy',
        'networkx': 'NetworkX', 
        'scipy': 'SciPy',
        'pandas': 'Pandas',
        'powerlaw': 'Powerlaw',
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
# Prioriza o diretório pwl no sys.path e evita adicionar 'simples' aqui para não haver
# conflito ao resolver 'constants' dentro de pwl/pwl.py
pwl_dir = os.path.join(os.path.dirname(__file__), '..', 'pwl')
if pwl_dir not in sys.path:
    sys.path.insert(0, pwl_dir)

# Importação direta do arquivo pwl.py
import importlib.util
pwl_path = os.path.join(os.path.dirname(__file__), '..', 'pwl', 'pwl.py')
spec = importlib.util.spec_from_file_location("pwl_module", pwl_path)
pwl_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pwl_module)
geraGrafoPwl = pwl_module.geraGrafoPwl

# Importação das constantes do pwl
constants_path = os.path.join(os.path.dirname(__file__), '..', 'pwl', 'constants.py')
spec_constants = importlib.util.spec_from_file_location("pwl_constants", constants_path)
pwl_constants = importlib.util.module_from_spec(spec_constants)
spec_constants.loader.exec_module(pwl_constants)
GAMMA_MIN = pwl_constants.GAMMA_MIN
GAMMA_MAX = pwl_constants.GAMMA_MAX
GRAU_MIN_PADRAO = pwl_constants.GRAU_MIN_PADRAO

def gera_gamma_aleatorio(categoria):
    """
    Gera um valor gamma aleatório dentro da categoria especificada.
    
    Args:
        categoria (str): 'denso', 'moderado', ou 'esparso'
    
    Returns:
        float: Valor gamma aleatório no intervalo da categoria
    """
    if categoria == 'denso':
        return np.random.uniform(2.0, 2.3)
    elif categoria == 'moderado':
        return np.random.uniform(2.3, 2.7)
    elif categoria == 'esparso':
        return np.random.uniform(2.7, 3.0)
    else:
        raise ValueError(f"Categoria inválida: {categoria}")



def gera_gamma_deterministico(categoria: str, seed_ctx: int) -> float:
    """Gera gamma determinístico por combinação (seed, tipo, numV, categoria)."""
    rng = np.random.default_rng(seed_ctx)
    if categoria == 'denso':
        return float(rng.uniform(2.0, 2.3))
    elif categoria == 'moderado':
        return float(rng.uniform(2.3, 2.7))
    elif categoria == 'esparso':
        return float(rng.uniform(2.7, 3.0))
    else:
        raise ValueError(f"Categoria inválida: {categoria}")

def calcula_qualidade_powerlaw(graus):
    """Calcula a qualidade do ajuste power-law."""
    try:
        import powerlaw
        
        # Filtra graus > 0
        graus_positivos = [g for g in graus if g > 0]
        if len(graus_positivos) < 10:
            return 0.0, 0.0, 0.0, 0.0
        
        # Ajusta distribuição power-law
        fit = powerlaw.Fit(graus_positivos, discrete=True)
        
        # Teste de Kolmogorov-Smirnov
        R, p_value = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
        
        # Parâmetros do ajuste
        alpha = fit.alpha
        xmin = fit.xmin
        
        return R, p_value, alpha, xmin
        
    except Exception as e:
        print(f"ERRO no cálculo power-law: {e}")
        return 0.0, 0.0, 0.0, 0.0

def calcula_metricas_completas_por_grafo(G, tipo_grafo, graus=None):
    """Calcula todas as métricas possíveis do grafo diretamente do objeto Graph."""
    metricas = {}
    n = int(G.number_of_nodes())
    # Perfis por tamanho
    perfil_full = n <= 10000
    perfil_mid = 10000 < n <= 100000
    perfil_large = n > 100000
    
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
        graus_grafo = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus_grafo)
        metricas['grau_max'] = max(graus_grafo)
        metricas['grau_min'] = min(graus_grafo)
        metricas['grau_desvio'] = np.std(graus_grafo)
        metricas['grau_mediana'] = np.median(graus_grafo)
        
        # Distribuição de graus
        metricas['grau_skewness'] = pd.Series(graus_grafo).skew()
        metricas['grau_kurtosis'] = pd.Series(graus_grafo).kurtosis()
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
        metricas['grau_desvio'] = metricas['grau_mediana'] = 0
        metricas['grau_skewness'] = metricas['grau_kurtosis'] = 0
    
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
            try:
                from networkx.algorithms.link_analysis.pagerank_alg import pagerank_scipy as pr_scipy
                pagerank = pr_scipy(G, max_iter=30, tol=1e-4)
            except Exception:
                pagerank = nx.pagerank(G, max_iter=30, tol=1e-4)
        elif perfil_mid:
            pagerank = nx.pagerank(G, max_iter=50)
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
            closeness = nx.closeness_centrality(G)
            metricas['closeness_medio'] = np.mean(list(closeness.values()))
            metricas['closeness_max'] = max(closeness.values())
            metricas['closeness_min'] = min(closeness.values())
            metricas['closeness_desvio'] = np.std(list(closeness.values()))
            metricas['closeness_mediana'] = np.median(list(closeness.values()))
        except Exception:
            metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
            metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
    else:
        metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
        metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
    
    if not perfil_large:
        try:
            k_bt = min(100, G.number_of_nodes()) if perfil_full else min(50, G.number_of_nodes())
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
            communities_label = nx.community.label_propagation_communities(G_und)
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
    
    # ===== MÉTRICAS ESPECÍFICAS DO POWER-LAW =====
    if graus is not None:
        # Calcula qualidade do power-law
        R, p_value, alpha, xmin = calcula_qualidade_powerlaw(graus)
        metricas['qualidade_powerlaw_R'] = R
        metricas['qualidade_powerlaw_p_value'] = p_value
        metricas['powerlaw_alpha'] = alpha
        metricas['powerlaw_xmin'] = xmin
        

        
        # Razão vértices/arestas
        metricas['razao_vertices_arestas'] = metricas['num_vertices'] / metricas['num_arestas'] if metricas['num_arestas'] > 0 else 0
    else:
        metricas['qualidade_powerlaw_R'] = 0.0
        metricas['qualidade_powerlaw_p_value'] = 1.0
        metricas['powerlaw_alpha'] = 0.0
        metricas['powerlaw_xmin'] = 0.0

        metricas['razao_vertices_arestas'] = 0.0
    
    return metricas

def executa_teste_powerlaw_completo(tipo, numV, gamma, seed, output_format='consolidated_csv', output_dir='./resultados', naming_pattern='metricas_{seed}_tipo{tipo}_v{vertices}_gamma{gamma}_{numero}.csv', num_grafos=50, timeout_por_grafo_s: int = 0):
    """Executa teste do gerador power-law com todas as métricas."""
    try:
        
        # Gera grafos com os mesmos parâmetros (configurável por --num_grafos)
        dirigido = tipo in [1, 21, 31]
        
        todas_metricas = []
        
        for i in range(num_grafos):
            # Gera um grafo
            # Compatibiliza seeds potencialmente > 2**32-1 (alguns RNGs exigem 32 bits)
            seed_effective = int(seed) + int(i)
            try:
                seed_compat = int(seed_effective % (2**32 - 1))
            except Exception:
                seed_compat = int(abs(hash((seed_effective, tipo, numV))) & 0xFFFFFFFF)
            t0 = time.perf_counter()
            # Timeout por grafo somente na geração (se suportado)
            try:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimeoutError("Timeout por grafo atingido")))
                    signal.alarm(int(timeout_por_grafo_s))
                resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed_compat)
            except TimeoutError:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                continue
            finally:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
            
            if resultado is None:
                continue
            
            arestas, G, graus = resultado
            tempo_geracao_s = time.perf_counter() - t0
            tipo_detectado = tipo
            
            # Calcula métricas completas diretamente do Graph (com timeout, se configurado)
            try:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimeoutError("Timeout por grafo atingido")))
                    signal.alarm(int(timeout_por_grafo_s))
                metricas = calcula_metricas_completas_por_grafo(G, tipo_detectado, graus)
            except TimeoutError:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
                # Salva métricas básicas mesmo com timeout
                try:
                    metricas = {}
                    metricas['num_vertices'] = G.number_of_nodes()
                    metricas['num_arestas'] = G.number_of_edges()
                    metricas['tipo_detectado'] = tipo_detectado
                    if G.number_of_nodes() > 1:
                        max_arestas = G.number_of_nodes() * (G.number_of_nodes() - 1)
                        if not G.is_directed():
                            max_arestas //= 2
                        metricas['densidade'] = G.number_of_edges() / max_arestas
                    else:
                        metricas['densidade'] = 0.0
                    graus_grafo = [d for n, d in G.degree()]
                    if graus_grafo:
                        metricas['grau_medio'] = float(np.mean(graus_grafo))
                        metricas['grau_max'] = int(max(graus_grafo))
                        metricas['grau_min'] = int(min(graus_grafo))
                        metricas['grau_desvio'] = float(np.std(graus_grafo))
                        metricas['grau_mediana'] = float(np.median(graus_grafo))
                    else:
                        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
                        metricas['grau_desvio'] = metricas['grau_mediana'] = 0
                    metricas['razao_vertices_arestas'] = (
                        metricas['num_vertices'] / metricas['num_arestas'] if metricas['num_arestas'] > 0 else 0.0
                    )
                    metricas['metricas_incompletas'] = True
                except Exception:
                    continue
            finally:
                if timeout_por_grafo_s and hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
            
            # Adiciona parâmetros do teste
            metricas.update({
                'gerador': 'Power-Law',
                'tipo': tipo,
                'numV': numV,
                'gamma': gamma,
                'seed': seed,
                'numero': i + 1,
                'tempo_geracao_s': tempo_geracao_s
            })
            
            # Se formato individual, salva arquivo CSV imediatamente
            if output_format == 'individual_csv':
                nome_arquivo = naming_pattern.format(
                    seed=seed,
                    tipo=tipo,
                    vertices=numV,
                    gamma=gamma,
                    numero=i + 1
                )
                caminho_arquivo = os.path.join(output_dir, nome_arquivo)
                
                # Cria diretório se não existir
                os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
                
                # Salva CSV individual
                df_individual = pd.DataFrame([metricas])
                df_individual.to_csv(caminho_arquivo, index=False)
                print(f"  [CSV] Salvo: {nome_arquivo}")
            
            todas_metricas.append(metricas)
        
        if not todas_metricas:
            return None
        
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
        
        # Adiciona métricas básicas
        metricas_medias.update({
            'taxa_sucesso': len(todas_metricas) / num_grafos,
            'limite_atingido': False
        })
        
        return metricas_medias
        
    except MemoryError:
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': 'MemoryError'
        }
    except Exception as e:
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,

            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def main():
    """Função principal do experimento."""
    # Verificar dependências antes de continuar
    verificar_dependencias()
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento Power-Law Completo - Todas as métricas')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp_powerlaw_completo',
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
                       default='metricas_{seed}_tipo{tipo}_v{vertices}_gamma{gamma}_{numero}.csv',
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
        CATEGORIAS_GAMMA = ['denso']
        SEEDS = args.seeds
        num_grafos_exec = min(args.num_grafos, 2)
    elif args.teste_rapido:
        TAMANHOS = [100, 1000]
        CATEGORIAS_GAMMA = ['denso', 'moderado']
        SEEDS = [1000, 2000]
        num_grafos_exec = args.num_grafos
    else:
        TAMANHOS = [100, 1000, 10000]
        if args.max_vertices >= 100000:
            TAMANHOS.append(100000)
        if args.max_vertices >= 1000000:
            TAMANHOS.append(1000000)
        CATEGORIAS_GAMMA = ['denso', 'moderado', 'esparso']
        SEEDS = args.seeds
        num_grafos_exec = args.num_grafos
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO POWER-LAW COMPLETO - TODAS AS MÉTRICAS")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Categorias gamma: {CATEGORIAS_GAMMA}")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = (len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA) * len(SEEDS))
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    

    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for categoria_gamma in CATEGORIAS_GAMMA:
                for seed in SEEDS:
                    teste_atual += 1
                    
                    # Gera gamma determinístico por combinação (seed, tipo, numV, categoria)
                    seed_ctx = (hash((int(seed), int(tipo), int(numV), str(categoria_gamma))) & 0xFFFFFFFF)
                    gamma = gera_gamma_deterministico(categoria_gamma, seed_ctx)
                    
                    print(f"[{teste_atual:6d}/{total_combinacoes}] Tipo {tipo} - V={numV} - {categoria_gamma} (gamma={gamma:.3f}) - Seed={seed}")
                    
                    resultado = executa_teste_powerlaw_completo(
                        tipo, numV, gamma, seed, args.output_format, args.output_dir, args.naming_pattern, num_grafos=num_grafos_exec, timeout_por_grafo_s=args.timeout_por_grafo_s
                    )
                    
                    if resultado:
                        resultados.append(resultado)
                        if resultado['limite_atingido']:
                            print(f"  [LIMITE] {resultado.get('erro', 'Erro desconhecido')}")
                        else:
                            print(f"  [OK] R={resultado['qualidade_powerlaw_R']:.3f}")
                    else:
                        print(f"  [ERRO] Falha")
    

    
    # Salva resultados
    if args.output_format == 'consolidated_csv' and resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_powerlaw_completo.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_powerlaw_completo.csv')
        
        # Cria resumo agrupado por tipo (resiliente a colunas ausentes)
        desejadas_mean = [
            'densidade', 'grau_medio', 'grau_max', 'grau_min', 'grau_desvio', 'grau_mediana',
            'num_componentes', 'conectividade',
            'pagerank_medio', 'pagerank_max', 'pagerank_min', 'pagerank_desvio', 'pagerank_mediana',
            'closeness_medio', 'closeness_max', 'closeness_min', 'closeness_desvio', 'closeness_mediana',
            'betweenness_medio', 'betweenness_max', 'betweenness_min', 'betweenness_desvio', 'betweenness_mediana',
            'diametro', 'raio', 'distancia_media',
            'num_comunidades_greedy', 'modularidade_greedy', 'num_comunidades_label', 'modularidade_label',
            'razao_vertices_arestas', 'taxa_sucesso', 'qualidade_powerlaw_R', 'powerlaw_alpha'
        ]
        agg_map = {col: 'mean' for col in desejadas_mean if col in df.columns}
        if 'limite_atingido' in df.columns:
            agg_map['limite_atingido'] = 'sum'

        if agg_map:
            resumo_por_tipo = df.groupby('tipo').agg(agg_map).reset_index()
        else:
            # Fallback mínimo quando não há colunas numéricas esperadas (ex.: todas combinações falharam)
            resumo_por_tipo = df.groupby('tipo').size().reset_index(name='count')
        
        resumo_por_tipo.to_csv(resumo_file, index=False)
        
        print("\n" + "=" * 80)
        print("[OK] EXPERIMENTO POWER-LAW COMPLETO CONCLUIDO!")
        if args.output_format == 'consolidated_csv':
            print(f"[RESULTADOS] Salvos em: {csv_file}")
            print(f"[RESUMO] Salvo em: {resumo_file}")
        else:
            print(f"[FORMATO] Arquivos individuais salvos em: {args.output_dir}")
        print(f"[SUCESSO] Taxa: {len(resultados)/total_combinacoes*100:.1f}%")
        print("=" * 80)
    elif args.output_format == 'individual_csv':
        # Para formato individual, verifica se há arquivos CSV gerados
        csv_files = [f for f in os.listdir(args.output_dir) if f.endswith('.csv')]
        if csv_files:
            print("\n" + "=" * 80)
            print("[OK] EXPERIMENTO POWER-LAW COMPLETO CONCLUIDO!")
            print(f"[FORMATO] Arquivos individuais salvos em: {args.output_dir}")
            print(f"[ARQUIVOS] {len(csv_files)} arquivos CSV gerados")
            print("=" * 80)
        else:
            print("[ERRO] Nenhum resultado valido foi gerado!")
    else:
        print("[ERRO] Nenhum resultado valido foi gerado!")

if __name__ == "__main__":
    main()
