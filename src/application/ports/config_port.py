from abc import ABC, abstractmethod


class ConfigPort(ABC):
    @abstractmethod
    def auto_complete_project_on_last_task_done(self) -> bool:
        pass
