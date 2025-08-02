"""
Script para execução massiva de testes do módulo simples.
Permite executar milhares de testes com diferentes configurações.
"""

import subprocess
import time
import os
from datetime import datetime

def executa_teste(config):
    """Executa um teste com configuração específica."""
    cmd = f"python test_simples.py {config['execucoes']} {config['vertices']} {config['arquivo']}"
    print(f"🔄 Executando: {cmd}")
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    end_time = time.time()
    
    if result.returncode == 0:
        print(f"✅ Concluído em {end_time - start_time:.2f}s")
        return True
    else:
        print(f"❌ Erro: {result.stderr}")
        return False

def executa_bateria_testes():
    """Executa uma bateria completa de testes."""
    print("🚀 Iniciando Bateria de Testes Massivos")
    print("=" * 60)
    
    # Configurações de teste
    configs = [
        # Testes pequenos (rápidos)
        {
            'nome': 'Testes Pequenos',
            'execucoes': 10,
            'vertices': '20,50',
            'arquivo': f"resultados_pequenos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        },
        # Testes médios
        {
            'nome': 'Testes Médios',
            'execucoes': 20,
            'vertices': '100,200',
            'arquivo': f"resultados_medios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        },
        # Testes grandes (mais demorados)
        {
            'nome': 'Testes Grandes',
            'execucoes': 15,
            'vertices': '500,1000',
            'arquivo': f"resultados_grandes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    ]
    
    total_sucessos = 0
    total_configs = len(configs)
    
    for i, config in enumerate(configs, 1):
        print(f"\n📊 Configuração {i}/{total_configs}: {config['nome']}")
        print(f"   Execuções: {config['execucoes']}")
        print(f"   Vértices: {config['vertices']}")
        print(f"   Arquivo: {config['arquivo']}")
        
        if executa_teste(config):
            total_sucessos += 1
        
        # Pausa entre execuções
        if i < total_configs:
            print("⏳ Aguardando 5 segundos...")
            time.sleep(5)
    
    print(f"\n🎉 Bateria de Testes Concluída!")
    print(f"   Sucessos: {total_sucessos}/{total_configs}")
    print(f"   Taxa de sucesso: {(total_sucessos/total_configs)*100:.1f}%")

def executa_teste_especifico():
    """Executa um teste específico baseado em input do usuário."""
    print("🎯 Teste Específico")
    print("=" * 30)
    
    try:
        execucoes = int(input("Número de execuções por tipo: ") or "5")
        vertices_input = input("Vértices (separados por vírgula): ") or "100,200"
        vertices = [int(x.strip()) for x in vertices_input.split(',')]
        
        config = {
            'execucoes': execucoes,
            'vertices': vertices_input,
            'arquivo': f"resultados_especifico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
        
        executa_teste(config)
        
    except ValueError as e:
        print(f"❌ Erro de entrada: {e}")

def main():
    """Menu principal."""
    print("🧪 Sistema de Testes Massivos - Módulo Simples")
    print("=" * 50)
    print("1. Bateria completa de testes")
    print("2. Teste específico")
    print("3. Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-3): ").strip()
            
            if opcao == "1":
                executa_bateria_testes()
                break
            elif opcao == "2":
                executa_teste_especifico()
                break
            elif opcao == "3":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida. Escolha 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 