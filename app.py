"""Streamlit Interactive Workbench for SQL Insight AI Engine."""

from __future__ import annotations
import pandas as pd
import streamlit as st
from src.sample_db import create_sample_analytics_db
from src.schema_inspector import inspect_sqlite_schema
from src.nl2sql_engine import translate_question_to_sql
from src.query_optimizer import analyze_and_optimize_sql, validate_read_only_sql

st.set_page_config(page_title="SQL Insight AI Engine", layout="wide")

st.title("SQL Insight AI Engine — Schema Inspector, NL2SQL & Query Optimizer")
st.caption("Enterprise Relational Schema Analysis, Natural Language to SQL Generation, and Execution Plan Optimization.")

conn = create_sample_analytics_db()
schema = inspect_sqlite_schema(conn)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Database Schema Metadata")
    for tbl in schema.tables:
        with st.expander(f"Table: {tbl.table_name} ({tbl.row_count} rows)", expanded=True):
            df_cols = pd.DataFrame([c.model_dump() for c in tbl.columns])
            st.dataframe(df_cols, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Natural Language to Optimized SQL")
    question = st.text_input(
        "Analytical Business Question:",
        value="Show total completed revenue and average order value grouped by customer region",
    )
    res = translate_question_to_sql(question, schema)
    sql_editor = st.text_area("Generated SQL Query (Editable):", value=res.generated_sql, height=130)

    if st.button("Execute & Analyze Execution Plan", type="primary"):
        report = analyze_and_optimize_sql(conn, sql_editor)
        if not report.is_read_only:
            st.error("Blocked non-read-only SQL statement.")
        else:
            df_res = pd.read_sql_query(sql_editor, conn)
            st.subheader("Query Result Set")
            st.dataframe(df_res, use_container_width=True)

            st.subheader("Execution Plan & Index Recommendations")
            st.json(report.model_dump())
