from fastapi import FastAPI

from src.core.config import settings
from src.db.session import engine
from src.db.base import Base
from src.apis.base import api_router

def create_tables():
    Base.metadata.create_all(bind=engine)

def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI(
        title = settings.TITLE,
        version = settings.VERSION,
        description = settings.DESCRIPTION,
        contact = {"name": settings.NAME, "email": settings.EMAIL },
        # openapi_tags = tags,
        openapi_url="/api/v1/openapi.json",
        max_size = 3221225472,
    )
    create_tables()
    include_router(app)
    return app

app = start_application()




# @app.get('/user', tags=["user"])
# def get_user():
#     return {"message" : "hello user"}

# @app.get('/product', tags=["product"])
# def get_product():
#     return {"message" : "hello Product"}

# @app.get('/getenvvar', tags=["config"])
# def get_envvars():
#     return {"database" : setting.TITLE}



# uvicorn main:app --host 0.0.0.0 --port 7443 --reload

# gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon
# -k uvicorn.workers.UvicornWorker: Uvicorn worker 클래스를 사용합니다.
# –access-logfile ./gunicorn-access.log: Gunicorn 로그 파일을 기록합니다.
# main:app: main.py의 app을 실행합니다.
# -workers 2: worker process의 개수를 설정합니다. 통상 CPU 코어 개수 * 2로 설정합니다!
# –daemon: Gunicorn을 백그라운드 데몬 상에서 구동합니다.
# –bind 0.0.0.0:8000: 8000 포트에 서버를 연결합니다. 예를 들어 8000포트로 bind 한다면 사용자는 <서버주소>:8000으로 서버에 접속이 가능합니다.




