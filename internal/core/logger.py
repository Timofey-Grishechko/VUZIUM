import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, ClassVar

from .config import settings
from .context import get_request_id, get_user_id


class JSONFormatter(logging.Formatter):
    """Formats the log entry as JSON."""
    

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.record.getMessage(),
        }
        
        #request_id and user_id from context
        request_id = get_request_id()
        if request_id:
            payload["request_id"] = request_id
            
        user_id = get_user_id()
        if user_id:
            payload["user_id"] = user_id

        for key, value in record.__dict__.items():
            if key.startswith("ctx_"):
                payload[key[4:]] = value
        
        # Traceback error
        if record.exc_info:
            payload["exceprion"] = self.formatException(record.exc_info)
        
        # Code's place
        payload["location"] = f"{record.filename}:{record.lineno}"
        
        return json.dumps(payload, ensure_ascii=False, default=str)
    

class DevFormatter(logging.Formatter):
    """Humanity format for dev"""
    
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        req = get_request_id() or "-"
        return (
            f"{color}{record.levelname:<8}{self.RESET} "
            f"{ts} [{req[:8]}] "
            f"{record.name}: {record.getMessage()}"
        )


def setup_logging() -> None:
    """Configures the root logger. Called once at application startup."""
    root = logging.getLogger()
    
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    
    handler = logging.StreamHandler(sys.stdout)
    
    if settings.env == "local":
        handler.setFormatter(DevFormatter())
        level = logging.DEBUG
    else:
        handler.setFormatter(JSONFormatter())
        level = logging.INFO
        
    root.addHandler(handler)
    root.setLevel(level)
    
    logging.getLogger("unicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Returning logger"""
    return logging.getLogger(name)
    