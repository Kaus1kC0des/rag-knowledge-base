from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from api.schemas.postgres import BASE, ChatSession, ChatMessage
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_PSYCOPG_URL")
print(DATABASE_URL)

ENGINE = create_engine(url=DATABASE_URL)

with ENGINE.connect() as connection:
    try:
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS "ragApp"'))
        connection.commit()
        print("Schema 'ragApp' ensured.")
    except Exception as e:
        print(f"Error creating schema: {e}")

BASE.metadata.create_all(bind=ENGINE)
if __name__ == "__main__":
    with ENGINE.connect() as connection:
        result = connection.execute(text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'rag_app';
            """
        ))
        tables = result.fetchall()
        print(f"Tables in 'rag_app' schema: {[table for table in tables]}")