#!/usr/bin/env python3
"""
Script para gerar chamadas de experimentos independentes.
Permite paralelismo evitando condições de corrida.
Cada experimento tem sua própria saída baseada na seed.
"""

import os
import sys
import argparse
from datetime import datetime

def generate_simples_experiments(seeds, sizes, execucoes, main_dir, output_file):
    """Gera chamadas para experimentos do módulo simples."""
    script_path = os.path.join(main_dir, "simples", "test_simples.py")
    
    with open(output_file, 'w') as f:
        for seed in seeds:
            for size in sizes:
                for execucao in range(execucoes):
                    # Cria diretório baseado na seed
                    seed_dir = os.path.join(main_dir, "results", "simples", str(seed))
                    
                    # Nome do arquivo de saída único
                    output_filename = f"size{size}_exec{execucao}.txt"
                    output_path = os.path.join(seed_dir, output_filename)
                    
                    # Comando completo
                    cmd = f"python {script_path} 1 {size} &> {output_path}"
                    
                    # Adiciona comando para criar diretório se não existir
                    mkdir_cmd = f"mkdir -p {seed_dir}"
                    f.write(f"{mkdir_cmd}\n")
                    f.write(f"{cmd}\n")

def generate_powerlaw_experiments(seeds, sizes, execucoes, main_dir, output_file):
    """Gera chamadas para experimentos do módulo powerlaw."""
    script_path = os.path.join(main_dir, "powerlaw", "test_pwl.py")
    
    with open(output_file, 'w') as f:
        for seed in seeds:
            for size in sizes:
                for execucao in range(execucoes):
                    # Cria diretório baseado na seed
                    seed_dir = os.path.join(main_dir, "results", "powerlaw", str(seed))
                    
                    # Nome do arquivo de saída único
                    output_filename = f"size{size}_exec{execucao}.txt"
                    output_path = os.path.join(seed_dir, output_filename)
                    
                    # Comando completo
                    cmd = f"python {script_path} 1 {size} &> {output_path}"
                    
                    # Adiciona comando para criar diretório se não existir
                    mkdir_cmd = f"mkdir -p {seed_dir}"
                    f.write(f"{mkdir_cmd}\n")
                    f.write(f"{cmd}\n")

def generate_combined_experiments(seeds, sizes, execucoes, main_dir, output_file):
    """Gera chamadas para ambos os módulos."""
    simples_path = os.path.join(main_dir, "simples", "test_simples.py")
    powerlaw_path = os.path.join(main_dir, "powerlaw", "test_pwl.py")
    
    with open(output_file, 'w') as f:
        for seed in seeds:
            for size in sizes:
                for execucao in range(execucoes):
                    # Diretórios baseados na seed
                    simples_dir = os.path.join(main_dir, "results", "simples", str(seed))
                    powerlaw_dir = os.path.join(main_dir, "results", "powerlaw", str(seed))
                    
                    # Arquivos de saída únicos
                    simples_output = os.path.join(simples_dir, f"size{size}_exec{execucao}.txt")
                    powerlaw_output = os.path.join(powerlaw_dir, f"size{size}_exec{execucao}.txt")
                    
                    # Comandos
                    mkdir_simples = f"mkdir -p {simples_dir}"
                    mkdir_powerlaw = f"mkdir -p {powerlaw_dir}"
                    cmd_simples = f"python {simples_path} 1 {size} &> {simples_output}"
                    cmd_powerlaw = f"python {powerlaw_path} 1 {size} &> {powerlaw_output}"
                    
                    f.write(f"{mkdir_simples}\n")
                    f.write(f"{mkdir_powerlaw}\n")
                    f.write(f"{cmd_simples}\n")
                    f.write(f"{cmd_powerlaw}\n")

def main():
    parser = argparse.ArgumentParser(description="Gera chamadas de experimentos para paralelismo")
    parser.add_argument("--module", choices=["simples", "powerlaw", "both"], 
                       default="both", help="Módulo(s) a executar")
    parser.add_argument("--main_dir", default=os.getcwd(), 
                       help="Diretório principal do projeto")
    parser.add_argument("--seeds", nargs="+", type=int, 
                       default=[270001, 341099, 160812, 713978, 705319, 219373, 255486, 135848, 142095, 571618],
                       help="Lista de seeds para os experimentos")
    parser.add_argument("--sizes", nargs="+", type=int, 
                       default=[100, 500, 1000], help="Tamanhos dos grafos")
    parser.add_argument("--execucoes", type=int, default=5, 
                       help="Número de execuções por configuração")
    parser.add_argument("--output", default=None, 
                       help="Arquivo de saída (padrão: experiments_<timestamp>.sh)")
    
    args = parser.parse_args()
    
    # Define arquivo de saída padrão
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"experiments_{args.module}_{timestamp}.sh"
    
    # Converte para caminho absoluto
    main_dir = os.path.abspath(args.main_dir)
    output_file = os.path.abspath(args.output)
    
    print(f"🚀 Gerando experimentos para módulo: {args.module}")
    print(f"📁 Diretório principal: {main_dir}")
    print(f"📊 Seeds: {len(args.seeds)} seeds")
    print(f"📏 Tamanhos: {args.sizes}")
    print(f"🔄 Execuções: {args.execucoes}")
    print(f"📄 Arquivo de saída: {output_file}")
    
    # Calcula total de experimentos
    total_experiments = len(args.seeds) * len(args.sizes) * args.execucoes
    if args.module == "both":
        total_experiments *= 2
    
    print(f"🎯 Total de experimentos: {total_experiments}")
    print(f"{'='*60}")
    
    # Gera os experimentos
    if args.module == "simples":
        generate_simples_experiments(args.seeds, args.sizes, args.execucoes, main_dir, output_file)
    elif args.module == "powerlaw":
        generate_powerlaw_experiments(args.seeds, args.sizes, args.execucoes, main_dir, output_file)
    else:  # both
        generate_combined_experiments(args.seeds, args.sizes, args.execucoes, main_dir, output_file)
    
    print(f"✅ Script gerado com sucesso: {output_file}")
    print(f"📋 Para executar: bash {output_file}")
    print(f"🔄 Para executar em paralelo: parallel -j <num_cores> < {output_file}")

if __name__ == "__main__":
    main() 