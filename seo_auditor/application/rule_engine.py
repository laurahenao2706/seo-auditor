from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse

from seo_auditor.domain.models import AuditContext, RuleResult
from seo_auditor.domain.protocols import AuditRuleEngine, HttpClient

ALLOWED_REL_VALUES = {
    "nofollow",
    "follow",
    "canonical",
    "alternate",
    "noopener",
    "noreferrer",
    "ugc",
    "sponsored",
}


class ChecklistRuleEngine(AuditRuleEngine):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def evaluate(self, context: AuditContext) -> list[RuleResult]:
        rules = [
            self._rule_1,
            self._rule_2,
            self._rule_3,
            self._rule_4,
            self._rule_5,
            self._rule_6,
            self._rule_7,
            self._rule_8,
            self._rule_9,
            self._rule_10,
            self._rule_11,
            self._rule_12,
            self._rule_13,
            self._rule_14,
            self._rule_15,
            self._rule_16,
            self._rule_17,
            self._rule_18,
            self._rule_19,
            self._rule_20,
            self._rule_21,
            self._rule_22,
            self._rule_23,
            self._rule_24,
            self._rule_25,
            self._rule_26,
            self._rule_27,
            self._rule_28,
            self._rule_29,
            self._rule_30,
        ]
        return [rule(context) for rule in rules]

    def _rule_1(self, context: AuditContext) -> RuleResult:
        has_robots = bool(context.robots_response and context.robots_response.status_code == 200)
        return RuleResult(
            1,
            "Archivo robots.txt",
            "PASS" if has_robots else "FAIL",
            f"robots.txt en {context.robots_url} -> {context.robots_response.status_code if context.robots_response else 'sin respuesta'}",
            "Crear y mantener robots.txt con reglas de rastreo.",
        )

    def _rule_2(self, context: AuditContext) -> RuleResult:
        redirect_codes = [r.status_code for r in context.response.history]
        redirect_ok = len(redirect_codes) <= 5
        return RuleResult(
            2,
            "Redirecciones",
            "PASS" if redirect_ok else "WARN",
            f"Cadena de redireccion: {redirect_codes or 'sin redireccion'}; URL final: {context.final_url}",
            "Evitar cadenas largas y usar 301 para definitivas y 302 para temporales.",
        )

    def _rule_3(self, context: AuditContext) -> RuleResult:
        h1_count = len(context.soup.find_all("h1"))
        h2_h4_count = len(context.soup.find_all(["h2", "h3", "h4"]))
        heading_ok = h1_count >= 1 and h2_h4_count >= 1
        return RuleResult(
            3,
            "Headings de las paginas",
            "PASS" if heading_ok else "FAIL",
            f"H1: {h1_count}, H2-H4: {h2_h4_count}",
            "Asegurar 1 H1 principal y subtitulos jerarquicos H2/H3/H4.",
        )

    def _rule_4(self, context: AuditContext) -> RuleResult:
        title_text = (context.soup.title.string or "").strip() if context.soup.title else ""
        title_len = len(title_text)
        title_ok = 30 <= title_len <= 60
        return RuleResult(
            4,
            "Metatitulo",
            "PASS" if title_ok else "WARN",
            f"Longitud title: {title_len}. Valor: {title_text[:100] or 'vacio'}",
            "Recomendado entre 30 y 60 caracteres, con palabras clave.",
        )

    def _rule_5(self, context: AuditContext) -> RuleResult:
        meta_desc_tag = context.soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        meta_desc = (meta_desc_tag.get("content") or "").strip() if meta_desc_tag else ""
        meta_desc_len = len(meta_desc)
        desc_ok = 70 <= meta_desc_len <= 160
        return RuleResult(
            5,
            "Metadescripcion",
            "PASS" if desc_ok else "WARN",
            f"Longitud meta description: {meta_desc_len}. Valor: {meta_desc[:120] or 'vacio'}",
            "Recomendado entre 70 y 160 caracteres con copy orientado a busqueda.",
        )

    def _rule_6(self, context: AuditContext) -> RuleResult:
        canonical_tag = context.soup.find("link", attrs={"rel": re.compile("canonical", re.I)})
        canonical_href = canonical_tag.get("href", "").strip() if canonical_tag else ""
        return RuleResult(
            6,
            "Canonical en la URL",
            "PASS" if canonical_href else "FAIL",
            f"Canonical: {canonical_href or 'no encontrado'}",
            "Incluir link rel=canonical absoluto en cada pagina indexable.",
        )

    def _rule_7(self, context: AuditContext) -> RuleResult:
        html_lang = (context.soup.html.get("lang") if context.soup.html else "") or ""
        hreflang_tags = context.soup.find_all("link", attrs={"hreflang": True})
        has_lang = bool(html_lang.strip())
        has_hreflang = len(hreflang_tags) > 0
        return RuleResult(
            7,
            "Hreflang y Geotargeting",
            "PASS" if (has_lang and (has_hreflang or "-" in html_lang)) else "WARN",
            f"html lang: {html_lang or 'vacio'}; hreflang tags: {len(hreflang_tags)}",
            "Definir idioma/pais en html lang y usar hreflang para versiones regionales.",
        )

    def _rule_8(self, context: AuditContext) -> RuleResult:
        ssr_ok = context.text_size >= 300
        return RuleResult(
            8,
            "Renderizacion desde el servidor",
            "PASS" if ssr_ok else "WARN",
            f"Texto visible en HTML inicial: {context.text_size} caracteres",
            "Verificar que el HTML entregado por servidor incluya contenido util para SEO.",
        )

    def _rule_9(self, context: AuditContext) -> RuleResult:
        broken_total = context.broken_link_count + context.broken_image_count
        status_9 = "PASS" if broken_total == 0 else "FAIL"
        details_9 = (
            f"Enlaces rotos: {context.broken_link_count}; Imagenes rotas: {context.broken_image_count}. "
            f"Ejemplos enlaces: {', '.join(context.broken_link_examples[:3]) or 'ninguno'}. "
            f"Ejemplos imagenes: {', '.join(context.broken_image_examples[:3]) or 'ninguno'}."
        )
        return RuleResult(
            9,
            "URLs e imagenes que llevan a 404",
            status_9,
            details_9,
            "Corregir rutas rotas o redirigir a contenido valido.",
        )

    def _rule_10(self, _: AuditContext) -> RuleResult:
        return RuleResult(
            10,
            "Errores de consola",
            "MANUAL",
            "No se puede validar sin ejecutar JavaScript en navegador (Playwright/Selenium).",
            "Revisar consola en navegador o integrar un auditor JS headless.",
            automated=False,
        )

    def _rule_11(self, context: AuditContext) -> RuleResult:
        is_404 = bool(context.non_existing_response and context.non_existing_response.status_code == 404)
        return RuleResult(
            11,
            "Pagina 404",
            "PASS" if is_404 else "WARN",
            f"URL de prueba: {context.non_existing_url} -> {context.non_existing_response.status_code if context.non_existing_response else 'sin respuesta'}",
            "Configurar respuesta HTTP 404 real y pagina de ayuda de navegacion.",
        )

    def _rule_12(self, context: AuditContext) -> RuleResult:
        has_breadcrumb = bool(
            context.soup.select("nav[aria-label*='breadcrumb' i]")
            or context.soup.select("[itemtype*='BreadcrumbList']")
            or context.soup.select("ol.breadcrumb, ul.breadcrumb")
        )
        return RuleResult(
            12,
            "Miga de pan",
            "PASS" if has_breadcrumb else "WARN",
            "Breadcrumb detectado" if has_breadcrumb else "No se detecto breadcrumb estructurado",
            "Agregar breadcrumb HTML y/o Schema.org BreadcrumbList.",
        )

    def _rule_13(self, context: AuditContext) -> RuleResult:
        og_tags = context.soup.find_all("meta", attrs={"property": re.compile(r"^og:", re.I)})
        return RuleResult(
            13,
            "Marcado Opengraph",
            "PASS" if len(og_tags) >= 3 else "WARN",
            f"Etiquetas OG detectadas: {len(og_tags)}",
            "Agregar al menos og:title, og:description y og:image.",
        )

    def _rule_14(self, context: AuditContext) -> RuleResult:
        tw_tags = context.soup.find_all("meta", attrs={"name": re.compile(r"^twitter:", re.I)})
        return RuleResult(
            14,
            "Marcado Twitter Cards",
            "PASS" if len(tw_tags) >= 2 else "WARN",
            f"Etiquetas Twitter detectadas: {len(tw_tags)}",
            "Agregar twitter:card, twitter:title, twitter:description, twitter:image.",
        )

    def _rule_15(self, context: AuditContext) -> RuleResult:
        viewport_tag = context.soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
        has_viewport = bool(viewport_tag and viewport_tag.get("content"))
        return RuleResult(
            15,
            "Responsive",
            "PASS" if has_viewport else "WARN",
            f"Meta viewport: {(viewport_tag.get('content') if viewport_tag else 'no encontrado')}",
            "Incluir meta viewport y validar diseno responsive en multiples breakpoints.",
        )

    def _rule_16(self, context: AuditContext) -> RuleResult:
        speed_status = "PASS" if context.ttfb <= 0.8 else "WARN"
        return RuleResult(
            16,
            "Velocidad de carga",
            speed_status,
            f"TTFB: {context.ttfb:.2f}s; tiempo total descarga HTML: {context.total_fetch:.2f}s",
            "Optimizar TTFB, cache, compresion y peso de recursos criticos.",
        )

    def _rule_17(self, context: AuditContext) -> RuleResult:
        nav_count = len(context.soup.find_all("nav"))
        return RuleResult(
            17,
            "Menu con etiqueta nav",
            "PASS" if nav_count > 0 else "WARN",
            f"Etiquetas nav detectadas: {nav_count}",
            "Encapsular navegacion principal en etiqueta nav.",
        )

    def _rule_18(self, context: AuditContext) -> RuleResult:
        menu_ul_ok = False
        for nav in context.soup.find_all("nav"):
            if nav.find("ul"):
                menu_ul_ok = True
                break
        return RuleResult(
            18,
            "Elementos de menu",
            "PASS" if menu_ul_ok else "WARN",
            "Se detecto ul dentro de nav" if menu_ul_ok else "No se detecto lista ul dentro de nav",
            "Estructurar menu con listas no ordenadas y enlaces claros.",
        )

    def _rule_19(self, context: AuditContext) -> RuleResult:
        semantic_name_ok, invalid_names = self._check_image_names(context.image_urls)
        return RuleResult(
            19,
            "Nombre de archivos cargados",
            "PASS" if semantic_name_ok else "WARN",
            f"Imagenes con nombre no recomendado: {len(invalid_names)}. Ejemplos: {', '.join(invalid_names[:4]) or 'ninguno'}",
            "Usar nombres semanticos en minuscula, separados por guion medio y sin caracteres especiales.",
        )

    def _rule_20(self, context: AuditContext) -> RuleResult:
        status_20 = "PASS" if not context.heavy_images else "WARN"
        return RuleResult(
            20,
            "Peso de las imagenes",
            status_20,
            f"Peso total imagenes muestreadas: {context.image_weight_total_kb:.1f} KB; >400KB: {len(context.heavy_images)}",
            "Comprimir imagenes y priorizar formatos modernos (WebP/AVIF) cuando aplique.",
        )

    def _rule_21(self, context: AuditContext) -> RuleResult:
        images = context.soup.find_all("img")
        imgs_without_alt = [img.get("src", "") for img in images if not (img.get("alt") or "").strip()]
        return RuleResult(
            21,
            'Texto alternativo "alt"',
            "PASS" if len(imgs_without_alt) == 0 else "WARN",
            f"Imagenes sin alt: {len(imgs_without_alt)}",
            "Agregar atributo alt descriptivo para accesibilidad y SEO de imagenes.",
        )

    def _rule_22(self, context: AuditContext) -> RuleResult:
        http_url = self._force_http(context.final_url)
        http_resp = self.http_client.request("GET", http_url, allow_redirects=True)
        redirects_to_https = bool(http_resp and http_resp.url.startswith("https://"))
        return RuleResult(
            22,
            "Redirecciones http a https",
            "PASS" if redirects_to_https else "FAIL",
            f"Prueba {http_url} -> {(http_resp.url if http_resp else 'sin respuesta')}",
            "Forzar redireccion 301 global de http a https.",
        )

    def _rule_23(self, context: AuditContext) -> RuleResult:
        parsed_final = urlparse(context.final_url)
        host = parsed_final.netloc
        alt_host = self._toggle_www(host)
        alt_url = urlunparse((parsed_final.scheme, alt_host, parsed_final.path or "/", "", "", "")) if alt_host else ""
        alt_resp = self.http_client.request("GET", alt_url, allow_redirects=True) if alt_url else None
        canonical_host_ok = bool(alt_resp and urlparse(alt_resp.url).netloc == host)
        return RuleResult(
            23,
            "URL con www o sin www",
            "PASS" if canonical_host_ok else "WARN",
            f"Host canonical: {host}. Prueba alterna: {alt_url or 'n/a'} -> {(alt_resp.url if alt_resp else 'sin respuesta')}",
            "Definir un unico host canonico y redirigir el alterno.",
        )

    def _rule_24(self, context: AuditContext) -> RuleResult:
        search_forms = context.soup.find_all("form")
        has_search = any((f.get("role") == "search") or (f.find(attrs={"type": "search"}) is not None) for f in search_forms)
        return RuleResult(
            24,
            "Sistema de busquedas internas",
            "WARN" if has_search else "MANUAL",
            "Se detecto buscador interno" if has_search else "No se detecto de forma automatica",
            "Validar que resultados de busqueda usen canonical/noindex cuando generen parametros.",
            automated=has_search,
        )

    def _rule_25(self, context: AuditContext) -> RuleResult:
        popup_keywords = ["popup", "modal", "interstitial", "subscribe", "newsletter"]
        html_lower = (context.response.text or "").lower()
        popup_hits = sum(1 for token in popup_keywords if token in html_lower)
        return RuleResult(
            25,
            "Evitar carga de pop-up's",
            "WARN" if popup_hits > 0 else "PASS",
            f"Coincidencias de patrones popup/modal: {popup_hits}",
            "Limitar interstitials intrusivos y cargar elementos no criticos de forma diferida.",
        )

    def _rule_26(self, context: AuditContext) -> RuleResult:
        sitemap_ok = bool(context.sitemap_response and context.sitemap_response.status_code == 200)
        return RuleResult(
            26,
            "Mapa del sitio",
            "PASS" if sitemap_ok else "FAIL",
            f"sitemap.xml en {context.sitemap_url} -> {context.sitemap_response.status_code if context.sitemap_response else 'sin respuesta'}",
            "Generar sitemap.xml automatico y mantenerlo actualizado.",
        )

    def _rule_27(self, context: AuditContext) -> RuleResult:
        manifest_link = context.soup.find("link", attrs={"rel": re.compile("manifest", re.I)})
        html_lower = (context.response.text or "").lower()
        has_sw_hint = "serviceworker" in html_lower or "service-worker" in html_lower
        pwa_ok = bool(manifest_link or has_sw_hint)
        return RuleResult(
            27,
            "PWA",
            "PASS" if pwa_ok else "WARN",
            f"Manifest: {manifest_link.get('href') if manifest_link else 'no'}; SW hint: {has_sw_hint}",
            "Si aplica PWA, incluir manifest.json y service worker funcional.",
        )

    def _rule_28(self, context: AuditContext) -> RuleResult:
        parsed_final = urlparse(context.final_url)
        path = parsed_final.path or "/"
        bad_path_chars = bool(re.search(r"[A-Z_+*'\s]", path))
        url_arch_ok = not bad_path_chars
        return RuleResult(
            28,
            "Arquitectura URL",
            "PASS" if url_arch_ok else "WARN",
            f"Path evaluado: {path}",
            "Usar URLs limpias, descriptivas, en minuscula y separadas por guion medio.",
        )

    def _rule_29(self, context: AuditContext) -> RuleResult:
        invalid_rel_links = 0
        for a_tag in context.soup.find_all("a"):
            rel_values = a_tag.get("rel") or []
            for rel_value in rel_values:
                if rel_value.lower() not in ALLOWED_REL_VALUES:
                    invalid_rel_links += 1
                    break
        return RuleResult(
            29,
            "Atributos para enlaces",
            "PASS" if invalid_rel_links == 0 else "WARN",
            f"Enlaces con rel no recomendado: {invalid_rel_links}",
            "Usar atributos rel de forma consistente segun objetivo SEO.",
        )

    def _rule_30(self, context: AuditContext) -> RuleResult:
        links_with_params = [url for url in context.internal_links if urlparse(url).query]
        has_noindex_meta = bool(
            context.soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I), "content": re.compile(r"noindex", re.I)})
        )
        return RuleResult(
            30,
            "Desindexacion de parametros",
            "WARN" if links_with_params and not has_noindex_meta else "PASS",
            f"Links internos con parametros: {len(links_with_params)}; meta robots noindex: {has_noindex_meta}",
            "Evitar indexar URLs con parametros usando canonical, noindex o reglas de rastreo.",
        )

    @staticmethod
    def _check_image_names(image_urls: list[str]) -> tuple[bool, list[str]]:
        invalid: list[str] = []
        good_pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.[a-z0-9]{2,5}$")
        default_pattern = re.compile(r"^(img|dsc|image)[-_]?\d+", re.I)
        for image_url in image_urls:
            file_name = image_url.rsplit("/", 1)[-1]
            if not file_name:
                continue
            if default_pattern.search(file_name) or not good_pattern.match(file_name):
                invalid.append(file_name)
        return len(invalid) == 0, invalid

    @staticmethod
    def _force_http(url: str) -> str:
        parsed = urlparse(url)
        return urlunparse(("http", parsed.netloc, parsed.path, "", parsed.query, ""))

    @staticmethod
    def _toggle_www(host: str) -> str:
        if not host:
            return ""
        if host.startswith("www."):
            return host[4:]
        return "www." + host
