from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from API.Router.V1 import user_management_router


# FastApiAddress, FastApiport, socketIP, socketPort, mongoDBClient, mongoDBPort, TestingmongoDBClient, TestingmongoDBPort = readConfigServer()
# app = FastAPI(docs_url=None, redoc_url=None)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="a585b66e3989f473b1e8cd67b7b5fc3ac601146a62bbc5658ae8e5266aeb946d")

app.include_router(user_management_router.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





