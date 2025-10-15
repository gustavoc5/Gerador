# EXECUÇÃO PARALELA DOS EXPERIMENTOS

## Arquivos Gerados:

- `comandos_todos.sh`: Comandos para execução paralela
- `concatenar_resultados.sh`: Script para concatenar resultados
- `README.md`: Este arquivo

## Como Usar:

### 1. Execução Paralela:
```bash
# Execute os comandos em paralelo (exemplo com 4 threads)
cat comandos_todos.sh | parallel -j 4
```

### 2. Concatenação dos Resultados:
```bash
./concatenar_resultados.sh
```

### 3. Estrutura de Saída:
```
/mnt/c/Users/gusta/OneDrive/GUSTAVO/Unifei/TCC/Gerador/resultados_experimentos/
├── exp_simples_completo/
│   ├── resultados_simples_completo.csv  # Resultado final
│   └── {seed}/                          # Dados por seed
│       ├── resultados_simples_completo.csv
│       └── log.txt
└── exp_powerlaw_completo/
    ├── resultados_powerlaw_completo.csv  # Resultado final
    └── {seed}/                          # Dados por seed
        ├── resultados_powerlaw_completo.csv
        └── log.txt
```

## Vantagens da Execução Paralela:

1. **Independência**: Cada seed executa em arquivo separado
2. **Sem condições de corrida**: Não há conflito de escrita
3. **Paralelização**: Múltiplas execuções simultâneas
4. **Recuperação**: Se uma seed falhar, as outras continuam
5. **Monitoramento**: Logs separados por seed
