from api.models.user_model import UserEditModel, UserModel
from api.schemas.postgres import Users
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import NoReferenceError

def get_user_by_id(user_id: str, db: Session):
    try:
        db_user = db.query(Users).filter(Users.id == user_id).first()
        if not db_user:
            raise NoReferenceError("User not found")
    except Exception as e:
        raise e
    else:
        return db_user


def create_user(user: UserModel, db: Session):
    try:
        if_user_exists = db.query(Users).filter(Users.id == user.id).first()
        if if_user_exists:
            raise HTTPException(status_code=400, detail="User already exists")
        db_user = Users(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise e

def update_user(user_id: str, user: UserEditModel, db: Session):
    try:
        db_user = db.query(Users).filter(Users.id == user_id).first()
        if not db_user:
            raise NoReferenceError("User not found")
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise e

def delete_user(user_id: str, db: Session):
    try:
        db_user = db.query(Users).filter(Users.id == user_id).first()
        if not db_user:
            raise NoReferenceError("User not found")
        db.delete(db_user)
        db.commit()
        return {"detail": "User deleted successfully", "user": db_user.model_dump_json()}
    except Exception as e:
        raise e