from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session

from typing import Optional
import crud, models, schemas
from database import SessionLocal, engine

# from propan import RabbitBroker
# from propan.fastapi import RabbitRouter

from typing_extensions import Annotated

from loguru import logger
from datetime import datetime
import configs


logger.add(f"./logs/{configs.APP_NAME}.log", rotation="12:00", encoding="utf-8", enqueue=True, retention="10 days")


models.Base.metadata.create_all(bind=engine)

# # create RabbitRouter
# router = RabbitRouter("amqp://guest:guest@rabbitmq.local:5672", setup_state=False)
# def broker():
#     return router.broker

app = FastAPI() #lifespan=router.lifespan_context

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/configs/", response_model=schemas.Config)
async def create_config(config: schemas.Config, db: Session = Depends(get_db)):
    try:
        db_config = crud.get_config_by_key(db=db, 
                                            app_name=config.app_name,
                                            app_env=config.app_env,
                                            conf_key=config.conf_key)
        if db_config:
            raise HTTPException(status_code=400, detail="Config already exists")       
        return crud.create_config(db=db, config=config)
    except Exception as ex:
        logger.error(ex)
        raise ex


@app.put("/configs/", response_model=schemas.Config)
async def update_config(config: schemas.Config, db: Session = Depends(get_db)):
    try:
        db_config = crud.get_config_by_key(db=db, 
                                app_name=config.app_name,
                                app_env=config.app_env,
                                conf_key=config.conf_key)
        if not db_config:
            raise HTTPException(status_code=404, detail="Hero not found")
        
        db_config.conf_value = config.conf_value
        db_config.description = config.description
        db_config.is_active = config.is_active
        db_config.updated_at = datetime.now()
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config
    except Exception as ex:
        logger.error(ex)
        raise ex

@app.get("/configs", response_model=schemas.ConfigBase)
async def get_configs(app_name: str, app_env: str,
                    srv_name: Optional[str] = None,
                    db: Session = Depends(get_db)):
    try:
        db_configs = crud.get_configs(db=db, app_name=app_name, app_env=app_env, srv_name=srv_name)
        if db_configs is None:
            raise HTTPException(status_code=404, detail="Config not found")
        # return db_config to json format
        json_compatible_item_data = jsonable_encoder(db_configs)
        return JSONResponse(content=json_compatible_item_data)
    except Exception as ex:
        logger.error(ex)
        raise ex

@app.get("/configs.env", response_class=PlainTextResponse)
async def get_configs_by_appenv_to_env_file(app_name: str, app_env: str, 
                    srv_name: Optional[str] = None,
                    db: Session = Depends(get_db)):
    try:
        db_configs = crud.get_configs(db=db, app_name=app_name, app_env= app_env, srv_name=srv_name)
        if db_configs is None:
            raise HTTPException(status_code=404, detail="Config not found")
        str_env = ""
        for config in db_configs:
            str_env += f"{config.conf_key}={config.conf_value}\n"
        return str_env
    except Exception as ex:
        logger.error(ex)
        raise ex
    

# define a route handler for the default home page
# @router.get("/publish/{message}", response_class=PlainTextResponse)
# async def hello_http(message: str):
#     # get current time string formatted yyyy/mm/dd hh:mm:ss
#     now = datetime.now()
#     current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    
#     await router.broker.publish(f"[{current_time}] Hello, {message}", "test_queue")
#     return "Hello, HTTP!"

## add RabbitRouter to FastAPI
#app.include_router(router)