"""Creates and seeds an in-memory or file-backed analytical SQLite database for testing and demos."""

from __future__ import annotations
import sqlite3


def create_sample_analytics_db(db_path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            region TEXT NOT NULL,
            tier TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_cost REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )

    cur.executemany(
        "INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?)",
        [
            (1, "Apex Cloud Corp", "South", "Enterprise"),
            (2, "NovaGrid Energy", "South", "Enterprise"),
            (3, "Vertex FinTech", "Southeast", "Enterprise"),
            (4, "meridian Retail", "Southeast", "Mid-Market"),
            (5, "Horizon Logistics", "North", "Mid-Market"),
            (6, "Pulse Health Systems", "South", "Enterprise"),
        ],
    )

    cur.executemany(
        "INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)",
        [
            (10, "Enterprise Data Warehouse Node", "Cloud Infrastructure", 1200.0),
            (20, "Real-Time BI Connector License", "Analytics & BI", 450.0),
            (30, "Automated ETL Pipeline Pro", "Data Engineering", 680.0),
            (40, "SQL Governance & Audit Suite", "Security & Compliance", 520.0),
        ],
    )

    cur.executemany(
        "INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)",
        [
            (1001, 1, "2026-05-12", "COMPLETED", 14800.00),
            (1002, 2, "2026-06-04", "COMPLETED", 22400.00),
            (1003, 3, "2026-06-19", "COMPLETED", 19350.00),
            (1004, 4, "2026-07-08", "COMPLETED", 8900.00),
            (1005, 5, "2026-08-14", "COMPLETED", 6400.00),
            (1006, 6, "2026-09-02", "COMPLETED", 17600.00),
            (1007, 1, "2026-10-01", "COMPLETED", 16200.00),
            (1008, 2, "2026-10-15", "PENDING", 5400.00),
        ],
    )

    cur.executemany(
        "INSERT OR REPLACE INTO order_items VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1001, 10, 5, 2400.0),
            (2, 1001, 20, 4, 700.0),
            (3, 1002, 10, 8, 2400.0),
            (4, 1002, 30, 4, 800.0),
            (5, 1003, 20, 15, 950.0),
            (6, 1004, 40, 10, 890.0),
            (7, 1005, 30, 8, 800.0),
            (8, 1006, 10, 6, 2400.0),
            (9, 1007, 40, 18, 900.0),
        ],
    )

    conn.commit()
    return conn
