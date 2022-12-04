from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import oauth2_schema, get_current_user
from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay, UserBase

# It's all routes for users
# We call in this file the db functions for users tale / models (cf db_user.py)

router = APIRouter(
    prefix='/article',
    tags=['article']
)


@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)


# @router.get('/{id}', response_model=ArticleDisplay)
# def get_article(id: int, db: Session = Depends(get_db)):
#     return db_article.get_article(db, id)


@router.get('/{id}') #, response_model=ArticleDisplay)
def get_article_endpoint(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }
