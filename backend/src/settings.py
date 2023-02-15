from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Настройки приложения """

    jwt_secret: str = "suhushu2uuy2h232819msby222h2y327bd7s68u9usdy7678698sdy8y7867sdy09"
    jwt_algorithm: str = "HS256"
    jwt_expires: int = 24 #Hours


settings = Settings()