from sqlalchemy.orm import Session
import models, schemas
from loguru import logger

def get_configs(db: Session, app_name: str, app_env: str,  srv_name: str| None = None):
    result =  db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env)
    if srv_name:
        result = result.filter(models.Config.srv_name == srv_name)
    return result.filter(models.Config.is_active == True).all()

def get_config_by_key(db: Session, app_name: str, app_env: str, conf_key: str):
    return db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env) \
        .filter(models.Config.conf_key == conf_key).first()

def create_config(db: Session, config: schemas.Config):
    db_config = models.Config(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config
