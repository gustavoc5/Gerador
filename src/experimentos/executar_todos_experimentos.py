#!/usr/bin/env python3
"""
EXECUTAR TODOS OS EXPERIMENTOS
Script para execução automatizada de todos os experimentos principais.
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def executar_experimento(script, args=""):
    """Executa um experimento e retorna o status."""
    comando = f"python {script} {args}".strip()
    print(f"\n{'='*80}")
    print(f"EXECUTANDO: {comando}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        tempo_execucao = time.time() - start_time
        
        if resultado.returncode == 0:
            print(f"✅ SUCESSO - Tempo: {tempo_execucao:.2f}s")
            print("Saída:")
            print(resultado.stdout)
            return True, tempo_execucao
        else:
            print(f"❌ ERRO - Tempo: {tempo_execucao:.2f}s")
            print("Erro:")
            print(resultado.stderr)
            return False, tempo_execucao
            
    except Exception as e:
        tempo_execucao = time.time() - start_time
        print(f"❌ EXCEÇÃO - Tempo: {tempo_execucao:.2f}s")
        print(f"Erro: {e}")
        return False, tempo_execucao

def main():
    """Função principal."""
    
    print("🧪 SISTEMA DE EXPERIMENTOS - EXECUÇÃO AUTOMATIZADA")
    print("=" * 80)
    
    # Configuração dos experimentos
    experimentos = {
        1: {
            "nome": "Simples Completo",
            "script": "experimento_simples_completo.py",
            "descricao": "Todas as métricas do gerador Simples (2.700 testes)"
        },
        2: {
            "nome": "Power-Law Completo", 
            "script": "experimento_powerlaw_completo.py",
            "descricao": "Todas as métricas do gerador Power-Law (180 testes)"
        }
    }
    
    # Verifica argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--teste_rapido":
        modo_teste = True
        print("🔬 MODO TESTE RÁPIDO ATIVADO")
    else:
        modo_teste = False
        print("🚀 MODO EXECUÇÃO COMPLETA")
    
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Diretório: {os.getcwd()}")
    print("=" * 80)
    
    # Lista experimentos disponíveis
    print("\n📋 EXPERIMENTOS DISPONÍVEIS:")
    for id_exp, info in experimentos.items():
        print(f"  {id_exp}. {info['nome']}")
        print(f"     {info['descricao']}")
    print()
    
    # Executa experimentos
    resultados = {}
    tempo_total = 0
    
    for id_exp, info in experimentos.items():
        print(f"\n🎯 EXECUTANDO EXPERIMENTO {id_exp}: {info['nome']}")
        
        # Prepara argumentos
        args = "--teste_rapido" if modo_teste else ""
        
        # Executa experimento
        sucesso, tempo = executar_experimento(info['script'], args)
        
        resultados[id_exp] = {
            'nome': info['nome'],
            'sucesso': sucesso,
            'tempo': tempo
        }
        
        tempo_total += tempo
        
        if sucesso:
            print(f"✅ {info['nome']} - CONCLUÍDO em {tempo:.2f}s")
        else:
            print(f"❌ {info['nome']} - FALHOU em {tempo:.2f}s")
    
    # Relatório final
    print(f"\n{'='*80}")
    print("📊 RELATÓRIO FINAL")
    print(f"{'='*80}")
    
    sucessos = sum(1 for r in resultados.values() if r['sucesso'])
    total = len(resultados)
    
    print(f"📈 RESUMO:")
    print(f"  Total de experimentos: {total}")
    print(f"  Sucessos: {sucessos}")
    print(f"  Falhas: {total - sucessos}")
    print(f"  Taxa de sucesso: {sucessos/total*100:.1f}%")
    print(f"  Tempo total: {tempo_total:.2f}s")
    
    print(f"\n📋 DETALHES:")
    for id_exp, resultado in resultados.items():
        status = "✅ SUCESSO" if resultado['sucesso'] else "❌ FALHA"
        print(f"  {id_exp}. {resultado['nome']}: {status} ({resultado['tempo']:.2f}s)")
    
    # Verifica diretórios de saída
    print(f"\n📁 DIRETÓRIOS DE SAÍDA:")
    diretorios_saida = [
        "resultados_experimentos/exp_simples_completo",
        "resultados_experimentos/exp_powerlaw_completo"
    ]
    
    for diretorio in diretorios_saida:
        if os.path.exists(diretorio):
            arquivos = len([f for f in os.listdir(diretorio) if f.endswith('.csv')])
            print(f"  ✅ {diretorio}/ ({arquivos} arquivos CSV)")
        else:
            print(f"  ❌ {diretorio}/ (não encontrado)")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"  1. Verificar arquivos de saída em resultados_experimentos/")
    print(f"  2. Analisar dados com ferramentas de análise")
    print(f"  3. Gerar visualizações e relatórios")
    
    if sucessos == total:
        print(f"\n🎉 TODOS OS EXPERIMENTOS CONCLUÍDOS COM SUCESSO!")
    else:
        print(f"\n⚠️  ALGUNS EXPERIMENTOS FALHARAM. Verifique os erros acima.")
    
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
