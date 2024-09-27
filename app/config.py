from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PASSWORD: str
    API_USERNAME: str

    class Config:
        env_file = ".env"
        
settings = Settings()