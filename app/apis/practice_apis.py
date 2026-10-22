# app/apis/practice_apis.py

import re
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator

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

router = APIRouter(prefix="/practice_api", tags=["practice_api"])

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_password(value: str) -> str:
    if not 8 <= len(value) <= 20:
        raise ValueError("비밀번호는 8자 이상 20자 이하여야 합니다.")
    if not re.search(r"[A-Z]", value):
        raise ValueError("비밀번호에는 대문자가 1개 이상 필요합니다.")
    if not re.search(r"[a-z]", value):
        raise ValueError("비밀번호에는 소문자가 1개 이상 필요합니다.")
    if not re.search(r"[^A-Za-z0-9\s]", value):
        raise ValueError("비밀번호에는 특수문자가 1개 이상 필요합니다.")
    return value


def validate_email(value: str) -> str:
    if len(value) > 30:
        raise ValueError("이메일은 30자 이하여야 합니다.")
    if not EMAIL_PATTERN.match(value):
        raise ValueError("이메일 형식이 올바르지 않습니다.")
    return value


class UserUpdate(BaseModel):
    age: Optional[int] = Field(default=None, ge=14)
    email: Optional[str] = None
    password: Optional[str] = None

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        return value if value is None else validate_email(value)

    @field_validator("password")
    @classmethod
    def check_password(cls, value):
        return value if value is None else validate_password(value)


@router.patch("/users/{user_id}")
def update_user(user_id: int, body: UserUpdate):
    # 1) 회원 찾기 (없으면 404)
    user = next((u for u in user_list if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 회원입니다.")

    # 2) 아무것도 안 보냈으면 400
    if body.age is None and body.email is None and body.password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 항목을 하나 이상 입력해야 합니다.")

    # 3) 보낸 것만 반영
    if body.age is not None:
        user["age"] = body.age
    if body.email is not None:
        user["email"] = body.email
    if body.password is not None:
        user["password"] = body.password

    # 4) 비밀번호는 빼고 응답
    return {"id": user["id"], "name": user["name"], "age": user["age"], "email": user["email"]}