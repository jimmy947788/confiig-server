from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


def generate_uuid():
    return str(uuid.uuid4())

class Config(Base):
    __tablename__ = "configs"

    uuid = Column(String(100), name="uuid", primary_key=True, index=True, default=generate_uuid)
    app_name = Column(String(100), nullable=False, index=True)
    app_env = Column(String(100), nullable=False, index=True)
    srv_name = Column(String(100), nullable=True, index=True)
    conf_key = Column(String(100), nullable=False, index=True)
    conf_value = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at =Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False, server_default=text('False'))
    