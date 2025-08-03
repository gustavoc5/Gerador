#!/usr/bin/env python3
"""
Script para concatenar resultados dos experimentos.
Organiza os resultados por seed e módulo.
"""

import os
import glob
import argparse
from datetime import datetime

def concatenate_module_results(results_dir, module_name, seeds):
    """Concatena resultados de um módulo específico."""
    module_dir = os.path.join(results_dir, module_name)
    if not os.path.exists(module_dir):
        print(f"❌ Diretório não encontrado: {module_dir}")
        return
    
    print(f"📁 Concatenando resultados do módulo: {module_name}")
    
    # Para cada seed, concatena todos os arquivos
    for seed in seeds:
        seed_dir = os.path.join(module_dir, str(seed))
        if not os.path.exists(seed_dir):
            continue
        
        # Encontra todos os arquivos .txt no diretório da seed
        files = glob.glob(os.path.join(seed_dir, "*.txt"))
        if not files:
            continue
        
        # Arquivo de saída concatenado
        output_file = os.path.join(results_dir, f"{module_name}_concatenated_{seed}.txt")
        
        print(f"  🔄 Seed {seed}: {len(files)} arquivos -> {output_file}")
        
        with open(output_file, 'w') as outfile:
            # Escreve cabeçalho
            outfile.write(f"# Resultados concatenados - Módulo {module_name}\n")
            outfile.write(f"# Seed: {seed}\n")
            outfile.write(f"# Arquivos: {len(files)}\n")
            outfile.write(f"# Gerado em: {datetime.now()}\n")
            outfile.write(f"{'='*60}\n\n")
            
            # Concatena cada arquivo
            for file_path in sorted(files):
                filename = os.path.basename(file_path)
                outfile.write(f"# Arquivo: {filename}\n")
                outfile.write(f"{'='*40}\n")
                
                try:
                    with open(file_path, 'r') as infile:
                        content = infile.read()
                        outfile.write(content)
                        if not content.endswith('\n'):
                            outfile.write('\n')
                except Exception as e:
                    outfile.write(f"❌ Erro ao ler arquivo: {e}\n")
                
                outfile.write(f"\n{'='*40}\n\n")

def generate_summary(results_dir, module_name, seeds):
    """Gera um resumo dos experimentos."""
    module_dir = os.path.join(results_dir, module_name)
    if not os.path.exists(module_dir):
        return
    
    summary_file = os.path.join(results_dir, f"{module_name}_summary.txt")
    
    print(f"📊 Gerando resumo: {summary_file}")
    
    with open(summary_file, 'w') as summary:
        summary.write(f"# Resumo dos Experimentos - Módulo {module_name}\n")
        summary.write(f"# Gerado em: {datetime.now()}\n")
        summary.write(f"{'='*60}\n\n")
        
        total_experiments = 0
        successful_seeds = 0
        
        for seed in seeds:
            seed_dir = os.path.join(module_dir, str(seed))
            if not os.path.exists(seed_dir):
                continue
            
            files = glob.glob(os.path.join(seed_dir, "*.txt"))
            if files:
                successful_seeds += 1
                total_experiments += len(files)
                
                summary.write(f"Seed {seed}:\n")
                summary.write(f"  Arquivos: {len(files)}\n")
                
                # Analisa tamanhos dos arquivos
                sizes = [os.path.getsize(f) for f in files]
                summary.write(f"  Tamanho total: {sum(sizes)} bytes\n")
                summary.write(f"  Tamanho médio: {sum(sizes)/len(sizes):.0f} bytes\n")
                summary.write(f"  Maior arquivo: {max(sizes)} bytes\n")
                summary.write(f"  Menor arquivo: {min(sizes)} bytes\n\n")
        
        summary.write(f"{'='*60}\n")
        summary.write(f"Total de seeds com sucesso: {successful_seeds}/{len(seeds)}\n")
        summary.write(f"Total de experimentos: {total_experiments}\n")
        summary.write(f"Taxa de sucesso: {(successful_seeds/len(seeds)*100):.1f}%\n")

def main():
    parser = argparse.ArgumentParser(description="Concatena resultados dos experimentos")
    parser.add_argument("--results_dir", default="results", 
                       help="Diretório com os resultados")
    parser.add_argument("--modules", nargs="+", 
                       default=["simples", "powerlaw"], 
                       help="Módulos a processar")
    parser.add_argument("--seeds", nargs="+", type=int,
                       default=[270001, 341099, 160812, 713978, 705319, 219373, 255486, 135848, 142095, 571618],
                       help="Seeds a processar")
    parser.add_argument("--summary", action="store_true",
                       help="Gera resumo dos experimentos")
    
    args = parser.parse_args()
    
    # Converte para caminho absoluto
    results_dir = os.path.abspath(args.results_dir)
    
    print(f"🚀 Concatenando resultados")
    print(f"📁 Diretório: {results_dir}")
    print(f"📊 Módulos: {args.modules}")
    print(f"🎲 Seeds: {len(args.seeds)}")
    print(f"{'='*60}")
    
    # Processa cada módulo
    for module in args.modules:
        concatenate_module_results(results_dir, module, args.seeds)
        
        if args.summary:
            generate_summary(results_dir, module, args.seeds)
    
    print(f"\n✅ Concatenação concluída!")
    print(f"📁 Resultados em: {results_dir}")

if __name__ == "__main__":
    main() 