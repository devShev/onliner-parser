from pydantic import BaseSettings


class Settings(BaseSettings):
    parse_history: bool = False
    parse_spec: bool = False

    deep_parse_status: bool = False
