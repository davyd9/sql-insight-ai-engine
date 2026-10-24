# SQL Insight AI Engine

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Workbench-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQL](https://img.shields.io/badge/SQL-Query%20Optimizer-CC2927?logo=microsoftsqlserver&logoColor=white)](https://github.com/davyd9/sql-insight-ai-engine)
[![Tests](https://img.shields.io/badge/Pytest-Passing-10B981?logo=pytest&logoColor=white)](https://github.com/davyd9/sql-insight-ai-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 🇧🇷 *[Leia em Português (README.pt-br.md)](README.pt-br.md)* | 🌐 **[Try the Interactive Web Workbench](https://davyd9.github.io/demos/sql-insight-engine/)**

**SQL Insight AI Engine** is an analytical database introspection, Natural Language-to-SQL (NL2SQL) translation, and execution plan optimization tool built in Python. It inspects relational database schemas, translates business questions into strictly validated read-only SQL queries, evaluates `EXPLAIN QUERY PLAN` output, and recommends composite B-Tree indexes to eliminate full table scans.

---

## Key Features

- **Automated DDL Schema Introspection (`src/schema_inspector.py`):** Extracts table structures, column types, primary/foreign keys, row counts, and active indexes into strongly typed Pydantic v2 models.
- **Natural Language to SQL Translation (`src/nl2sql_engine.py`):** Converts analytical business questions into read-only SQL queries using Google Gemini (`gemini-2.5-flash`) with a schema-aware deterministic fallback planner.
- **Execution Plan & Index Recommendation Engine (`src/query_optimizer.py`):** Inspects `EXPLAIN QUERY PLAN`, detects full table scans (`SCAN TABLE`), warns against non-sargable predicates or `SELECT *`, and generates `CREATE INDEX` DDL statements.
- **Strict Read-Only Security Guardrails:** Blocks all mutating DML/DDL statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`).

---

## Project Structure

```text
sql-insight-ai-engine/
├── src/
│   ├── __init__.py
│   ├── schema_inspector.py   # Relational metadata & DDL extractor
│   ├── query_optimizer.py    # EXPLAIN QUERY PLAN analyzer & index recommender
│   ├── nl2sql_engine.py      # Gemini API + deterministic NL2SQL translator
│   └── sample_db.py          # Seeded enterprise analytical SQLite database
├── tests/
│   └── test_sql_engine.py    # Automated unit & integration tests (Pytest)
├── app.py                    # Streamlit interactive SQL workbench
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Quick Start

```bash
pip install -r requirements.txt
pytest -v
streamlit run app.py
```

---

## Author

**Davyd Eduardo** — Software Developer & Data Analyst  
- **Portfolio:** [https://davyd9.github.io/](https://davyd9.github.io/)  
- **LinkedIn:** [linkedin.com/in/davyd-eduardo-506646289](https://www.linkedin.com/in/davyd-eduardo-506646289/)  
- **GitHub:** [github.com/davyd9](https://github.com/davyd9)
