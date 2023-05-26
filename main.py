from fastapi import FastAPI
from routers import blog, auth_router


app = FastAPI(
    title="Blog app"
)

app.include_router(blog.router)
app.include_router(auth_router.router)

