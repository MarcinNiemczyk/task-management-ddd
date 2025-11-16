from abc import ABC, abstractmethod


class IEventPublisher(ABC):
    @abstractmethod
    def publish(self, events: list[object]):
        pass
