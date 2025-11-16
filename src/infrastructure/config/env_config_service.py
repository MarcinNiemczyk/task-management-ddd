import os

from src.application.ports.config_port import ConfigPort


class EnvConfigService(ConfigPort):
    def auto_complete_project_on_last_task_done(self) -> bool:
        value = os.getenv("AUTO_COMPLETE_PROJECT", "false").lower()
        return value in ("1", "true", "yes")
