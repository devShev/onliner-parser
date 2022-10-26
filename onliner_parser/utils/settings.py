from pydantic import BaseSettings


class Settings(BaseSettings):
    parse_history: bool = True
    parse_spec: bool = True

    deep_parse_status: bool = False
