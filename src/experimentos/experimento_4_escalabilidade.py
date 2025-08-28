#!/usr/bin/env python3
"""
EXPERIMENTO 4: ANÁLISE DE ESCALABILIDADE E LIMITAÇÕES
Avalia o comportamento dos geradores com tamanhos extremos de grafos.

FATORES:
- Tamanho do Grafo (numV): 10000, 100000, 1000000
- Gerador: Simples, Power-Law
- Tipo de Grafo: Simples (0), Digrafo (1), Multigrafo (20), Multigrafo-Dirigido (21), Pseudografo (30), Pseudografo-Dirigido (31)
- Estratégia de Memória: Padrão, Otimizada
- Seed: 1000, 2000

VARIÁVEIS DE RESPOSTA:
Tempo de geração, Uso de memória, Taxa de sucesso, Limitações de hardware, 
Qualidade das métricas, Limitações de escalabilidade.
"""

import os
import sys
import random
import time
import psutil
import pandas as pd
import numpy as np
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simples.gerador import geraDataset
from simples.utils import criaMatrizAdjacencias, tipoGrafo
from powerlaw.pwl import geraGrafoPwl
from simples.constants import TIPOS_GRAFOS, TIPOS_VALIDOS
from powerlaw.constants import GAMMA_MIN, GAMMA_MAX

def monitora_memoria():
    """Monitora o uso de memória do processo atual."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def calcula_metricas_basicas(matriz, tipo_grafo):
    """Calcula métricas básicas do grafo (versão otimizada para grandes grafos)."""
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
    
    # Grau médio (otimizado para grandes grafos)
    if G.number_of_nodes() > 0:
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
    
    # Componentes conexas (otimizado)
    try:
        if G.is_directed():
            metricas['num_componentes'] = nx.number_strongly_connected_components(G)
        else:
            metricas['num_componentes'] = nx.number_connected_components(G)
    except:
        metricas['num_componentes'] = 1
    
    # Conectividade (otimizado)
    try:
        if G.is_directed():
            metricas['conectividade'] = 1.0 if nx.is_strongly_connected(G) else 0.0
        else:
            metricas['conectividade'] = 1.0 if nx.is_connected(G) else 0.0
    except:
        metricas['conectividade'] = 0.0
    
    return metricas

def executa_teste_simples_escalabilidade(tipo, numV, numA, seed, estrategia_memoria):
    """Executa teste do gerador simples com monitoramento de escalabilidade."""
    try:
        # Monitora memória inicial
        memoria_inicial = monitora_memoria()
        start_time = time.time()
        
        # Gera o grafo
        datasets = geraDataset(tipo, numV, numA, seed, n=1, numC=0, fator=1.0)
        
        if not datasets:
            return None
        
        # Monitora memória após geração
        memoria_pos_geracao = monitora_memoria()
        
        # Pega o primeiro dataset para análise
        arestas = datasets[0]
        matriz = criaMatrizAdjacencias(arestas, numV, tipo)
        
        # Monitora memória após criação da matriz
        memoria_pos_matriz = monitora_memoria()
        
        tipo_detectado = tipoGrafo(matriz)
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        # Monitora memória final
        memoria_final = monitora_memoria()
        tempo_geracao = time.time() - start_time
        
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_memoria': estrategia_memoria,
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'memoria_inicial_mb': memoria_inicial,
            'memoria_pos_geracao_mb': memoria_pos_geracao,
            'memoria_pos_matriz_mb': memoria_pos_matriz,
            'memoria_final_mb': memoria_final,
            'memoria_pico_mb': max(memoria_inicial, memoria_pos_geracao, memoria_pos_matriz, memoria_final),
            'memoria_incremento_mb': memoria_final - memoria_inicial,
            'taxa_sucesso': 1.0,
            'limite_atingido': False,
            **metricas
        }
        
    except MemoryError:
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_memoria': estrategia_memoria,
            'tempo_geracao': 0.0,
            'memoria_inicial_mb': monitora_memoria(),
            'memoria_pos_geracao_mb': 0.0,
            'memoria_pos_matriz_mb': 0.0,
            'memoria_final_mb': 0.0,
            'memoria_pico_mb': 0.0,
            'memoria_incremento_mb': 0.0,
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
            'estrategia_memoria': estrategia_memoria,
            'tempo_geracao': 0.0,
            'memoria_inicial_mb': monitora_memoria(),
            'memoria_pos_geracao_mb': 0.0,
            'memoria_pos_matriz_mb': 0.0,
            'memoria_final_mb': 0.0,
            'memoria_pico_mb': 0.0,
            'memoria_incremento_mb': 0.0,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def executa_teste_powerlaw_escalabilidade(tipo, numV, gamma, seed, estrategia_memoria):
    """Executa teste do gerador power-law com monitoramento de escalabilidade."""
    try:
        # Monitora memória inicial
        memoria_inicial = monitora_memoria()
        start_time = time.time()
        
        # Gera o grafo
        dirigido = tipo in [1, 21, 31]
        resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed, desequilibrado=False)
        
        if resultado is None:
            return None
        
        # Monitora memória após geração
        memoria_pos_geracao = monitora_memoria()
        
        arestas, G, graus = resultado
        matriz = nx.to_numpy_array(G)
        
        # Monitora memória após criação da matriz
        memoria_pos_matriz = monitora_memoria()
        
        tipo_detectado = tipo
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        # Monitora memória final
        memoria_final = monitora_memoria()
        tempo_geracao = time.time() - start_time
        
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'estrategia_memoria': estrategia_memoria,
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'memoria_inicial_mb': memoria_inicial,
            'memoria_pos_geracao_mb': memoria_pos_geracao,
            'memoria_pos_matriz_mb': memoria_pos_matriz,
            'memoria_final_mb': memoria_final,
            'memoria_pico_mb': max(memoria_inicial, memoria_pos_geracao, memoria_pos_matriz, memoria_final),
            'memoria_incremento_mb': memoria_final - memoria_inicial,
            'taxa_sucesso': 1.0,
            'limite_atingido': False,
            **metricas
        }
        
    except MemoryError:
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'estrategia_memoria': estrategia_memoria,
            'tempo_geracao': 0.0,
            'memoria_inicial_mb': monitora_memoria(),
            'memoria_pos_geracao_mb': 0.0,
            'memoria_pos_matriz_mb': 0.0,
            'memoria_final_mb': 0.0,
            'memoria_pico_mb': 0.0,
            'memoria_incremento_mb': 0.0,
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
            'estrategia_memoria': estrategia_memoria,
            'tempo_geracao': 0.0,
            'memoria_inicial_mb': monitora_memoria(),
            'memoria_pos_geracao_mb': 0.0,
            'memoria_pos_matriz_mb': 0.0,
            'memoria_final_mb': 0.0,
            'memoria_pico_mb': 0.0,
            'memoria_incremento_mb': 0.0,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento 4: Análise de Escalabilidade e Limitações')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp4_escalabilidade',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=100000,
                       help='Máximo de vértices para teste (padrão: 100000)')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000],
                       help='Lista de seeds para teste')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa apenas um subconjunto dos testes para validação rápida')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    GERADORES = ['Simples', 'Power-Law']
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]  # Todos os tipos
    TAMANHOS = [10000, 100000]
    if args.max_vertices >= 1000000:
        TAMANHOS.append(1000000)
    
    ESTRATEGIAS_MEMORIA = ['Padrão', 'Otimizada']
    SEEDS = args.seeds
    
    # Modo teste rápido
    if args.teste_rapido:
        TAMANHOS = [10000]
        TIPOS_GRAFOS = [0, 1, 20]
        ESTRATEGIAS_MEMORIA = ['Padrão']
        SEEDS = [1000]
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO 4: ANÁLISE DE ESCALABILIDADE E LIMITAÇÕES")
    print("=" * 80)
    print(f"Geradores: {GERADORES}")
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Estratégias de memória: {ESTRATEGIAS_MEMORIA}")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = len(GERADORES) * len(TIPOS_GRAFOS) * len(TAMANHOS) * len(ESTRATEGIAS_MEMORIA) * len(SEEDS)
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    # Informações do sistema
    memoria_total = psutil.virtual_memory().total / 1024 / 1024 / 1024  # GB
    print(f"💾 Memória total do sistema: {memoria_total:.1f} GB")
    print(f"🖥️  CPUs disponíveis: {psutil.cpu_count()}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    
    start_time_experimento = time.time()
    
    for gerador in GERADORES:
        for tipo in TIPOS_GRAFOS:
            for numV in TAMANHOS:
                for estrategia in ESTRATEGIAS_MEMORIA:
                    for seed in SEEDS:
                        teste_atual += 1
                        
                        print(f"[{teste_atual:4d}/{total_combinacoes}] {gerador} - Tipo {tipo} - V={numV} - {estrategia} - Seed={seed}")
                        
                        if gerador == 'Simples':
                            # Calcula número de arestas para simples
                            max_arestas = numV * (numV - 1) // 2
                            numA = random.randint(max(1, numV-1), max_arestas)
                            resultado = executa_teste_simples_escalabilidade(tipo, numV, numA, seed, estrategia)
                        else:  # Power-Law
                            # Gamma fixo para comparação
                            gamma = 2.5
                            resultado = executa_teste_powerlaw_escalabilidade(tipo, numV, gamma, seed, estrategia)
                        
                        if resultado:
                            resultados.append(resultado)
                            if resultado['limite_atingido']:
                                print(f"  ⚠️  Limite atingido - {resultado.get('erro', 'Erro desconhecido')}")
                            else:
                                print(f"  ✅ Sucesso - Tempo: {resultado['tempo_geracao']:.3f}s - Memória: {resultado['memoria_pico_mb']:.1f}MB")
                        else:
                            print(f"  ❌ Falha")
    
    end_time_experimento = time.time()
    tempo_total = end_time_experimento - start_time_experimento
    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_experimento4.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_experimento4.txt')
        with open(resumo_file, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 4: ANÁLISE DE ESCALABILIDADE E LIMITAÇÕES\n")
            f.write("=" * 60 + "\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de testes: {len(resultados)}/{total_combinacoes}\n")
            f.write(f"Taxa de sucesso: {len(resultados)/total_combinacoes*100:.1f}%\n")
            f.write(f"Tempo total: {tempo_total:.2f} segundos\n")
            f.write(f"Tempo médio por teste: {tempo_total/len(resultados):.3f} segundos\n\n")
            
            # Estatísticas por gerador
            for gerador in GERADORES:
                df_gerador = df[df['gerador'] == gerador]
                if len(df_gerador) > 0:
                    f.write(f"GERADOR: {gerador}\n")
                    f.write(f"  Testes: {len(df_gerador)}\n")
                    f.write(f"  Tempo médio: {df_gerador['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Memória pico média: {df_gerador['memoria_pico_mb'].mean():.1f}MB\n")
                    f.write(f"  Taxa de sucesso: {len(df_gerador[df_gerador['taxa_sucesso'] > 0])/len(df_gerador)*100:.1f}%\n\n")
            
            # Estatísticas por tamanho
            for tamanho in TAMANHOS:
                df_tamanho = df[df['numV'] == tamanho]
                if len(df_tamanho) > 0:
                    f.write(f"TAMANHO {tamanho}:\n")
                    f.write(f"  Testes: {len(df_tamanho)}\n")
                    f.write(f"  Tempo médio: {df_tamanho['tempo_geracao'].mean():.3f}s\n")
                    f.write(f"  Memória pico média: {df_tamanho['memoria_pico_mb'].mean():.1f}MB\n")
                    f.write(f"  Limites atingidos: {len(df_tamanho[df_tamanho['limite_atingido'] == True])}\n\n")
        
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
