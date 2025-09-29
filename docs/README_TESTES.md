# GUIA DE TESTES - SISTEMA DE EXPERIMENTOS

## 🎯 Visão Geral

Este guia apresenta diferentes níveis de teste para validar o sistema de experimentos, desde validação rápida até execução completa em produção.

## 🧪 Níveis de Teste

### **1. TESTE RÁPIDO (Smoke Test) - 5 minutos**

**Objetivo**: Validação rápida do sistema com parâmetros reduzidos.

```bash
# Teste Simples
python src/experimentos/simples.py \
  --seeds 1000 2000 \
  --tipos 0 1 \
  --smoke \
  --num_grafos 2 \
  --output_format individual_csv \
  --output_dir resultados_experimentos/smoke_simples

# Teste Power-Law
python src/experimentos/power_law.py \
  --seeds 1000 2000 \
  --tipos 0 1 \
  --smoke \
  --num_grafos 2 \
  --output_format individual_csv \
  --output_dir resultados_experimentos/smoke_powerlaw
```

**Resultado esperado**:
- ✅ 8 arquivos CSV (Simples) + 8 arquivos CSV (Power-Law)
- ✅ Tempo: ~5 minutos
- ✅ Validação: Sistema funcionando

### **2. TESTE MÉDIO (Validação) - 30 minutos**

**Objetivo**: Teste com granularidade por tipo, validando paralelização.

```bash
# 1. Gerar comandos usando paralelizacao.py
python src/experimentos/paralelizacao.py \
  --main_dir $(pwd) \
  --experimento todos \
  --seeds 2700001 3170702080 3548644859 1033592630 9263589860 1883634842 7648101510 1502014705 7214842310 2606453957 4194499680 2779365847 1094121244 1090525961 3310223418 604827988 1549035388 795578792 182649370 1127200130 332728275 1477598055 1157679575 3489403805 359655529 3107219804 911079554 1642444692 3959116112 2991474091

# 2. Executar com GNU parallel (exemplo com 12 threads)
cat comandos_paralelos/comandos_todos.sh | parallel -j 12

# 3. Concatenação dos resultados
bash comandos_paralelos/concatenar_resultados.sh
```

**Resultado esperado**:
- ✅ ~1.200 arquivos CSV individuais
- ✅ 2 arquivos consolidados (simples + powerlaw)
- ✅ Tempo: ~30 minutos
- ✅ Validação: Paralelização funcionando

### **3. EXECUÇÃO COMPLETA (Produção) - 2-3 horas**

**Objetivo**: Execução completa com máxima paralelização.

```bash
# 1. Gerar comandos usando paralelizacao.py
python src/experimentos/paralelizacao.py \
  --main_dir $(pwd) \
  --experimento todos \
  --seeds 2700001 3170702080 3548644859 1033592630 9263589860 1883634842 7648101510 1502014705 7214842310 2606453957 4194499680 2779365847 1094121244 1090525961 3310223418 604827988 1549035388 795578792 182649370 1127200130 332728275 1477598055 1157679575 3489403805 359655529 3107219804 911079554 1642444692 3959116112 2991474091

# 2. Executar com GNU parallel (exemplo com 60 threads - 30% das máquinas)
cat comandos_paralelos/comandos_todos.sh | parallel -j 60

# 3. Concatenação dos resultados
bash comandos_paralelos/concatenar_resultados.sh
```

**Resultado esperado**:
- ✅ ~135.000 arquivos CSV individuais
- ✅ 2 arquivos consolidados finais
- ✅ Tempo: 2-3 horas
- ✅ Aproveitamento: 60% das máquinas (120/200)

## 📊 Comparação de Níveis

| Nível | Comandos | Threads | Tempo | CSVs | Objetivo |
|-------|----------|---------|-------|------|----------|
| **Smoke** | 2 | 1 | 5min | 16 | Validação rápida |
| **Médio** | 24 | 12 | 30min | ~1.200 | Teste paralelo |
| **Completo** | 120 | 120 | 2-3h | ~135.000 | Produção |

## 🔍 Verificações Pós-Teste

### **1. Verificar Erros**
```bash
# Procurar por erros nos logs
grep -r "ERRO\|ERROR\|Exitval" resultados_experimentos/
# Deve retornar vazio (sem erros)
```

### **2. Contar Arquivos Gerados**
```bash
# Contar CSVs individuais
find resultados_experimentos/ -name "*.csv" | wc -l

# Verificar arquivos consolidados
ls -la resultados_experimentos/resultados_*.csv
```

### **3. Verificar Qualidade dos Dados**
```bash
# Verificar tamanho dos arquivos
du -h resultados_experimentos/resultados_*.csv

# Verificar conteúdo (primeiras linhas)
head -5 resultados_experimentos/resultados_simples_por_tipo.csv
head -5 resultados_experimentos/resultados_powerlaw_por_tipo.csv
```

## 🎯 Estratégia Recomendada

### **Para Primeira Execução:**
1. **Smoke Test** (5min) - Validar sistema
2. **Teste Médio** (30min) - Validar paralelização
3. **Execução Completa** (2-3h) - Produção

### **Para Desenvolvimento:**
- Use sempre **Smoke Test** para validação rápida
- Use **Teste Médio** para validar mudanças
- Use **Execução Completa** apenas para produção

### **Para Debug:**
```bash
# Teste individual para debug
python src/experimentos/simples.py \
  --seeds 1000 \
  --tipos 0 \
  --smoke \
  --num_grafos 1 \
  --output_format individual_csv \
  --output_dir debug/1000_tipo0
```

## 📈 Resultados Esperados

### **Smoke Test:**
- ✅ 16 arquivos CSV
- ✅ Tempo: ~5 minutos
- ✅ Status: 100% sucesso

### **Teste Médio:**
- ✅ ~1.200 arquivos CSV
- ✅ Tempo: ~30 minutos
- ✅ Status: 100% sucesso

### **Execução Completa:**
- ✅ ~135.000 arquivos CSV
- ✅ Tempo: 2-3 horas
- ✅ Status: 100% sucesso
- ✅ Aproveitamento: 60% das máquinas

## 🚀 Comandos Rápidos

### **Smoke Test Completo:**
```bash
# Simples
python src/experimentos/simples.py --seeds 1000 2000 --tipos 0 1 --smoke --num_grafos 2 --output_format individual_csv --output_dir resultados_experimentos/smoke_simples

# Power-Law
python src/experimentos/power_law.py --seeds 1000 2000 --tipos 0 1 --smoke --num_grafos 2 --output_format individual_csv --output_dir resultados_experimentos/smoke_powerlaw
```

### **Teste Médio:**
```bash
python src/experimentos/paralelizacao.py --main_dir $(pwd) --experimento todos --seeds 2700001 3170702080 3548644859 1033592630 9263589860
cat comandos_paralelos/comandos_todos.sh | parallel -j 12
bash comandos_paralelos/concatenar_resultados.sh
```

### **Execução Completa:**
```bash
python src/experimentos/paralelizacao.py --main_dir $(pwd) --experimento todos --seeds 2700001 3170702080 3548644859 1033592630 9263589860 1883634842 7648101510 1502014705 7214842310 2606453957 4194499680 2779365847 1094121244 1090525961 3310223418 604827988 1549035388 795578792 182649370 1127200130 332728275 1477598055 1157679575 3489403805 359655529 3107219804 911079554 1642444692 3959116112 2991474091
cat comandos_paralelos/comandos_todos.sh | parallel -j 60
bash comandos_paralelos/concatenar_resultados.sh
```

## ✅ Status do Sistema

**Sistema testado e funcionando:**
- ✅ **Scripts Python**: Funcionando com argumento `--tipos`
- ✅ **Verificação de dependências**: Implementada
- ✅ **Otimização para grafos densos**: Implementada
- ✅ **Limites de recursos**: Otimizados (apenas timeout)
- ✅ **Smoke test**: Validado e funcionando
- ✅ **Granularidade por tipo**: Implementada

