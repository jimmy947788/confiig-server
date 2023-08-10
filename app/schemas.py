from pydantic import BaseModel
from datetime import datetime


class ConfigBase(BaseModel):
    app_name: str
    app_env: str
    srv_name: str | None = None
    conf_key: str
    
class Config(ConfigBase):
    conf_value: str | None = None
    description: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
