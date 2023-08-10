from pydantic import BaseModel
from datetime import datetime


class ConfigCreate(BaseModel):
    app_name: str
    app_env: str
    conf_key: str
    conf_value: str | None = None
    description: str | None = None
    is_active: bool = True

class ConfigUpdate(ConfigCreate):
    srv_name: str

class Config(ConfigUpdate):
    uuid: str
    created_at: datetime
    updated_at: datetime
