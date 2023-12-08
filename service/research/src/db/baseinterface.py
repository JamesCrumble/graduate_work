from abc import ABC, abstractmethod


class DbInterface(ABC):
    INTERFACE_NAME = 'Интерфейс для работы с БД'

    @abstractmethod
    def prepare(self):
        ...

    @abstractmethod
    def write(self, data: dict):
        ...

    @abstractmethod
    def read(self, id: str):
        ...

    def __init__(self) -> None:
        super().__init__()
        self.prepare()
