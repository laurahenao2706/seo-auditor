from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .models import AuditContext, RuleResult


class HttpClient(ABC):
    @abstractmethod
    def request(self, method: str, url: str, allow_redirects: bool = True) -> Any:
        raise NotImplementedError


class UrlNormalizer(ABC):
    @abstractmethod
    def normalize(self, value: str) -> str:
        raise NotImplementedError


class AuditRuleEngine(ABC):
    @abstractmethod
    def evaluate(self, context: AuditContext) -> list[RuleResult]:
        raise NotImplementedError
