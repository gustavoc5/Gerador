# SISTEMA DE EXECUÇÃO PARALELA - TODOS OS EXPERIMENTOS

## 🎯 O QUE FAZ

**Gera comandos para executar TODOS os 2.700 testes em paralelo:**
- **Simples:** 1.800 testes × 50 grafos = 90.000 arquivos CSV
- **Power-Law:** 900 testes × 50 grafos = 45.000 arquivos CSV
- **Total:** 135.000 arquivos CSV individuais (1 por grafo)

**Cada seed executa em seu próprio diretório, evitando condições de corrida.**

---

## 🚀 COMO EXECUTAR

### **1. Gerar Comandos**
```bash
bash comandos_completos_paralelos.sh > comandos_execucao.sh
```

### **2. Executar em Paralelo**
```bash
# Com 10 threads (uma por seed)
cat comandos_execucao.sh | parallel -j 10

# Ou com todos os cores
cat comandos_execucao.sh | parallel -j $(nproc)
```

### **3. Concatenação Final**
```bash
bash concatenar_resultados_completos.sh
```

---

## 📁 ESTRUTURA GERADA

```
resultados_experimentos/
├── exp_simples_completo/
│   ├── 1000/                              # Seed 1000
│   │   ├── metricas_1000_tipo0_v100_dens0_comp0_1.csv
│   │   ├── metricas_1000_tipo0_v100_dens0_comp0_2.csv
│   │   └── ... (90.000 arquivos CSV)
│   ├── 2000/                              # Seed 2000
│   └── ... (até seed 10000)
└── exp_powerlaw_completo/
    ├── 1000/                              # Seed 1000
    │   ├── metricas_1000_tipo0_v100_gamma2.1_1.csv
    │   └── ... (45.000 arquivos CSV)
    └── ... (até seed 10000)
```

**Após concatenação:**
- `resultados_simples_completo.csv` (90.000 grafos)
- `resultados_powerlaw_completo.csv` (45.000 grafos)

---
**✅ IMPLEMENTADO:**
- 20 comandos Python independentes
- Cada seed em diretório separado
- 1 arquivo CSV por grafo (135.000 arquivos únicos)
- Paralelização REAL sem condições de corrida
