#!/usr/bin/env python3
"""
Script para análise dos resultados de testes do gerador de grafos.
"""

import pandas as pd
import numpy as np

def analisa_resultados(arquivo_csv):
    """Analisa os resultados de um arquivo CSV de testes."""
    
    try:
        df = pd.read_csv(arquivo_csv)
    except FileNotFoundError:
        print(f"❌ Arquivo {arquivo_csv} não encontrado!")
        return
    
    print("=" * 60)
    print("📊 ANÁLISE ESTATÍSTICA DOS RESULTADOS")
    print("=" * 60)
    
    # Estatísticas gerais
    total_execucoes = len(df)
    sucessos = (df['tipo_ok'] == True).sum()
    taxa_sucesso = (sucessos / total_execucoes) * 100
    
    print(f"📈 Total de execuções: {total_execucoes}")
    print(f"✅ Sucessos na detecção: {sucessos}")
    print(f"❌ Falhas na detecção: {total_execucoes - sucessos}")
    print(f"🎯 Taxa de sucesso: {taxa_sucesso:.1f}%")
    print()
    
    # Análise por tipo
    print("🔍 DETALHAMENTO POR TIPO DE GRAFO:")
    print("-" * 40)
    
    tipos_analisados = []
    for tipo in sorted(df['tipo'].unique()):
        subset = df[df['tipo'] == tipo]
        sucessos_tipo = (subset['tipo_ok'] == True).sum()
        total_tipo = len(subset)
        taxa_tipo = (sucessos_tipo / total_tipo) * 100
        descricao = subset['descricao'].iloc[0]
        
        tipos_analisados.append({
            'tipo': tipo,
            'descricao': descricao,
            'sucessos': sucessos_tipo,
            'total': total_tipo,
            'taxa': taxa_tipo
        })
        
        status = "✅" if taxa_tipo == 100 else "⚠️" if taxa_tipo >= 90 else "❌"
        print(f"{status} Tipo {tipo:2d} ({descricao:20s}): {sucessos_tipo:2d}/{total_tipo:2d} = {taxa_tipo:5.1f}%")
    
    print()
    
    # Métricas de performance
    print("⚡ MÉTRICAS DE PERFORMANCE:")
    print("-" * 40)
    
    vertices = df['vertices'].iloc[0]
    tempo_medio = df['tempo_geracao_s'].mean()
    tempo_max = df['tempo_geracao_s'].max()
    arestas_medio = df['num_arestas'].mean()
    arestas_min = df['num_arestas'].min()
    arestas_max = df['num_arestas'].max()
    
    print(f"🕐 Tempo médio de geração: {tempo_medio:.4f}s")
    print(f"⏱️  Tempo máximo de geração: {tempo_max:.4f}s")
    print(f"📊 Vértices por grafo: {vertices}")
    print(f"🔗 Arestas médias: {arestas_medio:.0f}")
    print(f"🔗 Arestas (mín/máx): {arestas_min}/{arestas_max}")
    print()
    
    # Análise de falhas
    if sucessos < total_execucoes:
        print("🚨 ANÁLISE DE FALHAS:")
        print("-" * 40)
        falhas = df[df['tipo_ok'] == False]
        
        for _, falha in falhas.iterrows():
            print(f"❌ Tipo {falha['tipo']} (execução {falha['execucao']}): "
                  f"solicitado={falha['tipo']}, detectado={falha['tipo_detectado']}")
    
    # Resumo final
    print("=" * 60)
    print("📋 RESUMO FINAL:")
    print("=" * 60)
    
    if taxa_sucesso == 100:
        print("🎉 PERFEITO! 100% de sucesso na detecção de tipos!")
    elif taxa_sucesso >= 95:
        print("✅ EXCELENTE! Taxa de sucesso muito alta!")
    elif taxa_sucesso >= 90:
        print("👍 BOM! Taxa de sucesso satisfatória.")
    else:
        print("⚠️  ATENÇÃO! Taxa de sucesso abaixo do esperado.")
    
    print(f"📊 Taxa geral: {taxa_sucesso:.1f}%")
    
    # Verifica se todos os tipos têm 100% de sucesso
    tipos_perfeitos = sum(1 for t in tipos_analisados if t['taxa'] == 100)
    total_tipos = len(tipos_analisados)
    
    if tipos_perfeitos == total_tipos:
        print("🎯 Todos os tipos de grafos estão sendo detectados corretamente!")
    else:
        print(f"⚠️  {total_tipos - tipos_perfeitos} tipo(s) ainda têm problemas de detecção.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "teste_grande.csv"
    
    analisa_resultados(arquivo) 