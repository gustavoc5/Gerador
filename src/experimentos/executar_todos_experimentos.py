#!/usr/bin/env python3
"""
SCRIPT PRINCIPAL PARA EXECUTAR TODOS OS EXPERIMENTOS
Executa todos os experimentos definidos de forma sequencial ou paralela.

EXPERIMENTOS DISPONÍVEIS:
1. experimento_1_comparacao_geradores.py - Comparação fundamental entre geradores
2. experimento_2_parametros_simples.py - Parâmetros críticos do gerador simples
3. experimento_3_parametros_powerlaw.py - Parâmetros críticos do gerador power-law
4. experimento_4_escalabilidade.py - Análise de escalabilidade e limitações
5. experimento_5_replicacoes.py - Replicações com análise estatística

USO:
python executar_todos_experimentos.py --experimentos 1,2,3,4 --modo sequencial
python executar_todos_experimentos.py --experimentos 1,2 --modo paralelo --cores 4
python executar_todos_experimentos.py --experimentos 1 --teste_rapido
"""

import os
import sys
import subprocess
import time
import argparse
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

def executa_experimento(experimento_num, args):
    """Executa um experimento específico."""
    script_map = {
        1: "experimento_1_comparacao_geradores.py",
        2: "experimento_2_parametros_simples.py", 
        3: "experimento_3_parametros_powerlaw.py",
        4: "experimento_4_escalabilidade.py",
        5: "experimento_5_replicacoes.py"
    }
    
    script_name = script_map.get(experimento_num)
    if not script_name:
        print(f"❌ Experimento {experimento_num} não encontrado!")
        return False
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script {script_path} não encontrado!")
        return False
    
    # Constrói comando
    comando = [sys.executable, script_path]
    
    # Adiciona argumentos específicos
    if args.teste_rapido:
        comando.append("--teste_rapido")
    
    if args.output_dir:
        comando.extend(["--output_dir", args.output_dir])
    
    if args.max_vertices:
        comando.extend(["--max_vertices", str(args.max_vertices)])
    
    if args.seeds:
        comando.extend(["--seeds"] + [str(s) for s in args.seeds])
    
    print(f"🚀 Executando Experimento {experimento_num}: {script_name}")
    print(f"📝 Comando: {' '.join(comando)}")
    print("-" * 60)
    
    try:
        start_time = time.time()
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=3600)  # 1 hora timeout
        end_time = time.time()
        
        if resultado.returncode == 0:
            print(f"✅ Experimento {experimento_num} concluído com sucesso!")
            print(f"⏱️  Tempo: {end_time - start_time:.2f} segundos")
            if resultado.stdout:
                print("📤 Saída:")
                print(resultado.stdout[-500:])  # Últimas 500 caracteres
            return True
        else:
            print(f"❌ Experimento {experimento_num} falhou!")
            print(f"🔍 Erro: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Experimento {experimento_num} excedeu o tempo limite (1 hora)")
        return False
    except Exception as e:
        print(f"💥 Erro ao executar experimento {experimento_num}: {e}")
        return False

def executa_sequencial(experimentos, args):
    """Executa experimentos de forma sequencial."""
    print("🔄 MODO SEQUENCIAL")
    print("=" * 60)
    
    resultados = {}
    start_time_total = time.time()
    
    for exp_num in experimentos:
        print(f"\n{'='*20} EXPERIMENTO {exp_num} {'='*20}")
        sucesso = executa_experimento(exp_num, args)
        resultados[exp_num] = sucesso
        print(f"{'='*60}\n")
    
    end_time_total = time.time()
    tempo_total = end_time_total - start_time_total
    
    # Resumo
    print("📊 RESUMO DA EXECUÇÃO SEQUENCIAL")
    print("=" * 60)
    for exp_num, sucesso in resultados.items():
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        print(f"Experimento {exp_num}: {status}")
    
    print(f"\n⏱️  Tempo total: {tempo_total:.2f} segundos")
    print(f"🎯 Taxa de sucesso: {sum(resultados.values())}/{len(resultados)} ({sum(resultados.values())/len(resultados)*100:.1f}%)")
    
    return resultados

def executa_paralelo(experimentos, args, num_cores):
    """Executa experimentos de forma paralela."""
    print(f"🔄 MODO PARALELO (cores: {num_cores})")
    print("=" * 60)
    
    resultados = {}
    start_time_total = time.time()
    
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Submete todos os experimentos
        future_to_exp = {executor.submit(executa_experimento, exp_num, args): exp_num 
                        for exp_num in experimentos}
        
        # Coleta resultados conforme completam
        for future in as_completed(future_to_exp):
            exp_num = future_to_exp[future]
            try:
                sucesso = future.result()
                resultados[exp_num] = sucesso
                status = "✅ SUCESSO" if sucesso else "❌ FALHA"
                print(f"Experimento {exp_num}: {status}")
            except Exception as e:
                print(f"💥 Erro no experimento {exp_num}: {e}")
                resultados[exp_num] = False
    
    end_time_total = time.time()
    tempo_total = end_time_total - start_time_total
    
    # Resumo
    print("\n📊 RESUMO DA EXECUÇÃO PARALELA")
    print("=" * 60)
    for exp_num, sucesso in resultados.items():
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        print(f"Experimento {exp_num}: {status}")
    
    print(f"\n⏱️  Tempo total: {tempo_total:.2f} segundos")
    print(f"🎯 Taxa de sucesso: {sum(resultados.values())}/{len(resultados)} ({sum(resultados.values())/len(resultados)*100:.1f}%)")
    
    return resultados

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Executa todos os experimentos de geração de grafos')
    parser.add_argument('--experimentos', nargs='+', type=int, default=[1,2,3,4,5],
                       help='Lista de experimentos para executar (1-5)')
    parser.add_argument('--modo', choices=['sequencial', 'paralelo'], default='sequencial',
                       help='Modo de execução')
    parser.add_argument('--cores', type=int, default=4,
                       help='Número de cores para execução paralela')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa versões rápidas dos experimentos')
    parser.add_argument('--output_dir', default='./resultados_experimentos',
                       help='Diretório base de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para testes')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000],
                       help='Lista de seeds para testes')
    
    args = parser.parse_args()
    
    # Valida experimentos
    experimentos_validos = [1, 2, 3, 4, 5]
    experimentos = [exp for exp in args.experimentos if exp in experimentos_validos]
    
    if not experimentos:
        print("❌ Nenhum experimento válido especificado!")
        print(f"Experimentos válidos: {experimentos_validos}")
        return
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("🎯 EXECUTOR DE EXPERIMENTOS - GERADOR DE GRAFOS")
    print("=" * 60)
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔬 Experimentos: {experimentos}")
    print(f"⚙️  Modo: {args.modo}")
    if args.modo == 'paralelo':
        print(f"🖥️  Cores: {args.cores}")
    print(f"📁 Diretório: {args.output_dir}")
    print(f"🔢 Máximo vértices: {args.max_vertices}")
    print(f"🌱 Seeds: {args.seeds}")
    if args.teste_rapido:
        print("⚡ MODO TESTE RÁPIDO ATIVADO")
    print("=" * 60)
    
    # Executa experimentos
    if args.modo == 'sequencial':
        resultados = executa_sequencial(experimentos, args)
    else:  # paralelo
        resultados = executa_paralelo(experimentos, args, args.cores)
    
    # Salva log final
    log_file = os.path.join(args.output_dir, f"log_execucao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("LOG DE EXECUÇÃO DOS EXPERIMENTOS\n")
        f.write("=" * 40 + "\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Experimentos: {experimentos}\n")
        f.write(f"Modo: {args.modo}\n")
        f.write(f"Teste rápido: {args.teste_rapido}\n\n")
        
        for exp_num, sucesso in resultados.items():
            status = "SUCESSO" if sucesso else "FALHA"
            f.write(f"Experimento {exp_num}: {status}\n")
        
        f.write(f"\nTaxa de sucesso: {sum(resultados.values())}/{len(resultados)} ({sum(resultados.values())/len(resultados)*100:.1f}%)\n")
    
    print(f"\n📋 Log salvo em: {log_file}")
    print("🎉 Execução finalizada!")

if __name__ == "__main__":
    main()
