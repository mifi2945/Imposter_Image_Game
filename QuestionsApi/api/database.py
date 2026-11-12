import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from objects.question import Question


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _connection_parameters() -> dict[str, str | int]:
    password = os.getenv("PGPASSWORD")
    if password is None:
        raise RuntimeError("PGPASSWORD environment variable must be set")

    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "dbname": os.getenv("PGDATABASE", "questions"),
        "user": os.getenv("PGUSER", "questions"),
        "password": password,
    }


async def apply_migrations() -> None:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT pg_advisory_xact_lock(5201, 1)")
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            await cursor.execute("SELECT version FROM schema_migrations")
            applied_versions = {row[0] for row in await cursor.fetchall()}

            for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
                version = migration.stem
                if version in applied_versions:
                    continue

                await cursor.execute(migration.read_text(encoding="utf-8"))
                await cursor.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (version,),
                )


async def create_question(category: str, question: str) -> Question:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO categories (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                """,
                (category,),
            )
            await cursor.execute(
                """
                INSERT INTO questions (category, question)
                VALUES (%s, %s)
                RETURNING id, category, question
                """,
                (category, question),
            )
            return Question(**(await cursor.fetchone()))


async def get_questions(category: str | None = None) -> list[Question]:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            if category is None:
                await cursor.execute(
                    "SELECT id, category, question FROM questions ORDER BY id"
                )
            else:
                await cursor.execute(
                    """
                    SELECT id, category, question
                    FROM questions
                    WHERE category = %s
                    ORDER BY id
                    """,
                    (category,),
                )
            return [Question(**row) for row in await cursor.fetchall()]

async def get_random_question(category: str) -> Question | None:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, category, question
                FROM questions
                WHERE category = %s
                ORDER BY RANDOM()
                LIMIT 1
                """,
                (category,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return Question(**row)

async def get_random_category() -> str | None:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                SELECT category
                FROM questions
                ORDER BY RANDOM()
                LIMIT 1
                """
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return row[0]


async def delete_question(question_id: int) -> bool:
    async with await psycopg.AsyncConnection.connect(
        **_connection_parameters()
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM questions WHERE id = %s",
                (question_id,),
            )
            return cursor.rowcount > 0
