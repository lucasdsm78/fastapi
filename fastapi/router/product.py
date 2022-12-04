from typing import Optional, List

from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from custom_log import log
import time

# It's all routes for users
# We call in this file the db functions for users tale / models (cf db_user.py)

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']


async def time_consuming_functionality():
    time.sleep(5)
    return 'ok'

# Example for form in FastAPI

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


# Example of custom response, return HTML Response

@router.get('/all')
async def get_all_products():
    await time_consuming_functionality()
    # return products
    data = " ".join(products)
    return Response(content=data, media_type="text/plain")


# here is an example to get all products and SET COOKIES

@router.get('/allcookies')
def get_all_productscookies():
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


# example to get products with Headers and GET COOKIES
@router.get('/withheaderandsetcookievalue')
def get_products(
        response: Response,
        custom_header: Optional[List[str]] = Header(None),
        test_cookie: Optional[str] = Cookie(None),

):
    if custom_header:
        response.headers['custom_response_header'] = ", ".join(custom_header)

    return {
        'data': products,
        'custom_header': custom_header,
        'my cookie': test_cookie
    }


# example to get products with Headers
@router.get('/withheader')
def get_products(
        response: Response,
        custom_header: Optional[str] = Header(None)
):
    return products


# example to get products with multiple Headers
@router.get('/withlistheader')
def get_products(
        response: Response,
        custom_header: Optional[List[str]] = Header(None)
):
    return products


# example to get products with custom Response Headers
@router.get('/withcustomresponsetheader')
def get_products(
        response: Response,
        custom_header: Optional[List[str]] = Header(None)
):
    response.headers['custom_response_header'] = ", ".join(custom_header)
    return products


# Return HTML response

@router.get('/{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available"
            }
        },
        "description": "A cleartext error message"
    }
})
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(content=out, media_type="text/plain", status_code=404)
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")
