from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_PSYCOPG_URL")

ENGINE = create_engine(url=DATABASE_URL)

with ENGINE.connect() as connection:
    try:
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS "ragApp"'))
        connection.commit()
        print("Schema 'rag_app' ensured.")
    except Exception as e:
        print(f"Error creating schema: {e}")

SESSION = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)

def get_pg_db():
    session = SESSION()
    try:
        yield session
    finally:
        session.close()