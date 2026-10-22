# app/apis/practice_apis.py -> 특정 API 기능을 담당
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

# API 경로들을 모아서 관리하기 위한 객체
router = APIRouter()

user_list = [
	{
		"id": 1,
		"name": "홍길동",
		"age": 24,
		"email": "gildong24@example.com",
		"password": "Password1234!!"
	},
	{
		"id": 2,
		"name": "장문복",
		"age": 21,
		"email": "moonluck12@example.com",
		"password": "Check1321!"
	},
	{
		"id": 3,
		"name": "임우진",
		"age": 31,
		"email": "limousine33@example.com",
		"password": "lwsPAssword12@"
	}
]

# 아래 경로로 GET 요청 들어오면 바로 아래의 get_users() 함수가 실행되도록 설정
# endpoint = API를 호출할 때 사용하는 주소 경로 = "practice_api/users"
# 1번) 모든 회원 목록 조회 API
@router.get("/practice_api/users")
def get_users():
    return [
        {
            "id": user["id"],
            "name": user["name"],
            "age": user["age"],
            "email": user["email"],
        }
        for user in user_list
    ]

# 5번) 회원 정보 삭제 API
@router.delete("/practice_api/users/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(user_list):
        if user["id"] == user_id:
            del user_list[idx]
            return {"message": f"User [{user_id}] 성공적으로 삭제되었습니다."}
            
    # 유효한 id가 아닐 경우 404 에러 반환
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found"
    )