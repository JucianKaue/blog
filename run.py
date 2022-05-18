import uvicorn

from starlette.applications import Starlette
from app.routes import routes


app = Starlette(debug=True, routes=routes, )

if __name__ == "__main__":
   uvicorn.run('run:app', host='127.0.0.1', reload=True, port=5000)
