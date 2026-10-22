# main.py -> Application의 진입점 역할
import os # 운영체제의 파일, 폴더 관련 기능 사용
from pathlib import Path # 파일 및 폴더 경로를 객체로 관리

from fastapi import FastAPI # API 서버 생성
from starlette.staticfiles import StaticFiles # CSS, JS, 이미지 등 정적 파일 제공
from starlette.responses import FileResponse # 특정 파일을 HTTP 응답으로 반환
from app.apis.practice_apis import router as practice_router

app = FastAPI()

# 프로젝트 기준 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
# __file__ : 현재 실행 중인 Python 파일의 경로
# .resolve(): 절대 경로로 변환
# .parent: 현재 파일이 들어 있는 폴더
# .parent.parent: 그 상위 폴더
# -> BASE_DIR = Oz_codingSchool 폴더를 가리킴

# 만약 static, media 폴더가 존재하지 않으면 생성
if not (BASE_DIR / "static").exists():
    os.mkdir(BASE_DIR / "static")
if not (BASE_DIR / "media").exists():
    os.mkdir(BASE_DIR / "media")

# mount() = 특정 URL 경로를 특정 폴더와 연결
# 'static' 폴더를 '/static' 경로로 마운트 (CSS, JS 파일 서빙용)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
# 'media' 폴더를 '/media' 경로로 마운트 (사용자 업로드 파일 서빙용)
app.mount("/media", StaticFiles(directory=BASE_DIR / "media"), name="media")

# GET 요청을 처리할 경로 등록 / 정상 응답 상태 코드 지정 / Swagger 문서에서 해당 경로 숨김
@app.get(path="/healthcheck", status_code=200, include_in_schema=False)
# 비동기 함수 정의
async def healthcheck():
    return {"status": "ok"}

# 메인 페이지 반환 - 브라우저에서 서버의 루트 주소(/)에 접근하면 static/index.html 파일을 반환
@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")

# 실습 API 라우터 등록
app.include_router(practice_router)

# 나머지 경로 처리 (catch_all)
@app.get("/{path:path}", include_in_schema=False)
async def catch_all(path: str):
    # API나 정적 파일 경로는 제외 (FastAPI가 먼저 매칭하지 못한 경우에만 실행됨)
    if (
        path.startswith("api/v1")
        or path.startswith("static/")
        or path.startswith("media/")
    ):
        from fastapi import HTTPException

        raise HTTPException(status_code=404)
    return FileResponse(BASE_DIR / "static" / "index.html")
