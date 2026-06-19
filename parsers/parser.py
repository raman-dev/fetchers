from abc import ABC,abstractmethod
from enum import Enum

class Parser(ABC):
    @abstractmethod
    def parse(self,source,parseType):
        pass

    