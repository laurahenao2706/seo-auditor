from __future__ import annotations

import re
from urllib.parse import urlparse

from seo_auditor.domain.protocols import UrlNormalizer


class BasicUrlNormalizer(UrlNormalizer):
    def normalize(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            return ""
        if not re.match(r"^https?://", value, flags=re.I):
            value = "https://" + value
        parsed = urlparse(value)
        if not parsed.netloc:
            return ""
        return value
