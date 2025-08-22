#!/usr/bin/env python3
"""
Script para gerar comandos de execução paralela de experimentos.
Gera comandos para os módulos simples e powerlaw, organizando saída por seed.
"""

import os
import sys
import random
from pathlib import Path

def gera_comandos_simples(main_dir, seeds, vertices_list, tipos_list, execucoes_por_combinacao=1):
    """Gera comandos para o módulo simples."""
    comandos = []
    
    for seed in seeds:
        # Cria diretório para o seed
        seed_dir = os.path.join(main_dir, "simples", str(seed))
        comandos.append(f"mkdir -p {seed_dir}")
        
        for vertices in vertices_list:
            for tipo in tipos_list:
                for execucao in range(execucoes_por_combinacao):
                    # Calcula número de arestas baseado na densidade
                    max_arestas = vertices * (vertices - 1) // 2
                    num_arestas = random.randint(max(1, vertices-1), max_arestas)
                    
                    # Nome do arquivo de saída
                    output_file = f"simples_t{tipo}_v{vertices}_a{num_arestas}_s{seed}_e{execucao}.txt"
                    output_path = os.path.join(seed_dir, output_file)
                    
                    # Comando completo
                    comando = (
                        f"python src/simples/test_simples.py "
                        f"--seed {seed} "
                        f"--output_txt {output_path} "
                        f"&> {output_path}"
                    )
                    comandos.append(comando)
    
    return comandos

def gera_comandos_powerlaw(main_dir, seeds, vertices_list, tipos_list, execucoes_por_combinacao=1):
    """Gera comandos para o módulo powerlaw."""
    comandos = []
    
    for seed in seeds:
        # Cria diretório para o seed
        seed_dir = os.path.join(main_dir, "powerlaw", str(seed))
        comandos.append(f"mkdir -p {seed_dir}")
        
        for vertices in vertices_list:
            for tipo in tipos_list:
                for execucao in range(execucoes_por_combinacao):
                    # Gama aleatório no intervalo válido (2.0 a 3.5)
                    gamma = round(random.uniform(2.0, 3.5), 2)
                    
                    # Nome do arquivo de saída
                    output_file = f"powerlaw_t{tipo}_v{vertices}_g{gamma}_s{seed}_e{execucao}.txt"
                    output_path = os.path.join(seed_dir, output_file)
                    
                    # Comando completo
                    comando = (
                        f"python src/powerlaw/test_pwl.py "
                        f"--seed {seed} "
                        f"--output_txt {output_path} "
                        f"&> {output_path}"
                    )
                    comandos.append(comando)
    
    return comandos

def gera_comandos_completos(main_dir, seeds, vertices_list, tipos_list, execucoes_por_combinacao=1):
    """Gera comandos para ambos os módulos."""
    comandos = []
    
    # Comandos para simples
    comandos.extend(gera_comandos_simples(main_dir, seeds, vertices_list, tipos_list, execucoes_por_combinacao))
    
    # Comandos para powerlaw
    comandos.extend(gera_comandos_powerlaw(main_dir, seeds, vertices_list, tipos_list, execucoes_por_combinacao))
    
    return comandos

def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gera comandos para execução paralela de experimentos')
    parser.add_argument('--main_dir', default='/home/user/projects/graph_generation/results',
                       help='Diretório principal para resultados')
    parser.add_argument('--seeds', nargs='+', type=int, default=[123, 456, 789],
                       help='Lista de seeds para experimentos')
    parser.add_argument('--vertices', nargs='+', type=int, default=[10, 20, 50],
                       help='Lista de números de vértices')
    parser.add_argument('--tipos', nargs='+', type=int, default=[0, 1, 2, 3, 4, 5],
                       help='Lista de tipos de grafo (0-5)')
    parser.add_argument('--execucoes', type=int, default=1,
                       help='Número de execuções por combinação')
    parser.add_argument('--modulo', choices=['simples', 'powerlaw', 'ambos'], default='ambos',
                       help='Módulo(s) para gerar comandos')
    parser.add_argument('--output_file', default='comandos_experimentos.sh',
                       help='Arquivo de saída com os comandos')
    
    args = parser.parse_args()
    
    # Gera comandos baseado no módulo escolhido
    if args.modulo == 'simples':
        comandos = gera_comandos_simples(args.main_dir, args.seeds, args.vertices, args.tipos, args.execucoes)
    elif args.modulo == 'powerlaw':
        comandos = gera_comandos_powerlaw(args.main_dir, args.seeds, args.vertices, args.tipos, args.execucoes)
    else:  # ambos
        comandos = gera_comandos_completos(args.main_dir, args.seeds, args.vertices, args.tipos, args.execucoes)
    
    # Salva comandos em arquivo
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# Comandos gerados automaticamente para execução paralela\n")
        f.write(f"# Total de comandos: {len(comandos)}\n")
        f.write(f"# Módulo: {args.modulo}\n")
        f.write(f"# Seeds: {args.seeds}\n")
        f.write(f"# Vértices: {args.vertices}\n")
        f.write(f"# Tipos: {args.tipos}\n")
        f.write(f"# Execuções por combinação: {args.execucoes}\n")
        f.write("\n")
        
        for i, comando in enumerate(comandos, 1):
            f.write(f"# Comando {i}\n")
            f.write(f"{comando}\n")
            f.write("\n")
    
    # Torna o arquivo executável
    os.chmod(args.output_file, 0o755)
    
    print(f"✅ Gerados {len(comandos)} comandos em: {args.output_file}")
    print(f"📁 Diretório principal: {args.main_dir}")
    print(f"🌱 Seeds: {args.seeds}")
    print(f"📊 Vértices: {args.vertices}")
    print(f"🎯 Tipos: {args.tipos}")
    print(f"🔄 Execuções por combinação: {args.execucoes}")
    print(f"📦 Módulo: {args.modulo}")
    
    # Estatísticas
    total_experimentos = len(args.seeds) * len(args.vertices) * len(args.tipos) * args.execucoes
    if args.modulo == 'ambos':
        total_experimentos *= 2
    
    print(f"\n📈 Total de experimentos: {total_experimentos}")
    print(f"💡 Para executar: bash {args.output_file}")

if __name__ == "__main__":
    main() 