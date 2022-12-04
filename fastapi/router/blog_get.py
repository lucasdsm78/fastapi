from fastapi import APIRouter, status, Response, Depends
from enum import Enum
from router.blog_post import require_functionality
from typing import Optional

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

@router.get(
    '/all',
    summary="Retrieve all blogs",
    description="This api call simulates fetching all blogs",
    response_description="The list of available blogs"
)
def get_all_blogs(page=1, page_size: Optional[int] = None, req_parameters: dict = Depends(require_functionality)):
    return {'message': f'All {page_size} blogs on page {page}', 'req': req_parameters}


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@router.get('/blog/type/{type}')
def get_blog_type(type: BlogType):
    return {'message': f'Blog type {type}'}


@router.get('/{id}/comments/{comment_id}')
def get_comment(id:int, comment_id:int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retreving a comment of a string
    - **id** mandatory path parameter
    """
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Blog with id {id}'}
