from abc import ABC, abstractmethod

from core.models.schemas import ReportSchema


class ParsingStrategy(ABC):
    @abstractmethod
    def parse(self, content: str) -> ReportSchema:
        pass
