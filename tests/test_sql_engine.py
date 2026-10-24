"""Automated unit and integration tests for SQL Insight AI Engine."""

from src.sample_db import create_sample_analytics_db
from src.schema_inspector import inspect_sqlite_schema
from src.query_optimizer import validate_read_only_sql, analyze_and_optimize_sql
from src.nl2sql_engine import translate_question_to_sql


def test_schema_introspection():
    conn = create_sample_analytics_db()
    schema = inspect_sqlite_schema(conn)
    table_names = [t.table_name for t in schema.tables]
    assert "customers" in table_names
    assert "orders" in table_names
    assert "products" in table_names
    assert "order_items" in table_names


def test_read_only_sql_guardrails():
    assert validate_read_only_sql("SELECT customer_id, company_name FROM customers;") is True
    assert validate_read_only_sql("WITH cte AS (SELECT * FROM orders) SELECT * FROM cte;") is True
    assert validate_read_only_sql("DROP TABLE customers;") is False
    assert validate_read_only_sql("DELETE FROM orders WHERE order_id = 1001;") is False
    assert validate_read_only_sql("UPDATE customers SET tier = 'Free';") is False


def test_query_optimizer_plan_and_index_recommendation():
    conn = create_sample_analytics_db()
    report = analyze_and_optimize_sql(
        conn, "SELECT * FROM orders WHERE status = 'COMPLETED'"
    )
    assert report.is_read_only is True
    assert len(report.execution_plan) > 0
    assert any("SELECT *" in w for w in report.warnings)
    assert len(report.recommended_indexes) >= 1


def test_nl2sql_translation():
    conn = create_sample_analytics_db()
    schema = inspect_sqlite_schema(conn)
    res = translate_question_to_sql("Show total revenue grouped by customer region", schema)
    assert "SELECT" in res.generated_sql.upper()
    assert "GROUP BY" in res.generated_sql.upper()
    rows = conn.execute(res.generated_sql).fetchall()
    assert len(rows) >= 2
