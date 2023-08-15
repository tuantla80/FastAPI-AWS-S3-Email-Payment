from fastapi import FastAPI
import uvicorn

from resources.routes import api_router
from db import database


app = FastAPI()

app.include_router(api_router)


@app.on_event('startup')
async def startup():
   await database.connect()


@app.on_event('shutdown')
async def shutdown():
   await database.disconnect()


@app.get('/')
async def root():
   return {'message': 'Hellow World'}


if __name__ == '__main__':
   uvicorn.run(app, host='127.0.0.1')
