#!/usr/bin/env python3
"""
Script para concatenar resultados de experimentos individuais.
Organiza resultados por módulo e seed, criando arquivos agregados.
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from datetime import datetime

def concatenate_module_results(main_dir, module_name):
    """Concatena resultados de um módulo específico."""
    module_dir = os.path.join(main_dir, module_name)
    
    if not os.path.exists(module_dir):
        print(f"⚠️ Diretório do módulo {module_name} não encontrado: {module_dir}")
        return
    
    print(f"📦 Concatenando resultados do módulo: {module_name}")
    
    # Encontra todos os diretórios de seed
    seed_dirs = [d for d in os.listdir(module_dir) 
                if os.path.isdir(os.path.join(module_dir, d))]
    
    if not seed_dirs:
        print(f"⚠️ Nenhum diretório de seed encontrado em: {module_dir}")
        return
    
    # Para cada seed, concatena os arquivos
    for seed in seed_dirs:
        seed_path = os.path.join(module_dir, seed)
        txt_files = glob.glob(os.path.join(seed_path, "*.txt"))
        
        if not txt_files:
            print(f"⚠️ Nenhum arquivo .txt encontrado para seed {seed}")
            continue
        
        # Arquivo de saída concatenado
        output_file = os.path.join(main_dir, f"{module_name}_concatenated_{seed}.txt")
        
        print(f"  🌱 Seed {seed}: {len(txt_files)} arquivos -> {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Cabeçalho
            outfile.write(f"# Resultados concatenados do módulo {module_name}\n")
            outfile.write(f"# Seed: {seed}\n")
            outfile.write(f"# Arquivos: {len(txt_files)}\n")
            outfile.write(f"# Concatenado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write("=" * 80 + "\n\n")
            
            # Concatena cada arquivo
            for i, txt_file in enumerate(sorted(txt_files), 1):
                filename = os.path.basename(txt_file)
                outfile.write(f"# Arquivo {i}: {filename}\n")
                outfile.write("-" * 40 + "\n")
                
                try:
                    with open(txt_file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        if not content.endswith('\n'):
                            outfile.write('\n')
                except Exception as e:
                    outfile.write(f"ERRO ao ler arquivo: {e}\n")
                
                outfile.write("\n" + "=" * 80 + "\n\n")
    
    print(f"✅ Concatenação do módulo {module_name} concluída!")

def generate_summary(main_dir):
    """Gera um resumo dos experimentos executados."""
    summary_file = os.path.join(main_dir, "summary_experiments.txt")
    
    print(f"📊 Gerando resumo: {summary_file}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("RESUMO DOS EXPERIMENTOS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Diretório principal: {main_dir}\n\n")
        
        # Estatísticas por módulo
        for module in ['simples', 'powerlaw']:
            module_dir = os.path.join(main_dir, module)
            if not os.path.exists(module_dir):
                continue
            
            f.write(f"MÓDULO: {module.upper()}\n")
            f.write("-" * 30 + "\n")
            
            seed_dirs = [d for d in os.listdir(module_dir) 
                        if os.path.isdir(os.path.join(module_dir, d))]
            
            total_files = 0
            for seed in seed_dirs:
                seed_path = os.path.join(module_dir, seed)
                txt_files = glob.glob(os.path.join(seed_path, "*.txt"))
                total_files += len(txt_files)
                f.write(f"  Seed {seed}: {len(txt_files)} arquivos\n")
            
            f.write(f"  Total: {total_files} arquivos\n\n")
        
        # Arquivos concatenados
        f.write("ARQUIVOS CONCATENADOS\n")
        f.write("-" * 30 + "\n")
        concatenated_files = glob.glob(os.path.join(main_dir, "*_concatenated_*.txt"))
        for file in sorted(concatenated_files):
            filename = os.path.basename(file)
            f.write(f"  {filename}\n")
        
        f.write(f"\nTotal de arquivos concatenados: {len(concatenated_files)}\n")

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Concatena resultados de experimentos')
    parser.add_argument('--main_dir', default='./results',
                       help='Diretório principal com os resultados')
    parser.add_argument('--module', choices=['simples', 'powerlaw', 'both'], default='both',
                       help='Módulo(s) para concatenar')
    parser.add_argument('--summary', action='store_true',
                       help='Gera resumo dos experimentos')
    
    args = parser.parse_args()
    
    # Converte para caminho absoluto
    main_dir = os.path.abspath(args.main_dir)
    
    print(f"🚀 Concatenando resultados...")
    print(f"📁 Diretório principal: {main_dir}")
    print(f"📦 Módulo(s): {args.module}")
    print("=" * 60)
    
    # Verifica se o diretório existe
    if not os.path.exists(main_dir):
        print(f"❌ Diretório não encontrado: {main_dir}")
        print("💡 Execute os experimentos primeiro!")
        return
    
    # Concatena baseado no módulo escolhido
    if args.module in ['simples', 'both']:
        concatenate_module_results(main_dir, 'simples')
    
    if args.module in ['powerlaw', 'both']:
        concatenate_module_results(main_dir, 'powerlaw')
    
    # Gera resumo se solicitado
    if args.summary:
        generate_summary(main_dir)
    
    print("\n✅ Concatenação concluída!")
    print(f"📁 Resultados em: {main_dir}")

if __name__ == "__main__":
    main() 