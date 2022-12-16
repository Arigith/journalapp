from fastapi import FastAPI
from database import engine
from routers import journal, user, authentication
import models
# added import so Astro will work
from fastapi.middleware.cors import CORSMiddleware
# end addition

app=FastAPI()

# added for Astro
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# end additions

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(journal.router)