from __future__ import annotations

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from seo_auditor.domain.protocols import HttpClient

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class RequestsHttpClient(HttpClient):
    def __init__(self, timeout: int = 12) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
            }
        )

    def request(self, method: str, url: str, allow_redirects: bool = True) -> requests.Response | None:
        try:
            return self.session.request(method, url, timeout=self.timeout, allow_redirects=allow_redirects)
        except requests.exceptions.SSLError:
            try:
                return self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    allow_redirects=allow_redirects,
                    verify=False,
                )
            except requests.RequestException:
                return None
        except requests.RequestException:
            return None
