#!/usr/bin/env python3
"""
GERADOR DE COMANDOS PARA EXECUÇÃO PARALELA DOS EXPERIMENTOS

Este script gera comandos para execução paralela dos experimentos, onde cada execução:
- É independente
- Salva em arquivo separado baseado na seed
- Usa caminhos absolutos
- Evita condições de corrida
- Permite paralelização

ESTRATÉGIA:
- Para cada seed, cria um diretório separado
- Cada execução salva em arquivo único baseado na seed
- No final, todos os arquivos são concatenados
"""

import os
import sys
import argparse
from pathlib import Path

def join_path(base: str, *parts: str) -> str:
    """Concatena caminhos respeitando POSIX quando base inicia com '/'."""
    if base.startswith('/'):
        cleaned = [base.rstrip('/')]
        cleaned += [p.strip('/\\') for p in parts]
        return '/'.join(cleaned)
    return os.path.join(base, *parts)

def gerar_comandos_simples(main_dir, seeds, output_file):
    """
    Gera comandos para o experimento Simples Completo.
    """
    print("Gerando comandos para experimento Simples Completo...")
    
    # Configurações do experimento
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]
    TAMANHOS = [100, 1000, 10000, 100000, 1000000]
    PREFERENCIAS_DENSIDADE = [0, 1, 2]  # 0=Sem preferência, 1=Esparso, 2=Denso
    NUM_COMPONENTES = [0, 1]  # 0=Aleatório, 1=Conexo
    
    # Script Python
    script_path = join_path(main_dir, "src/experimentos/simples.py")
    
    comandos = []
    
    for seed in seeds:
        # Cria diretório para esta seed
        seed_dir = join_path(main_dir, f"resultados_experimentos/exp_simples_completo/{seed}")
        comandos.append(f"mkdir -p {seed_dir}")
        
        # Gera comando para esta seed
        output_path = join_path(seed_dir, "resultados.csv")
        
        comando = (
            f"mkdir -p {seed_dir} && timeout --signal=SIGKILL 2h "
            f"bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; "
            f"python3 -u {script_path} --output_dir {seed_dir} --seeds {seed} --max_vertices 10000 &> {seed_dir}/log.txt'"
        )
        
        comandos.append(comando)
    
    # Salva comandos no arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# COMANDOS PARA EXECUÇÃO PARALELA - EXPERIMENTO SIMPLES COMPLETO\n")
        f.write(f"# Total de seeds: {len(seeds)}\n")
        f.write(f"# Total de testes por seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES)}\n")
        f.write(f"# Total de grafos por seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES) * 50}\n\n")
        
        for comando in comandos:
            f.write(comando + "\n")
    
    print(f"Comandos salvos em: {output_file}")
    print(f"Total de comandos gerados: {len(comandos)}")

def gerar_comandos_powerlaw(main_dir, seeds, output_file):
    """
    Gera comandos para o experimento Power-Law Completo.
    """
    print("Gerando comandos para experimento Power-Law Completo...")
    
    # Configurações do experimento
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]
    TAMANHOS = [100, 1000, 10000, 100000, 1000000]
    CATEGORIAS_GAMMA = ['denso', 'moderado', 'esparso']
    
    # Script Python
    script_path = join_path(main_dir, "src/experimentos/power_law.py")
    
    comandos = []
    
    for seed in seeds:
        # Cria diretório para esta seed
        seed_dir = join_path(main_dir, f"resultados_experimentos/exp_powerlaw_completo/{seed}")
        comandos.append(f"mkdir -p {seed_dir}")
        
        # Gera comando para esta seed
        output_path = join_path(seed_dir, "resultados.csv")
        
        comando = (
            f"mkdir -p {seed_dir} && timeout --signal=SIGKILL 2h "
            f"bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; "
            f"python3 -u {script_path} --output_dir {seed_dir} --seeds {seed} --max_vertices 10000 &> {seed_dir}/log.txt'"
        )
        
        comandos.append(comando)
    
    # Salva comandos no arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# COMANDOS PARA EXECUÇÃO PARALELA - EXPERIMENTO POWER-LAW COMPLETO\n")
        f.write(f"# Total de seeds: {len(seeds)}\n")
        f.write(f"# Total de testes por seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA)}\n")
        f.write(f"# Total de grafos por seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA) * 50}\n\n")
        
        for comando in comandos:
            f.write(comando + "\n")
    
    print(f"Comandos salvos em: {output_file}")
    print(f"Total de comandos gerados: {len(comandos)}")

def gerar_comandos_todos(main_dir, seeds, output_file):
    """
    Gera comandos para ambos os experimentos.
    Cada comando é uma linha única, sem quebras, para GNU parallel.
    """
    print("Gerando comandos para ambos os experimentos...")
    
    # Configurações dos experimentos
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]
    TAMANHOS = [100, 1000, 10000, 100000, 1000000]
    PREFERENCIAS_DENSIDADE = [0, 1, 2]
    NUM_COMPONENTES = [0, 1]
    CATEGORIAS_GAMMA = ['denso', 'moderado', 'esparso']
    
    # Scripts Python
    script_simples = join_path(main_dir, "src/experimentos/simples.py")
    script_powerlaw = join_path(main_dir, "src/experimentos/power_law.py")
    
    comandos = []
    
    for seed in seeds:
        # Cria diretórios para esta seed
        seed_dir_simples = join_path(main_dir, f"resultados_experimentos/exp_simples_completo/{seed}")
        seed_dir_powerlaw = join_path(main_dir, f"resultados_experimentos/exp_powerlaw_completo/{seed}")
        
        comandos.append(f"mkdir -p {seed_dir_simples}")
        comandos.append(f"mkdir -p {seed_dir_powerlaw}")
        
        # Comando para experimento Simples (uma linha única, sem quebras)
        comando_simples = (
            f"mkdir -p {seed_dir_simples} && timeout --signal=SIGKILL 22h "
            f"bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; "
            f"python3 -u {script_simples} --output_dir {seed_dir_simples} --seeds {seed} --max_vertices 10000 &> {seed_dir_simples}/log.txt'"
        )
        
        # Comando para experimento Power-Law (uma linha única, sem quebras)
        comando_powerlaw = (
            f"mkdir -p {seed_dir_powerlaw} && timeout --signal=SIGKILL 22h "
            f"bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; "
            f"python3 -u {script_powerlaw} --output_dir {seed_dir_powerlaw} --seeds {seed} --max_vertices 10000 &> {seed_dir_powerlaw}/log.txt'"
        )
        
        comandos.append(comando_simples)
        comandos.append(comando_powerlaw)
    
    # Salva comandos no arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# COMANDOS PARA EXECUÇÃO PARALELA - AMBOS OS EXPERIMENTOS\n")
        f.write(f"# Total of seeds: {len(seeds)}\n")
        f.write(f"# Total of commands: {len(seeds) * 4}\n")
        f.write(f"# Commands per seed: 4 (2 mkdir + 2 python)\n")
        f.write(f"# Simples tests per seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES)}\n")
        f.write(f"# Power-Law tests per seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA)}\n")
        f.write(f"# Simples graphs per seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES) * 50}\n")
        f.write(f"# Power-Law graphs per seed: {len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA) * 50}\n")
        f.write(f"# Thread limit: 24 threads per process\n\n")
        
        for comando in comandos:
            f.write(comando + "\n")
    
    # Gera arquivo separado apenas com comandos mkdir (para GNU parallel)
    mkdir_file = output_file.replace('.sh', '_mkdir.sh')
    with open(mkdir_file, 'w', encoding='utf-8') as f:
        for comando in comandos:
            # mantém apenas mkdir simples (sem encadeamento com '&&')
            if comando.startswith('mkdir -p ') and '&&' not in comando:
                f.write(comando + "\n")
    
    # Gera arquivo separado apenas com comandos python (para GNU parallel)
    python_file = output_file.replace('.sh', '_python.sh')
    with open(python_file, 'w', encoding='utf-8') as f:
        for comando in comandos:
            # mantém apenas os comandos compostos (mkdir -p && timeout ...)
            if comando.startswith('mkdir -p ') and '&&' in comando and 'timeout --signal=SIGKILL 2h' in comando:
                f.write(comando + "\n")
    
    print(f"Comandos salvos em: {output_file}")
    print(f"Total de comandos gerados: {len(comandos)}")

def gerar_script_concatenacao(main_dir, seeds, output_file):
    """
    Gera script para concatenar os resultados de todas as seeds.
    """
    print("Gerando script de concatenação...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# SCRIPT PARA CONCATENAR RESULTADOS DE TODAS AS SEEDS\n\n")
        
        f.write(f"MAIN_DIR=\"{main_dir}\"\n")
        f.write("echo \"Concatenando resultados...\"\n\n")
        
        # Concatenação Simples
        f.write("# CONCATENAÇÃO EXPERIMENTO SIMPLES\n")
        f.write("echo \"Concatenando experimento Simples...\"\n")
        f.write("cat > ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv << 'EOF'\n")
        f.write("gerador,tipo,numV,numA,seed,estrategia_arestas,preferencia_densidade,numC,num_grafos_gerados\n")
        f.write("EOF\n\n")
        
        for seed in seeds:
            seed_file = f"${{MAIN_DIR}}/resultados_experimentos/exp_simples_completo/{seed}/resultados_simples_completo.csv"
            f.write(f"if [ -f {seed_file} ]; then\n")
            f.write(f"    tail -n +2 {seed_file} >> ${{MAIN_DIR}}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv\n")
            f.write(f"    echo \"Seed {seed} (Simples): OK\"\n")
            f.write("else\n")
            f.write(f"    echo \"Seed {seed} (Simples): ARQUIVO NÃO ENCONTRADO\"\n")
            f.write("fi\n\n")
        
        # Concatenação Power-Law
        f.write("# CONCATENAÇÃO EXPERIMENTO POWER-LAW\n")
        f.write("echo \"Concatenando experimento Power-Law...\"\n")
        f.write("cat > ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv << 'EOF'\n")
        f.write("gerador,tipo,numV,gamma,seed,num_grafos_gerados\n")
        f.write("EOF\n\n")
        
        for seed in seeds:
            seed_file = f"${{MAIN_DIR}}/resultados_experimentos/exp_powerlaw_completo/{seed}/resultados_powerlaw_completo.csv"
            f.write(f"if [ -f {seed_file} ]; then\n")
            f.write(f"    tail -n +2 {seed_file} >> ${{MAIN_DIR}}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv\n")
            f.write(f"    echo \"Seed {seed} (Power-Law): OK\"\n")
            f.write("else\n")
            f.write(f"    echo \"Seed {seed} (Power-Law): ARQUIVO NÃO ENCONTRADO\"\n")
            f.write("fi\n\n")
        
        f.write("echo \"Concatenação concluída!\"\n")
        f.write("echo \"Arquivos finais:\"\n")
        f.write("echo \"  - ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv\"\n")
        f.write("echo \"  - ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv\"\n")
    
    # Torna o script executável (ignora erros em sistemas montados NTFS/WSL)
    try:
        os.chmod(output_file, 0o755)
    except (PermissionError, OSError):
        pass  # Não é crítico; script pode ser executado com bash
    
    print(f"Script de concatenação salvo em: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Gerador de comandos para execução paralela dos experimentos')
    parser.add_argument('--main_dir', required=True, help='Diretório principal do projeto (caminho absoluto)')
    parser.add_argument('--experimento', choices=['simples', 'powerlaw', 'todos'], default='todos',
                       help='Experimento para gerar comandos')
    parser.add_argument('--seeds', nargs='+', type=int, 
                       default=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                       help='Lista de seeds para execução')
    parser.add_argument('--output_dir', default='./comandos_paralelos',
                       help='Diretório de saída para os comandos')
    
    args = parser.parse_args()
    
    # Converte para caminho absoluto
    main_dir = args.main_dir if args.main_dir.startswith('/') else os.path.abspath(args.main_dir)
    output_dir = os.path.abspath(args.output_dir)
    
    # Cria diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 80)
    print("GERADOR DE COMANDOS PARA EXECUÇÃO PARALELA")
    print("=" * 80)
    print(f"Diretório principal: {main_dir}")
    print(f"Diretório de saída: {output_dir}")
    print(f"Experimento: {args.experimento}")
    print(f"Seeds: {args.seeds}")
    print(f"Total de seeds: {len(args.seeds)}")
    print("=" * 80)
    
    # Gera comandos baseado no experimento escolhido
    if args.experimento == 'simples':
        output_file = os.path.join(output_dir, 'comandos_simples.sh')
        gerar_comandos_simples(main_dir, args.seeds, output_file)
        
    elif args.experimento == 'powerlaw':
        output_file = os.path.join(output_dir, 'comandos_powerlaw.sh')
        gerar_comandos_powerlaw(main_dir, args.seeds, output_file)
        
    else:  # todos
        output_file = os.path.join(output_dir, 'comandos_todos.sh')
        gerar_comandos_todos(main_dir, args.seeds, output_file)
    
    # Gera script de concatenação
    script_concatenacao = os.path.join(output_dir, 'concatenar_resultados.sh')
    gerar_script_concatenacao(main_dir, args.seeds, script_concatenacao)
    
    # Gera README com instruções
    readme_file = os.path.join(output_dir, 'README.md')
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("# EXECUÇÃO PARALELA DOS EXPERIMENTOS\n\n")
        f.write("## Arquivos Gerados:\n\n")
        f.write(f"- `comandos_{args.experimento}.sh`: Comandos para execução paralela\n")
        f.write("- `concatenar_resultados.sh`: Script para concatenar resultados\n")
        f.write("- `README.md`: Este arquivo\n\n")
        
        f.write("## Como Usar:\n\n")
        f.write("### 1. Execução Paralela:\n")
        f.write("```bash\n")
        f.write(f"# Execute os comandos em paralelo (exemplo com 4 threads)\n")
        f.write(f"cat comandos_{args.experimento}.sh | parallel -j 4\n")
        f.write("```\n\n")
        
        f.write("### 2. Concatenação dos Resultados:\n")
        f.write("```bash\n")
        f.write("./concatenar_resultados.sh\n")
        f.write("```\n\n")
        
        f.write("### 3. Estrutura de Saída:\n")
        f.write("```\n")
        f.write(f"{main_dir}/resultados_experimentos/\n")
        f.write("├── exp_simples_completo/\n")
        f.write("│   ├── resultados_simples_completo.csv  # Resultado final\n")
        f.write("│   └── {seed}/                          # Dados por seed\n")
        f.write("│       ├── resultados_simples_completo.csv\n")
        f.write("│       └── log.txt\n")
        f.write("└── exp_powerlaw_completo/\n")
        f.write("    ├── resultados_powerlaw_completo.csv  # Resultado final\n")
        f.write("    └── {seed}/                          # Dados por seed\n")
        f.write("        ├── resultados_powerlaw_completo.csv\n")
        f.write("        └── log.txt\n")
        f.write("```\n\n")
        
        f.write("## Vantagens da Execução Paralela:\n\n")
        f.write("1. **Independência**: Cada seed executa em arquivo separado\n")
        f.write("2. **Sem condições de corrida**: Não há conflito de escrita\n")
        f.write("3. **Paralelização**: Múltiplas execuções simultâneas\n")
        f.write("4. **Recuperação**: Se uma seed falhar, as outras continuam\n")
        f.write("5. **Monitoramento**: Logs separados por seed\n")
    
    print("\n" + "=" * 80)
    print("GERAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"Arquivos gerados em: {output_dir}")
    print(f"1. comandos_{args.experimento}.sh - Comandos para execução paralela")
    print(f"2. concatenar_resultados.sh - Script para concatenar resultados")
    print(f"3. README.md - Instruções de uso")
    print("\nPróximos passos:")
    print(f"1. Execute: cat {output_dir}/comandos_{args.experimento}.sh | parallel -j 4")
    print(f"2. Após conclusão: {output_dir}/concatenar_resultados.sh")
    print("=" * 80)

if __name__ == "__main__":
    main()
