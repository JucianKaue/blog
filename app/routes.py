from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.views import *

routes = [
   Route('/', endpoint=home_page),
   Route('/blog', endpoint=blog_page, methods=['GET', 'POST']),
   Route('/login', endpoint=login_page, methods=['GET', 'POST']),
   Route('/register', endpoint=register_page, methods=['GET', 'POST']),

   Route('/logout', endpoint=logout_function),

   Mount('/static', app=StaticFiles(directory='static'), name='static')
]

