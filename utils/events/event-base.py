from abc import ABC, abstractmethod


class BaseEventClass(ABC):
    @abstractmethod
    def register(self, event_type, callback):
        pass

    @abstractmethod
    def notify(self, event_type, *args, **kwargs):
        """Broadcast event with flexible arguments."""
        pass
