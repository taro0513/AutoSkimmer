from pydantic_settings import BaseSettings


class Config(BaseSettings):
    JOB_SCHEDULER_DB: str
    TASK_DB: str

    class Config:
        env_file = '.env'


config = Config()
