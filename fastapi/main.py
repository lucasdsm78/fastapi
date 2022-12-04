import time

from fastapi import FastAPI, Request, HTTPException

from db import models
from db.database import engine
from templates import templates
from exceptions import StoryException
from router import blog_get, article
from router import user
from router import blog_post
from router import product
from router import file
from auth import authentication
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Add all routers

app.include_router(templates.router)
app.include_router(blog_get.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(file.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(product.router)


@app.get('/hello')
def index():
    return {'message': 'Hello world!'}


# create the database and import models

models.Base.metadata.create_all(engine)


# add a middleware to intercepts the request and the response
# it can access to all related info

@app.middleware("http")
async def add_midleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


# If we change the structure of the table, we should delete the db file
# and run the server

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exception: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exception.name}
    )


@app.exception_handler(HTTPException)
def custom_handler(request: Request, exception: StoryException):
    return PlainTextResponse(str(exception), status_code=400)


# @app.get('/blog/all')
# def get_all_blogs():
#     return {'message': 'All blogs provided'}

app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static', StaticFiles(directory="templates/static"), name='static')
