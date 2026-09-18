from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "local"
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()