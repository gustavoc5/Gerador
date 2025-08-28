#!/usr/bin/env python3
"""
EXECUTOR DE TODOS OS EXPERIMENTOS
Executa sequencialmente os experimentos Simples e Power-Law.
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def executar_experimento(script, args):
    """Executa um experimento específico."""
    print(f"\n{'='*80}")
    print(f"EXECUTANDO: {script}")
    print(f"ARGUMENTOS: {args}")
    print(f"{'='*80}")
    
    comando = [sys.executable, script] + args
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            print(f"[SUCESSO] {script} executado com sucesso!")
            if resultado.stdout:
                print("SAÍDA:")
                print(resultado.stdout)
        else:
            print(f"[ERRO] {script} falhou!")
            if resultado.stderr:
                print("ERRO:")
                print(resultado.stderr)
            return False
            
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao executar {script}: {e}")
        return False
    
    return True

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Executa todos os experimentos')
    parser.add_argument('--output_dir', default='./resultados_experimentos',
                       help='Diretório base de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste')
    parser.add_argument('--seeds', nargs='+', type=int, 
                       default=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                       help='Lista de seeds para teste')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa versão reduzida para teste rápido')
    parser.add_argument('--apenas_simples', action='store_true',
                       help='Executa apenas o experimento simples')
    parser.add_argument('--apenas_powerlaw', action='store_true',
                       help='Executa apenas o experimento power-law')
    
    args = parser.parse_args()
    
    # Cria diretório base
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXECUTOR DE TODOS OS EXPERIMENTOS")
    print("=" * 80)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Diretório base: {args.output_dir}")
    print(f"Máximo de vértices: {args.max_vertices}")
    print(f"Seeds: {args.seeds}")
    print(f"Teste rápido: {args.teste_rapido}")
    print("=" * 80)
    
    # Argumentos comuns
    args_comuns = [
        '--max_vertices', str(args.max_vertices),
        '--seeds'
    ] + [str(s) for s in args.seeds]
    
    if args.teste_rapido:
        args_comuns.append('--teste_rapido')
    
    sucessos = 0
    total_experimentos = 0
    
    # Executa experimento Simples
    if not args.apenas_powerlaw:
        total_experimentos += 1
        args_simples = args_comuns + [
            '--output_dir', os.path.join(args.output_dir, 'exp_simples_completo')
        ]
        
        if executar_experimento('simples.py', args_simples):
            sucessos += 1
    
    # Executa experimento Power-Law
    if not args.apenas_simples:
        total_experimentos += 1
        args_powerlaw = args_comuns + [
            '--output_dir', os.path.join(args.output_dir, 'exp_powerlaw_completo')
        ]
        
        if executar_experimento('powerlaw.py', args_powerlaw):
            sucessos += 1
    
    # Resumo final
    print("\n" + "=" * 80)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 80)
    print(f"Experimentos executados: {sucessos}/{total_experimentos}")
    print(f"Taxa de sucesso: {sucessos/total_experimentos*100:.1f}%")
    print(f"Data/Hora final: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if sucessos == total_experimentos:
        print("[SUCESSO] Todos os experimentos foram executados com sucesso!")
    else:
        print("[ATENÇÃO] Alguns experimentos falharam.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
