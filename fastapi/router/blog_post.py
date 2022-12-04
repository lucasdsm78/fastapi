from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    nb_comments: int
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version
    }


# @router.post('/new/{id}/comment')
# def create_comment(blog: BlogModel, id: int, comment_id: int = Query(None,
#                                                                      title='Id of the comment',
#                                                                      alias='commentId',
#                                                                      deprecated=True,
#                                                                      description='Some description for comment_id'),
#                    content: str = Body(..., min_length=10, max_length=12, regex='^[a-z\s]*$'),
#                    v: Optional[List[str]] = Query(['1.0', '1.1', '1.2'])
#                    ):
#     return {
#         'blog': blog,
#         'id': id,
#         'content': content,
#         'comment_id': comment_id,
#         'version': v
#     }

@router.post('/new/{id}/comment/comment_{id')
def create_comment(blog: BlogModel, id: int, comment_title: int = Query(None,
                                                                        title='Title of the comment',
                                                                        alias='commentTitle',
                                                                        deprecated=True,
                                                                        description='Some description for comment_title'),
                   content: str = Body(..., min_length=10, max_length=12, regex='^[a-z\s]*$'),
                   v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']),
                   comment_id: int = Path(None, gt=5, le=10)
                   ):
    return {
        'blog': blog,
        'id': id,
        'content': content,
        'comment_title': comment_title,
        'comment_id': comment_id,
        'version': v
    }


def require_functionality():
    return {'message': 'Learning fastAPI is important'}
