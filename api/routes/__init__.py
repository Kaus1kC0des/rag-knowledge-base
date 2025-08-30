from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from api.utils.get_pg_database import get_pg_db
from api.utils.authenticate_user import authenticate_user
import logging