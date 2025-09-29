# SISTEMA DE EXECUÇÃO PARALELA POR TIPO - ESTRATÉGIA GRANULAR

## 🎯 O QUE FAZ

**Gera comandos para executar experimentos com granularidade por tipo de grafo:**
- **120 comandos** (10 seeds × 6 tipos × 2 experimentos)
- **Processos menores** (20min vs 2h)
- **Melhor aproveitamento** das máquinas (60% vs 10%)
- **Menos falhas** (Exitval 0)

**Cada comando processa apenas 1 tipo de grafo por seed, evitando processos longos.**

---

## 🚀 COMO EXECUTAR

### **1. Gerar Comandos**
```bash
bash comandos_por_tipo.sh > comandos_execucao.sh
```

### **2. Executar em Paralelo**
```bash
# Com 120 threads (recomendado)
cat comandos_execucao.sh | parallel -j 120

# Com 200 threads (máximo)
cat comandos_execucao.sh | parallel -j 200

# Com GNU parallel
parallel -j 120 < comandos_execucao.sh
```

### **3. Concatenação Final**
```bash
bash concatenar_resultados_por_tipo.sh
```

---

## 📁 ESTRUTURA GERADA

```
resultados_experimentos/
├── exp_simples_por_tipo/
│   ├── 1000_tipo0/  (30 combinações: 5 tamanhos × 3 densidades × 2 componentes)
│   ├── 1000_tipo1/  (30 combinações)
│   ├── 1000_tipo20/ (30 combinações)
│   ├── 1000_tipo21/ (30 combinações)
│   ├── 1000_tipo30/ (30 combinações)
│   ├── 1000_tipo31/ (30 combinações)
│   ├── 2000_tipo0/  (30 combinações)
│   └── ... (até 10000_tipo31)
└── exp_powerlaw_por_tipo/
    ├── 1000_tipo0/  (15 combinações: 5 tamanhos × 3 gammas)
    ├── 1000_tipo1/  (15 combinações)
    └── ... (até 10000_tipo31)
```

**Após concatenação:**
- `resultados_simples_por_tipo.csv` (90.000 grafos)
- `resultados_powerlaw_por_tipo.csv` (45.000 grafos)

---

## 🎯 VANTAGENS DA ESTRATÉGIA POR TIPO

### **📊 Comparação com Estratégia Atual:**

| Métrica | Atual | Por Tipo | Melhoria |
|---------|-------|----------|----------|
| **Comandos** | 20 | 120 | **6x mais** |
| **Máquinas usadas** | 20/200 (10%) | 120/200 (60%) | **6x melhor** |
| **Tempo por processo** | 2h | 20min | **6x mais rápido** |
| **Chance de falha** | Alta | Baixa | **Muito melhor** |
| **Debug** | Difícil | Fácil | **Muito melhor** |

### **✅ Benefícios:**

1. **Processos Menores**: 20min vs 2h = menos chance de timeout
2. **Melhor Paralelização**: 120 vs 20 comandos = 6x mais granularidade
3. **Aproveitamento**: 60% vs 10% das máquinas
4. **Debug Fácil**: 1 tipo por processo = fácil identificação de problemas
5. **Mesma Qualidade**: 2.700 testes, 135.000 grafos (exatamente igual)

### **🔧 Implementação:**

**Scripts Python atualizados:**
- ✅ Argumento `--tipos` adicionado
- ✅ Filtro por tipo implementado
- ✅ Compatibilidade mantida

**Scripts Bash criados:**
- ✅ `comandos_por_tipo.sh` - Gera 120 comandos
- ✅ `concatenar_resultados_por_tipo.sh` - Concatena resultados

---

## 🧪 TESTE RÁPIDO

### **Smoke Test:**
```bash
# Teste com parâmetros reduzidos
export SMOKE=1
bash comandos_por_tipo.sh > comandos_execucao.sh
parallel -j 12 < comandos_execucao.sh
```

### **Teste Individual:**
```bash
# Testar um comando específico
python src/experimentos/simples.py \
  --seeds 1000 \
  --tipos 0 \
  --smoke \
  --num_grafos 1 \
  --output_format individual_csv \
  --output_dir resultados_experimentos/teste/1000_tipo0
```

---

## 📈 RESULTADOS ESPERADOS

**Execução Completa:**
- **120 comandos** executados em paralelo
- **2.700 testes** realizados (mesmo número que antes)
- **135.000 grafos** processados (mesmo número que antes)
- **Tempo total**: ~1/3 do tempo atual
- **Taxa de sucesso**: Muito maior (processos menores)

**Arquivos Finais:**
- `resultados_simples_por_tipo.csv` (90.000 grafos)
- `resultados_powerlaw_por_tipo.csv` (45.000 grafos)

---

## 🎯 CONCLUSÃO

**A estratégia "Por Tipo" resolve perfeitamente o problema do orientador:**

1. ✅ **Aumenta paralelização** de 60 para 120+ processos
2. ✅ **Processos menores** = menos falhas (Exitval 0)
3. ✅ **Melhor aproveitamento** das 200 máquinas (60%)
4. ✅ **Execução mais rápida** (1/3 do tempo)
5. ✅ **Mesma qualidade científica** (mesmos testes, mesmos grafos)
