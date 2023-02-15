from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.users import router as users_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)