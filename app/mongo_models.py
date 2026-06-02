from beanie import Document
from pydantic import Field
from typing import Optional

class LogEntry(Document):
    event: str
    level: str ="INFO"
    metadata: dict = Field(default_factory=dict)

class Settings:
    name = "log_entries"