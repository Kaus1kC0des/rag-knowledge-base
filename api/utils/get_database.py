from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..schemas.postgres import *
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URL")