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
# 1. Gerar comandos por tipo
bash comandos_teste/comandos_por_tipo.sh > comandos_execucao.sh

# 2. Executar com 12 threads (teste controlado)
parallel -j 12 < comandos_execucao.sh

# 3. Concatenação dos resultados
bash comandos_teste/concatenar_resultados_por_tipo.sh
```

**Resultado esperado**:
- ✅ ~1.200 arquivos CSV individuais
- ✅ 2 arquivos consolidados (simples + powerlaw)
- ✅ Tempo: ~30 minutos
- ✅ Validação: Paralelização funcionando

### **3. EXECUÇÃO COMPLETA (Produção) - 2-3 horas**

**Objetivo**: Execução completa com máxima paralelização.

```bash
# 1. Gerar comandos completos
bash comandos_teste/comandos_por_tipo.sh > comandos_execucao.sh

# 2. Executar com 120 threads (todas as máquinas)
parallel -j 120 < comandos_execucao.sh

# 3. Concatenação dos resultados
bash comandos_teste/concatenar_resultados_por_tipo.sh
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
bash comandos_teste/comandos_por_tipo.sh > comandos.sh
parallel -j 12 < comandos.sh
bash comandos_teste/concatenar_resultados_por_tipo.sh
```

### **Execução Completa:**
```bash
bash comandos_teste/comandos_por_tipo.sh > comandos.sh
parallel -j 120 < comandos.sh
bash comandos_teste/concatenar_resultados_por_tipo.sh
```

## ✅ Status do Sistema

**Sistema testado e funcionando:**
- ✅ **Scripts Python**: Funcionando com argumento `--tipos`
- ✅ **Verificação de dependências**: Implementada
- ✅ **Otimização para grafos densos**: Implementada
- ✅ **Limites de recursos**: Otimizados (apenas timeout)
- ✅ **Smoke test**: Validado e funcionando
- ✅ **Granularidade por tipo**: Implementada

