import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Instant Refund API"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
    SIGNER_URL: str = os.getenv("SIGNER_URL", "http://instant-refund-signer:8080/sign")
    
    # SWITCHING TO PUBLIC IP (Front Door)
    KASPAD_ADDRESS: str = "159.203.168.9" 
    KASPAD_PORT: int = 16110

settings = Settings()
