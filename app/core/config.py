import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Instant Refund API"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
    SIGNER_URL: str = os.getenv("SIGNER_URL", "http://instant-refund-signer:8080/sign")
    
    # THE CRITICAL LINK
    KASPAD_ADDRESS: str = "10.17.0.5" 
    KASPAD_PORT: int = 16110

settings = Settings()
