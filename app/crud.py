from sqlalchemy.orm import Session
import models, schemas
from loguru import logger

def get_configs(db: Session, app_name: str, app_env: str):
    return db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env) \
        .filter(models.Config.is_active == True) \
        .all()

def get_config_by_key(db: Session, app_name: str, app_env: str, conf_key: str):
    return db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env) \
        .filter(models.Config.conf_key == conf_key).first()

def create_config(db: Session, config: schemas.ConfigCreate):
    db_config = models.Config(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config
