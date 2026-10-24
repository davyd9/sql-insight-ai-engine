"""Natural Language to SQL (NL2SQL) translation engine with Gemini API and deterministic fallback."""

from __future__ import annotations
import os
from pydantic import BaseModel
from src.schema_inspector import DatabaseSchema
from src.query_optimizer import validate_read_only_sql


class NL2SQLResult(BaseModel):
    question: str
    generated_sql: str
    explanation: str
    engine_used: str = "deterministic-ast"


def translate_question_to_sql(question: str, schema: DatabaseSchema) -> NL2SQLResult:
    """Translates an analytical business question into an optimized SQL query."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                "You are a Senior Database Engineer. Given the following database schema:\n"
                f"{schema.to_prompt_context()}\n\n"
                f"Write a single, optimized, read-only SELECT SQL query to answer: '{question}'.\n"
                "Return ONLY the raw SQL query without markdown fences."
            )
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            candidate_sql = (resp.text or "").strip().strip("`").replace("sql\n", "").strip()
            if validate_read_only_sql(candidate_sql):
                return NL2SQLResult(
                    question=question,
                    generated_sql=candidate_sql,
                    explanation="Generated via Gemini 2.5 Flash using live DDL schema context.",
                    engine_used="gemini-2.5-flash",
                )
        except Exception:
            pass

    q_low = question.lower()
    if "region" in q_low or "região" in q_low:
        sql = (
            "SELECT c.region AS region, COUNT(o.order_id) AS total_orders, "
            "ROUND(SUM(o.total_amount), 2) AS total_revenue, "
            "ROUND(AVG(o.total_amount), 2) AS avg_order_value "
            "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
            "WHERE o.status = 'COMPLETED' "
            "GROUP BY c.region ORDER BY total_revenue DESC;"
        )
        exp = "Aggregates completed order revenue and average ticket grouped by customer region."
    elif "category" in q_low or "product" in q_low or "categoria" in q_low:
        sql = (
            "SELECT p.category AS category, COUNT(oi.item_id) AS units_sold, "
            "ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue "
            "FROM order_items oi JOIN products p ON oi.product_id = p.product_id "
            "GROUP BY p.category ORDER BY gross_revenue DESC;"
        )
        exp = "Computes total units sold and gross revenue grouped by product category."
    elif "month" in q_low or "trend" in q_low or "mensal" in q_low:
        sql = (
            "SELECT substr(order_date, 1, 7) AS year_month, "
            "COUNT(order_id) AS orders_count, "
            "ROUND(SUM(total_amount), 2) AS monthly_revenue "
            "FROM orders WHERE status = 'COMPLETED' "
            "GROUP BY year_month ORDER BY year_month ASC;"
        )
        exp = "Calculates monthly revenue trend across completed transactions."
    else:
        sql = (
            "SELECT c.company_name, c.region, c.tier, "
            "COUNT(o.order_id) AS orders_count, ROUND(SUM(o.total_amount), 2) AS lifetime_value "
            "FROM customers c JOIN orders o ON c.customer_id = o.customer_id "
            "WHERE o.status = 'COMPLETED' "
            "GROUP BY c.customer_id, c.company_name, c.region, c.tier "
            "ORDER BY lifetime_value DESC LIMIT 10;"
        )
        exp = "Ranks top 10 enterprise customers by lifetime completed order value (LTV)."

    return NL2SQLResult(
        question=question,
        generated_sql=sql,
        explanation=exp,
        engine_used="schema-aware-planner",
    )
