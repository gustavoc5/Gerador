#!/usr/bin/env python3
"""
EXPERIMENTO 2: PARÂMETROS CRÍTICOS DO GERADOR SIMPLES
Analisa todos os parâmetros do gerador simples que impactam a geração.

FATORES:
- Número de Vértices (numV): 100, 1000, 10000, 100000, 1000000
- Tipo de Grafo: Simples (0), Digrafo (1), Multigrafo (20), Multigrafo-Dirigido (21), Pseudografo (30), Pseudografo-Dirigido (31)
- Estratégia de Arestas: Proporcional, Aleatório
- Número de Componentes (numC): 0 (conexo), 1, 2, 5, 10
- Fator de Balanceamento (fator): 0 (Aleatório), 1 (Parcialmente Balanceado), 2 (Balanceado)
- Número de Grafos (n): 1, 5, 10
- Seed: 1000, 2000, 3000

VARIÁVEIS DE RESPOSTA:
Tempo de geração, Taxa de sucesso, Densidade resultante, Conectividade, Uso de memória, Número de tentativas.
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

from simples.gerador import geraDataset
from simples.utils import criaMatrizAdjacencias, tipoGrafo
from simples.constants import TIPOS_GRAFOS, TIPOS_VALIDOS, GERACAO

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

def calcula_numero_arestas_proporcional(numV, fator_densidade):
    """Calcula número de arestas proporcional à densidade."""
    max_arestas = numV * (numV - 1) // 2
    return int(max_arestas * fator_densidade)

def executa_teste_simples(tipo, numV, numA, seed, n, numC, fator):
    """Executa teste do gerador simples com todos os parâmetros."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        datasets = geraDataset(tipo, numV, numA, seed, n, numC, fator)
        
        if not datasets:
            return None
        
        # Pega o primeiro dataset para análise
        arestas = datasets[0]
        matriz = criaMatrizAdjacencias(arestas, numV, tipo)
        tipo_detectado = tipoGrafo(matriz)
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        tempo_geracao = time.time() - start_time
        
        return {
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'n': n,
            'numC': numC,
            'fator': fator,
            'estrategia_arestas': 'Proporcional' if numA == calcula_numero_arestas_proporcional(numV, 0.5) else 'Aleatório',
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'taxa_sucesso': 1.0,
            'num_datasets_gerados': len(datasets),
            **metricas
        }
        
    except Exception as e:
        print(f"ERRO: {e}")
        return None

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento 2: Parâmetros Críticos do Gerador Simples')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp2_parametros_simples',
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
    
    ESTRATEGIAS_ARESTAS = ['Proporcional', 'Aleatório']
    FATORES_DENSIDADE = [0.1, 0.3, 0.5, 0.7, 0.9]  # Para estratégia proporcional
    NUM_COMPONENTES = [0, 1, 2, 5, 10]
    FATORES_BALANCEAMENTO = [0, 1, 2]  # Aleatório, Parcialmente Balanceado, Balanceado
    NUM_GRAFOS = [1, 5, 10]
    SEEDS = args.seeds
    
    # Modo teste rápido
    if args.teste_rapido:
        TAMANHOS = [100, 1000]
        TIPOS_GRAFOS = [0, 1, 20]
        FATORES_DENSIDADE = [0.3, 0.7]
        NUM_COMPONENTES = [0, 2]
        FATORES_BALANCEAMENTO = [0, 2]
        NUM_GRAFOS = [1, 5]
        SEEDS = [1000, 2000]
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO 2: PARÂMETROS CRÍTICOS DO GERADOR SIMPLES")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Estratégias de arestas: {ESTRATEGIAS_ARESTAS}")
    print(f"Fatores de densidade: {FATORES_DENSIDADE}")
    print(f"Número de componentes: {NUM_COMPONENTES}")
    print(f"Fatores de balanceamento: {FATORES_BALANCEAMENTO}")
    print(f"Número de grafos: {NUM_GRAFOS}")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = len(TIPOS_GRAFOS) * len(TAMANHOS) * len(ESTRATEGIAS_ARESTAS) * len(FATORES_DENSIDADE) * len(NUM_COMPONENTES) * len(FATORES_BALANCEAMENTO) * len(NUM_GRAFOS) * len(SEEDS)
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    
    start_time_experimento = time.time()
    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for estrategia in ESTRATEGIAS_ARESTAS:
                for fator_densidade in FATORES_DENSIDADE:
                    for numC in NUM_COMPONENTES:
                        for fator in FATORES_BALANCEAMENTO:
                            for n in NUM_GRAFOS:
                                for seed in SEEDS:
                                    teste_atual += 1
                                    
                                    # Calcula número de arestas baseado na estratégia
                                    if estrategia == 'Proporcional':
                                        numA = calcula_numero_arestas_proporcional(numV, fator_densidade)
                                    else:  # Aleatório
                                        max_arestas = numV * (numV - 1) // 2
                                        numA = random.randint(max(1, numV-1), max_arestas)
                                    
                                    print(f"[{teste_atual:4d}/{total_combinacoes}] Tipo {tipo} - V={numV} - A={numA} - C={numC} - F={fator} - N={n} - Seed={seed}")
                                    
                                    resultado = executa_teste_simples(tipo, numV, numA, seed, n, numC, fator)
                                    
                                    if resultado:
                                        resultados.append(resultado)
                                        print(f"  ✅ Sucesso - Tempo: {resultado['tempo_geracao']:.3f}s")
                                    else:
                                        print(f"  ❌ Falha")
    
    end_time_experimento = time.time()
    tempo_total = end_time_experimento - start_time_experimento
    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_experimento2.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_experimento2.txt')
        with open(resumo_file, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 2: PARÂMETROS CRÍTICOS DO GERADOR SIMPLES\n")
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
                    f.write(f"TIPO {tipo} ({TIPOS_GRAFOS[tipo]}):\n")
                    f.write(f"  Testes: {len(df_tipo)}\n")
                    f.write(f"  Tempo médio: {df_tipo['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Densidade média: {df_tipo['densidade'].mean():.4f}\n")
                    f.write(f"  Conectividade média: {df_tipo['conectividade'].mean():.4f}\n\n")
            
            # Estatísticas por fator de balanceamento
            for fator in FATORES_BALANCEAMENTO:
                df_fator = df[df['fator'] == fator]
                if len(df_fator) > 0:
                    f.write(f"FATOR {fator} ({GERACAO[fator]}):\n")
                    f.write(f"  Testes: {len(df_fator)}\n")
                    f.write(f"  Tempo médio: {df_fator['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Taxa de sucesso: {len(df_fator)/len(df)*100:.1f}%\n\n")
        
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
