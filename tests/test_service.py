import unittest
from dataclasses import dataclass

from seo_auditor.application.normalizer import BasicUrlNormalizer
from seo_auditor.application.rule_engine import ChecklistRuleEngine
from seo_auditor.application.service import SeoAuditService


class FakeElapsed:
    def __init__(self, seconds: float) -> None:
        self._seconds = seconds

    def total_seconds(self) -> float:
        return self._seconds


@dataclass
class FakeResponse:
    url: str
    status_code: int
    text: str = ""
    history: list | None = None
    headers: dict | None = None
    elapsed: FakeElapsed | None = None

    def __post_init__(self) -> None:
        if self.history is None:
            self.history = []
        if self.headers is None:
            self.headers = {}
        if self.elapsed is None:
            self.elapsed = FakeElapsed(0.2)


class FakeHttpClient:
    def __init__(self) -> None:
        html = """
        <html lang='es-CO'>
          <head>
            <title>Titulo de ejemplo optimizado para motores de busqueda</title>
            <meta name='description' content='Descripcion de prueba para validar el auditor SEO automatico con longitud correcta en metadatos.'>
            <link rel='canonical' href='https://example.com/'>
            <link rel='alternate' hreflang='es-CO' href='https://example.com/'>
            <meta property='og:title' content='og title'>
            <meta property='og:description' content='og description'>
            <meta property='og:image' content='https://example.com/image.jpg'>
            <meta name='twitter:card' content='summary_large_image'>
            <meta name='twitter:title' content='title'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <link rel='manifest' href='/manifest.json'>
          </head>
          <body>
            <nav aria-label='breadcrumb'><ul><li>Inicio</li></ul></nav>
            <h1>Heading principal</h1>
            <h2>Subtitulo</h2>
            <a href='/contacto'>Contacto</a>
            <img src='https://example.com/banner-home.jpg' alt='Banner principal'>
          </body>
        </html>
        """
        self.responses = {
            ("GET", "https://example.com"): FakeResponse(url="https://example.com/", status_code=200, text=html),
            ("GET", "https://example.com/"): FakeResponse(url="https://example.com/", status_code=200, text=html),
            ("GET", "https://example.com/robots.txt"): FakeResponse(url="https://example.com/robots.txt", status_code=200, text="User-agent: *"),
            ("GET", "https://example.com/sitemap.xml"): FakeResponse(url="https://example.com/sitemap.xml", status_code=200, text="<urlset></urlset>"),
            ("GET", "https://example.com/no-existe-seo-check-404-test"): FakeResponse(
                url="https://example.com/no-existe-seo-check-404-test", status_code=404, text="not found"
            ),
            ("HEAD", "https://example.com/contacto"): FakeResponse(url="https://example.com/contacto", status_code=200),
            ("HEAD", "https://example.com/banner-home.jpg"): FakeResponse(
                url="https://example.com/banner-home.jpg", status_code=200, headers={"Content-Length": "102400"}
            ),
            ("GET", "http://example.com/"): FakeResponse(url="https://example.com/", status_code=301),
            ("GET", "https://www.example.com/"): FakeResponse(url="https://example.com/", status_code=301),
        }

    def request(self, method: str, url: str, allow_redirects: bool = True):
        return self.responses.get((method, url))


class SeoAuditServiceTestCase(unittest.TestCase):
    def test_analyze_builds_30_rules(self) -> None:
        fake_http = FakeHttpClient()
        service = SeoAuditService(
            http_client=fake_http,
            normalizer=BasicUrlNormalizer(),
            rule_engine=ChecklistRuleEngine(fake_http),
        )

        report = service.analyze("example.com")

        self.assertEqual(report["normalized_url"], "https://example.com")
        self.assertEqual(len(report["results"]), 30)
        self.assertEqual(sum(report["summary"].values()), 30)


if __name__ == "__main__":
    unittest.main()
