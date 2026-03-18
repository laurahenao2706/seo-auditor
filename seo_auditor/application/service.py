from __future__ import annotations

import time
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

from seo_auditor.application.normalizer import BasicUrlNormalizer
from seo_auditor.application.rule_engine import ChecklistRuleEngine
from seo_auditor.domain.exceptions import FetchError, InvalidUrlError
from seo_auditor.domain.models import AuditContext, AuditReport, RuleResult
from seo_auditor.domain.protocols import AuditRuleEngine, HttpClient, UrlNormalizer
from seo_auditor.infrastructure.http_client import RequestsHttpClient


class SeoAuditService:
    def __init__(
        self,
        http_client: HttpClient | None = None,
        normalizer: UrlNormalizer | None = None,
        rule_engine: AuditRuleEngine | None = None,
        sample_size: int = 25,
    ) -> None:
        self.http_client = http_client or RequestsHttpClient()
        self.normalizer = normalizer or BasicUrlNormalizer()
        self.rule_engine = rule_engine or ChecklistRuleEngine(self.http_client)
        self.sample_size = sample_size

    def analyze(self, input_url: str) -> dict:
        normalized = self.normalizer.normalize(input_url)
        if not normalized:
            raise InvalidUrlError("La URL no es valida. Incluye dominio, por ejemplo https://www.ejemplo.com")

        start_time = time.perf_counter()
        response = self.http_client.request("GET", normalized, allow_redirects=True)
        if response is None:
            raise FetchError("No fue posible descargar la URL principal.")

        final_url = response.url
        parsed_final = urlparse(final_url)
        base_origin = f"{parsed_final.scheme}://{parsed_final.netloc}"
        soup = BeautifulSoup(response.text or "", "html.parser")

        robots_url = urljoin(base_origin, "/robots.txt")
        robots_response = self.http_client.request("GET", robots_url, allow_redirects=True)

        sitemap_url = urljoin(base_origin, "/sitemap.xml")
        sitemap_response = self.http_client.request("GET", sitemap_url, allow_redirects=True)

        internal_links = self._collect_internal_links(soup, base_origin)
        image_urls = self._collect_images(soup, base_origin)

        broken_link_count, broken_link_examples = self._check_broken_resources(internal_links)
        broken_image_count, broken_image_examples = self._check_broken_resources(image_urls)

        non_existing_url = self._build_non_existing_url(base_origin)
        non_existing_response = self.http_client.request("GET", non_existing_url, allow_redirects=True)

        image_weight_total_kb, heavy_images = self._check_image_weight(image_urls)

        context = AuditContext(
            input_url=input_url,
            normalized_url=normalized,
            final_url=final_url,
            base_origin=base_origin,
            response=response,
            soup=soup,
            robots_url=robots_url,
            robots_response=robots_response,
            sitemap_url=sitemap_url,
            sitemap_response=sitemap_response,
            text_size=len(soup.get_text(" ", strip=True)),
            ttfb=response.elapsed.total_seconds(),
            total_fetch=time.perf_counter() - start_time,
            internal_links=internal_links,
            image_urls=image_urls,
            broken_link_count=broken_link_count,
            broken_link_examples=broken_link_examples,
            broken_image_count=broken_image_count,
            broken_image_examples=broken_image_examples,
            non_existing_url=non_existing_url,
            non_existing_response=non_existing_response,
            image_weight_total_kb=image_weight_total_kb,
            heavy_images=heavy_images,
        )

        results = self.rule_engine.evaluate(context)
        report = AuditReport(
            input_url=input_url,
            normalized_url=normalized,
            final_url=final_url,
            generated_at=AuditReport.now(),
            summary=self._build_summary(results),
            results=results,
        )
        return report.to_dict()

    def _check_broken_resources(self, urls: list[str]) -> tuple[int, list[str]]:
        broken: list[str] = []
        for url in urls[: self.sample_size]:
            response = self.http_client.request("HEAD", url, allow_redirects=True)
            if response is None or response.status_code >= 400:
                response = self.http_client.request("GET", url, allow_redirects=True)
            if response is None or response.status_code >= 400:
                broken.append(url)
        return len(broken), broken

    def _check_image_weight(self, image_urls: list[str]) -> tuple[float, list[str]]:
        total_kb = 0.0
        heavy: list[str] = []
        for image_url in image_urls[: self.sample_size]:
            head_response = self.http_client.request("HEAD", image_url, allow_redirects=True)
            content_len = head_response.headers.get("Content-Length") if head_response is not None else None
            if content_len is None:
                get_response = self.http_client.request("GET", image_url, allow_redirects=True)
                if get_response is not None:
                    content_len = get_response.headers.get("Content-Length")
            try:
                size_bytes = int(content_len) if content_len else 0
            except ValueError:
                size_bytes = 0
            size_kb = size_bytes / 1024
            total_kb += size_kb
            if size_kb > 400:
                heavy.append(image_url)
        return total_kb, heavy

    @staticmethod
    def _collect_internal_links(soup: BeautifulSoup, base_origin: str) -> list[str]:
        base_host = urlparse(base_origin).netloc
        links: list[str] = []
        seen = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            absolute = urljoin(base_origin, href)
            parsed = urlparse(absolute)
            if parsed.scheme not in {"http", "https"}:
                continue
            if parsed.netloc != base_host:
                continue
            cleaned = urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))
            if cleaned not in seen:
                seen.add(cleaned)
                links.append(cleaned)
        return links

    @staticmethod
    def _collect_images(soup: BeautifulSoup, base_origin: str) -> list[str]:
        images: list[str] = []
        seen = set()
        for img_tag in soup.find_all("img", src=True):
            src = img_tag.get("src", "").strip()
            if not src or src.startswith("data:"):
                continue
            absolute = urljoin(base_origin, src)
            parsed = urlparse(absolute)
            if parsed.scheme not in {"http", "https"}:
                continue
            clean = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
            if clean not in seen:
                seen.add(clean)
                images.append(clean)
        return images

    @staticmethod
    def _build_non_existing_url(base_origin: str) -> str:
        return urljoin(base_origin, "/no-existe-seo-check-404-test")

    @staticmethod
    def _build_summary(report: list[RuleResult]) -> dict[str, int]:
        summary: dict[str, int] = {"PASS": 0, "FAIL": 0, "WARN": 0, "MANUAL": 0}
        for result in report:
            summary[result.status] = summary.get(result.status, 0) + 1
        return summary
