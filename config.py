from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Portalz Users FastAPI"
    supabase_url: str
    supabase_key: str
    salt: str

    class Config:
        env_file = ".env"
