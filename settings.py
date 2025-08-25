import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    bot_token: str
    admin_chat_id: str
    base_dir: str = os.path.dirname(os.path.dirname(__file__))

    DB_NAME: str
    DB_ENGINE: str

    APP_NAME: str = "neonavt_tg_bot"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


    def send_msg_url(self, text: str) -> str:
        return (f"https://api.telegram.org/bot{self.bot_token}/"
                f"sendMessage?chat_id={self.admin_chat_id}&text={text}")

    class Config:
        env_file = ".env"



settings = Settings()