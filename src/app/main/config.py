from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str

    @property
    def dsn_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_URI}"
    
    @property
    def dsn_psycopg(self):
        return f"postgresql+psycopg://{self.DB_URI}"


settings = Settings()
