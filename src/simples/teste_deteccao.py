"""
Teste simples para verificar a detecção de tipos de grafos.
"""
import random
import numpy as np
from gerador import geraMultigrafo, geraPseudografo
from utils import criaMatrizAdjacencias, tipoGrafo

def debug_tipoGrafo(matriz):
    """Debug da função tipoGrafo."""
    laco = False
    multipla = False
    vert = len(matriz)
    
    print("🔍 Debug da função tipoGrafo:")
    for i in range(vert):
        for j in range(vert):
            cell = matriz[i][j]
            if cell > 0:
                print(f"  Posição [{i},{j}] = {cell}")
                if cell > 1:
                    multipla = True
                    print(f"    -> Aresta múltipla detectada!")
                if cell > 0 and i == j:
                    laco = True
                    print(f"    -> Laço detectado!")
    
    dirigido = not (np.transpose(matriz) == matriz).all()
    print(f"  Dirigido: {dirigido}")
    print(f"  Múltipla: {multipla}")
    print(f"  Laço: {laco}")
    
    if dirigido and multipla and laco:
        tipo = 31
    elif dirigido and multipla:
        tipo = 21
    elif dirigido:
        tipo = 1
    elif laco:
        tipo = 30
    elif multipla:
        tipo = 20
    else:
        tipo = 0
    
    print(f"  Tipo calculado: {tipo}")
    return tipo

def testa_deteccao():
    """Testa a detecção de tipos de grafos."""
    random.seed(42)
    
    print("🧪 Testando Detecção de Tipos de Grafos")
    print("=" * 50)
    
    # Teste Multigrafo Simples (tipo 20)
    print("\n📊 Teste Multigrafo Simples (tipo 20):")
    arestas_multigrafo = geraMultigrafo(10, 15, dirigido=False)
    print(f"Arestas geradas: {arestas_multigrafo}")
    matriz = criaMatrizAdjacencias(arestas_multigrafo, 10, 20)
    print(f"Matriz gerada:\n{matriz}")
    
    # Debug manual
    tipo_debug = debug_tipoGrafo(matriz)
    
    # Função original
    tipo_detectado = tipoGrafo(matriz)
    print(f"Tipo detectado (função): {tipo_detectado}")
    print(f"Tipo detectado (debug): {tipo_debug}")
    print(f"Esperado: 20, Obtido: {tipo_detectado}")
    print(f"✅ Correto!" if tipo_detectado == 20 else f"❌ Erro!")
    
    # Teste Multigrafo Dirigido (tipo 21)
    print("\n📊 Teste Multigrafo Dirigido (tipo 21):")
    arestas_multigrafo_dir = geraMultigrafo(10, 15, dirigido=True)
    print(f"Arestas geradas: {arestas_multigrafo_dir}")
    matriz = criaMatrizAdjacencias(arestas_multigrafo_dir, 10, 21)
    tipo_detectado = tipoGrafo(matriz)
    print(f"Tipo detectado: {tipo_detectado}")
    print(f"Esperado: 21, Obtido: {tipo_detectado}")
    print(f"✅ Correto!" if tipo_detectado == 21 else f"❌ Erro!")
    
    # Teste Pseudografo Simples (tipo 30)
    print("\n📊 Teste Pseudografo Simples (tipo 30):")
    arestas_pseudografo = geraPseudografo(10, 15, dirigido=False)
    print(f"Arestas geradas: {arestas_pseudografo}")
    matriz = criaMatrizAdjacencias(arestas_pseudografo, 10, 30)
    print(f"Matriz gerada:\n{matriz}")
    tipo_detectado = tipoGrafo(matriz)
    print(f"Tipo detectado: {tipo_detectado}")
    print(f"Esperado: 30, Obtido: {tipo_detectado}")
    print(f"✅ Correto!" if tipo_detectado == 30 else f"❌ Erro!")
    
    # Teste Pseudografo Dirigido (tipo 31)
    print("\n📊 Teste Pseudografo Dirigido (tipo 31):")
    arestas_pseudografo_dir = geraPseudografo(10, 15, dirigido=True)
    print(f"Arestas geradas: {arestas_pseudografo_dir}")
    matriz = criaMatrizAdjacencias(arestas_pseudografo_dir, 10, 31)
    tipo_detectado = tipoGrafo(matriz)
    print(f"Tipo detectado: {tipo_detectado}")
    print(f"Esperado: 31, Obtido: {tipo_detectado}")
    print(f"✅ Correto!" if tipo_detectado == 31 else f"❌ Erro!")

if __name__ == "__main__":
    testa_deteccao() 