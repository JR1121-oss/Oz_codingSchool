# app/apis/practice_apis.py -> 특정 API 기능을 담당
from fastapi import APIRouter

router = APIRouter() # API 경로들을 모아서 관리하기 위한 객체

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
@router.get("/practice_api/users")
def get_users():
    # 조회할 항목만 반환하기
    return [
        {
            "id": user["id"],
            "name": user["name"],
            "age": user["age"],
            "email": user["email"]
        }
        for user in user_list
	]
