from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import models, engine

# 创建数据库文件
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# 允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'])


