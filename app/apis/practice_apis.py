from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

# FastAPI 앱 및 라우터 설정 (서버 실행을 위해 필수)
app = FastAPI()
router = APIRouter(prefix="/practice_api")
app.include_router(router)

# 과제에서 제공된 기본 유저 데이터
user_list = [
    {"id": 1, "name": "홍길동", "age": 24, "email": "gildong24@example.com", "password": "Password1234!!"},
    {"id": 2, "name": "장문복", "age": 21, "email": "moonluck12@example.com", "password": "Check1321!"},
    {"id": 3, "name": "임우진", "age": 31, "email": "limousine33@example.com", "password": "lwsPAssword12@"}
]

# 2번 요구사항: 응답 항목을 4개(id, name, age, email)로 제한하는 모델
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str

# 2번 요구사항: 특정 회원 조회 API 엔드포인트
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for u in user_list:
        if u["id"] == user_id:
            return u  # 일치하는 id가 있으면 해당 유저 정보 반환
            
    # 유효한 id가 아닐 경우 404 에러 반환
    raise HTTPException(status_code=404, detail="Not Found")
