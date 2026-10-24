# SQL Insight AI Engine

Python tool that inspects a relational database schema, turns plain English questions into read-only SQL and suggests indexes based on the query plan.

## Features

- Reads tables, columns, keys and indexes from a SQLite database
- Converts natural language questions into SQL using the Gemini API, with a rule based fallback when no API key is set
- Runs `EXPLAIN QUERY PLAN` and points out full table scans
- Suggests `CREATE INDEX` statements for slow queries
- Blocks any statement that changes data (`INSERT`, `UPDATE`, `DELETE`, `DROP`)

## Tech Stack

- Python 3.11
- SQLite
- Streamlit
- Pydantic
- Pandas
- Pytest

## Getting Started

```bash
git clone https://github.com/davyd9/sql-insight-ai-engine.git
cd sql-insight-ai-engine
pip install -r requirements.txt
pytest -v
streamlit run app.py
```

To use the Gemini translator, set `GEMINI_API_KEY` in your environment. Without it the app uses the built-in fallback planner.
