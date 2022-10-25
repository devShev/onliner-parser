from pydantic import BaseSettings


class Settings(BaseSettings):
    parse_history: bool = True
    parse_spec: bool = True
