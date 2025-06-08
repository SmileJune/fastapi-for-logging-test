import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic 모델 예시
class Item(BaseModel):
    name: str
    description: str | None = None

# 헬스 체크 엔드포인트
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 예시 API 엔드포인트
@app.post("/items/")
def create_item(item: Item):
    logger.info(f"Received item: {item}")
    return {"item": item}

# 에러 핸들링 예시
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return {"error": exc.detail}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return {"error": "Internal server error"}

# 환경 변수 사용 예시
@app.get("/env")
def get_env():
    example_var = os.getenv("EXAMPLE_VAR", "not set")
    return {"EXAMPLE_VAR": example_var} 