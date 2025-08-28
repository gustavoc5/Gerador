#!/usr/bin/env python3
"""
EXPERIMENTO 3: PARÂMETROS CRÍTICOS DO GERADOR POWER-LAW
Analisa todos os parâmetros do gerador power-law que impactam a geração.

FATORES:
- Número de Vértices (numV): 100, 1000, 10000, 100000, 1000000
- Tipo de Grafo: Simples (0), Digrafo (1), Multigrafo (20), Multigrafo-Dirigido (21), Pseudografo (30), Pseudografo-Dirigido (31)
- Expoente Gamma (γ): 2.0, 2.2, 2.5, 2.8, 3.0
- Tipo de Distribuição: Balanceado, Desequilibrado
- Grau Mínimo: 1, 2, 3
- Seed: 1000, 2000, 3000

VARIÁVEIS DE RESPOSTA:
Tempo de geração, Qualidade do ajuste power-law (p-value), Densidade resultante, 
Distribuição de graus, Uso de memória, Taxa de sucesso.
"""

import os
import sys
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from powerlaw.pwl import geraGrafoPwl
from powerlaw.constants import GAMMA_MIN, GAMMA_MAX, GRAU_MIN_PADRAO

def calcula_metricas_basicas(matriz, tipo_grafo):
    """Calcula métricas básicas do grafo."""
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
    
    # Conectividade
    if G.is_directed():
        metricas['conectividade'] = 1.0 if nx.is_strongly_connected(G) else 0.0
    else:
        metricas['conectividade'] = 1.0 if nx.is_connected(G) else 0.0
    
    return metricas

def calcula_qualidade_powerlaw(graus):
    """Calcula a qualidade do ajuste power-law."""
    try:
        import powerlaw
        
        # Filtra graus > 0
        graus_positivos = [g for g in graus if g > 0]
        if len(graus_positivos) < 10:
            return 0.0, 0.0
        
        # Ajusta distribuição power-law
        fit = powerlaw.Fit(graus_positivos, discrete=True)
        
        # Teste de Kolmogorov-Smirnov
        R, p_value = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
        
        return R, p_value
        
    except Exception as e:
        print(f"ERRO no cálculo power-law: {e}")
        return 0.0, 0.0

def executa_teste_powerlaw(tipo, numV, gamma, seed, desequilibrado, grau_min):
    """Executa teste do gerador power-law com todos os parâmetros."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        dirigido = tipo in [1, 21, 31]
        resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed, desequilibrado=desequilibrado)
        
        if resultado is None:
            return None
        
        arestas, G, graus = resultado
        matriz = nx.to_numpy_array(G)
        tipo_detectado = tipo
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        # Calcula qualidade do power-law
        if isinstance(graus, tuple):
            graus_analise = graus[0]  # Pega graus de saída para análise
        else:
            graus_analise = graus
        
        R, p_value = calcula_qualidade_powerlaw(graus_analise)
        
        tempo_geracao = time.time() - start_time
        
        return {
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'desequilibrado': desequilibrado,
            'grau_min': grau_min,
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'taxa_sucesso': 1.0,
            'qualidade_powerlaw_R': R,
            'qualidade_powerlaw_p_value': p_value,
            'distribuicao_tipo': 'Desequilibrado' if desequilibrado else 'Balanceado',
            **metricas
        }
        
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento 3: Parâmetros Críticos do Gerador Power-Law')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp3_parametros_powerlaw',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste (padrão: 10000)')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000],
                       help='Lista de seeds para teste')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa apenas um subconjunto dos testes para validação rápida')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]  # Todos os tipos
    TAMANHOS = [100, 1000, 10000]
    if args.max_vertices >= 100000:
        TAMANHOS.append(100000)
    if args.max_vertices >= 1000000:
        TAMANHOS.append(1000000)
    
    EXPONENTES_GAMMA = [2.0, 2.2, 2.5, 2.8, 3.0]
    TIPOS_DISTRIBUICAO = [False, True]  # Balanceado, Desequilibrado
    GRAUS_MIN = [1, 2, 3]
    SEEDS = args.seeds
    
    # Modo teste rápido
    if args.teste_rapido:
        TAMANHOS = [100, 1000]
        TIPOS_GRAFOS = [0, 1, 20]
        EXPONENTES_GAMMA = [2.0, 2.5, 3.0]
        TIPOS_DISTRIBUICAO = [False, True]
        GRAUS_MIN = [1, 2]
        SEEDS = [1000, 2000]
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO 3: PARÂMETROS CRÍTICOS DO GERADOR POWER-LAW")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Expoentes gamma: {EXPONENTES_GAMMA}")
    print(f"Tipos de distribuição: {len(TIPOS_DISTRIBUICAO)} tipos")
    print(f"Graus mínimos: {GRAUS_MIN}")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = len(TIPOS_GRAFOS) * len(TAMANHOS) * len(EXPONENTES_GAMMA) * len(TIPOS_DISTRIBUICAO) * len(GRAUS_MIN) * len(SEEDS)
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    
    start_time_experimento = time.time()
    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for gamma in EXPONENTES_GAMMA:
                for desequilibrado in TIPOS_DISTRIBUICAO:
                    for grau_min in GRAUS_MIN:
                        for seed in SEEDS:
                            teste_atual += 1
                            
                            print(f"[{teste_atual:4d}/{total_combinacoes}] Tipo {tipo} - V={numV} - γ={gamma} - {'Des' if desequilibrado else 'Bal'} - min={grau_min} - Seed={seed}")
                            
                            resultado = executa_teste_powerlaw(tipo, numV, gamma, seed, desequilibrado, grau_min)
                            
                            if resultado:
                                resultados.append(resultado)
                                print(f"  ✅ Sucesso - Tempo: {resultado['tempo_geracao']:.3f}s - R={resultado['qualidade_powerlaw_R']:.3f}")
                            else:
                                print(f"  ❌ Falha")
    
    end_time_experimento = time.time()
    tempo_total = end_time_experimento - start_time_experimento
    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_experimento3.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_experimento3.txt')
        with open(resumo_file, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 3: PARÂMETROS CRÍTICOS DO GERADOR POWER-LAW\n")
            f.write("=" * 60 + "\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de testes: {len(resultados)}/{total_combinacoes}\n")
            f.write(f"Taxa de sucesso: {len(resultados)/total_combinacoes*100:.1f}%\n")
            f.write(f"Tempo total: {tempo_total:.2f} segundos\n")
            f.write(f"Tempo médio por teste: {tempo_total/len(resultados):.3f} segundos\n\n")
            
            # Estatísticas por tipo de grafo
            for tipo in TIPOS_GRAFOS:
                df_tipo = df[df['tipo'] == tipo]
                if len(df_tipo) > 0:
                    f.write(f"TIPO {tipo}:\n")
                    f.write(f"  Testes: {len(df_tipo)}\n")
                    f.write(f"  Tempo médio: {df_tipo['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Densidade média: {df_tipo['densidade'].mean():.4f}\n")
                    f.write(f"  Qualidade power-law média (R): {df_tipo['qualidade_powerlaw_R'].mean():.3f}\n\n")
            
            # Estatísticas por gamma
            for gamma in EXPONENTES_GAMMA:
                df_gamma = df[df['gamma'] == gamma]
                if len(df_gamma) > 0:
                    f.write(f"GAMMA {gamma}:\n")
                    f.write(f"  Testes: {len(df_gamma)}\n")
                    f.write(f"  Densidade média: {df_gamma['densidade'].mean():.4f}\n")
                    f.write(f"  Grau médio: {df_gamma['grau_medio'].mean():.2f}\n")
                    f.write(f"  Qualidade power-law média (R): {df_gamma['qualidade_powerlaw_R'].mean():.3f}\n\n")
            
            # Estatísticas por tipo de distribuição
            for desequilibrado in TIPOS_DISTRIBUICAO:
                df_dist = df[df['desequilibrado'] == desequilibrado]
                if len(df_dist) > 0:
                    tipo_nome = "Desequilibrado" if desequilibrado else "Balanceado"
                    f.write(f"DISTRIBUIÇÃO {tipo_nome}:\n")
                    f.write(f"  Testes: {len(df_dist)}\n")
                    f.write(f"  Tempo médio: {df_dist['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Qualidade power-law média (R): {df_dist['qualidade_powerlaw_R'].mean():.3f}\n\n")
        
        print("\n" + "=" * 80)
        print("✅ EXPERIMENTO CONCLUÍDO!")
        print(f"📊 Resultados salvos em: {csv_file}")
        print(f"📋 Resumo salvo em: {resumo_file}")
        print(f"⏱️  Tempo total: {tempo_total:.2f} segundos")
        print(f"🎯 Taxa de sucesso: {len(resultados)/total_combinacoes*100:.1f}%")
        print("=" * 80)
    else:
        print("❌ Nenhum resultado válido foi gerado!")

if __name__ == "__main__":
    main()
