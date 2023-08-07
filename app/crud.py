from sqlalchemy.orm import Session
import models, schemas


def get_configs(db: Session, app_name: str, app_env: str):
    return db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env).all()

def get_config_by_key(db: Session, app_name: str, app_env: str, srv_name: str, conf_key: str):
    return db.query(models.Config) \
        .filter(models.Config.app_name == app_name) \
        .filter(models.Config.app_env == app_env) \
        .filter(models.Config.srv_name == srv_name) \
        .filter(models.Config.conf_key == conf_key).first()

def create_config(db: Session, config: schemas.ConfigCreate):
    db_config = models.Config(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config