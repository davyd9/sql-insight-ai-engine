# SQL Insight AI Engine (PT-BR)

> 🇺🇸 *[Read in English (README.md)](README.md)* | 🌐 **[Testar Workbench Interativo Online](https://davyd9.github.io/demos/sql-insight-engine/)**

**SQL Insight AI Engine** é uma ferramenta de introspecção de schemas relacionais, conversão de linguagem natural para SQL (NL2SQL) e otimização de planos de execução construída em Python.

## Funcionalidades Principais
- **Introspecção Automática de Schema (`src/schema_inspector.py`):** Extrai tabelas, colunas, chaves primárias/estrangeiras, contagem de registros e índices em modelos Pydantic.
- **Tradução de Perguntas de Negócio para SQL (`src/nl2sql_engine.py`):** Converte perguntas analíticas em queries SQL otimizadas usando Google Gemini (`gemini-2.5-flash`) e planejador determinístico.
- **Otimizador de Queries e Recomendação de Índices (`src/query_optimizer.py`):** Analisa `EXPLAIN QUERY PLAN`, detecta Table Scans e sugere comandos `CREATE INDEX`.
- **Guardrails de Segurança Read-Only:** Bloqueia comandos destrutivos (`DROP`, `DELETE`, `UPDATE`, `ALTER`, `TRUNCATE`).
