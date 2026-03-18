from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class RuleResult:
    rule_id: int
    item: str
    status: str
    details: str
    recommendation: str
    automated: bool = True


@dataclass
class AuditContext:
    input_url: str
    normalized_url: str
    final_url: str
    base_origin: str
    response: Any
    soup: Any
    robots_url: str
    robots_response: Any
    sitemap_url: str
    sitemap_response: Any
    text_size: int
    ttfb: float
    total_fetch: float
    internal_links: list[str]
    image_urls: list[str]
    broken_link_count: int
    broken_link_examples: list[str]
    broken_image_count: int
    broken_image_examples: list[str]
    non_existing_url: str
    non_existing_response: Any
    image_weight_total_kb: float
    heavy_images: list[str]


@dataclass
class AuditReport:
    input_url: str
    normalized_url: str
    final_url: str
    generated_at: str
    summary: dict[str, int]
    results: list[RuleResult]

    @staticmethod
    def now() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_url": self.input_url,
            "normalized_url": self.normalized_url,
            "final_url": self.final_url,
            "generated_at": self.generated_at,
            "summary": self.summary,
            "results": [asdict(result) for result in self.results],
        }
