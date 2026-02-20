from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='APP_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    token: str


app_settings = AppSettings()  # type: ignore[call-arg]
