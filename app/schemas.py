from pydantic import BaseModel
from datetime import datetime


class ConfigCreate(BaseModel):
    app_name: str
    app_env: str
    srv_name: str
    conf_key: str
    conf_value: str | None = None
    description: str | None = None

class Config(ConfigCreate):
    uuid: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
