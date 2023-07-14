import uvicorn
from fastapi import FastAPI

import models
from database import engine
from routers.auth import auth_router
from routers.recipes import recipe_router
from routers.users import users_router

app = FastAPI(docs_url='/')
app.include_router(users_router)
app.include_router(recipe_router)
app.include_router(auth_router)
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
