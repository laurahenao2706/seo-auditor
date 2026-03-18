import unittest

from seo_auditor.application.normalizer import BasicUrlNormalizer


class BasicUrlNormalizerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.normalizer = BasicUrlNormalizer()

    def test_adds_https_when_missing(self) -> None:
        self.assertEqual(self.normalizer.normalize("example.com"), "https://example.com")

    def test_returns_empty_when_invalid(self) -> None:
        self.assertEqual(self.normalizer.normalize(""), "")


if __name__ == "__main__":
    unittest.main()
