from abc import ABC, abstractmethod


class basepit:
    def __init__(self, index, seeds, prev=None, back=None, active=True) -> None:
        self.storage = {
            "index": index,
            "active": active,
            "value": seeds,
            "prev": prev,
            "link": back,
            "reset": seeds,
            "capture": False,
        }

    def __getitem__(self, ppty):
        return self.storage.get(ppty, "Key not found!")

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def isCapture(self):
        pass
