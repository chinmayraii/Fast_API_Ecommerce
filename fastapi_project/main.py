from fastapi import FastAPI
from admin.apis import routes as AdminRoute
from tortoise.contrib.fastapi import register_tortoise
from configs.connection import DATABASE_URL


app=FastAPI()
db_url=DATABASE_URL()

app.include_router(AdminRoute.router,tags={'Admin'})


register_tortoise(
    app,
    db_url=db_url,
    modules={'models':['admin.apis.models']},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.get('/')
async def create_user():
    return ("Hello world")