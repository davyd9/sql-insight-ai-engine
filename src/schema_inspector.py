"""Database schema introspection and DDL metadata extraction module."""

from __future__ import annotations
import sqlite3
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class ColumnMeta(BaseModel):
    name: str
    data_type: str
    not_null: bool = False
    is_primary_key: bool = False


class TableMeta(BaseModel):
    table_name: str
    row_count: int = 0
    columns: List[ColumnMeta] = Field(default_factory=list)
    indexes: List[str] = Field(default_factory=list)
    ddl: str = ""


class DatabaseSchema(BaseModel):
    dialect: str = "sqlite"
    tables: List[TableMeta] = Field(default_factory=list)

    def to_prompt_context(self) -> str:
        lines = [f"-- Database Dialect: {self.dialect.upper()}"]
        for t in self.tables:
            cols = ", ".join(
                f"{c.name} {c.data_type}{' PRIMARY KEY' if c.is_primary_key else ''}"
                for c in t.columns
            )
            lines.append(f"TABLE {t.table_name} ({cols}) -- rows: {t.row_count}")
        return "\n".join(lines)


def inspect_sqlite_schema(conn: sqlite3.Connection) -> DatabaseSchema:
    """Introspects all user tables, columns, row counts, and indexes from a SQLite connection."""
    cur = conn.cursor()
    tables_raw = cur.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()

    tables: List[TableMeta] = []
    for t_name, ddl in tables_raw:
        col_rows = cur.execute(f"PRAGMA table_info('{t_name}')").fetchall()
        cols = [
            ColumnMeta(
                name=r[1],
                data_type=r[2] or "TEXT",
                not_null=bool(r[3]),
                is_primary_key=bool(r[5]),
            )
            for r in col_rows
        ]
        idx_rows = cur.execute(f"PRAGMA index_list('{t_name}')").fetchall()
        indexes = [r[1] for r in idx_rows]
        count_row = cur.execute(f"SELECT COUNT(*) FROM '{t_name}'").fetchone()
        row_count = int(count_row[0]) if count_row else 0

        tables.append(
            TableMeta(
                table_name=t_name,
                row_count=row_count,
                columns=cols,
                indexes=indexes,
                ddl=ddl or "",
            )
        )

    return DatabaseSchema(dialect="sqlite", tables=tables)
