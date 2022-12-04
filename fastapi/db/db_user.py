from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from db.hash import Hash
from db.models import DbUser
from schemas import UserBase


# Create user and insert into database
def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


## We do query, insert with models (tables)
def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found')
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {username} not found')
    return user


def update_user(db: Session, user_id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == user_id)
    user.update({DbUser.username: request.username,
                 DbUser.email: request.email,
                 DbUser.password: Hash.bcrypt(request.password)})
    db.commit()
    return 'ok its updated'


def delete_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found')
    # Do try catch, handle exception
    db.delete(user)
    db.commit()
    return "ok its deleted"
