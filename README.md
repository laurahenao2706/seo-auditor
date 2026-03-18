# SEO Checklist Auditor

[![CI/CD Pipeline](https://github.com/TU_USUARIO/seo-auditor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/TU_USUARIO/seo-auditor/actions/workflows/ci-cd.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Framework en Python para auditar SEO tecnico de una URL con enfoque en POO, SOLID, separacion por capas y pruebas unitarias.

## Principios aplicados

- POO: clases con responsabilidades acotadas por capa.
- SOLID:
  - SRP: normalizacion, acceso HTTP, motor de reglas, serializacion y orquestacion separados.
  - OCP: el motor permite extender reglas sin cambiar el contrato del servicio.
  - LSP: cualquier implementacion de interfaces puede reemplazar la concreta.
  - ISP: interfaces pequenas para HTTP, normalizacion y motor de reglas.
  - DIP: el servicio depende de abstracciones, no de implementaciones concretas.
- Patron principal: Strategy en el motor de reglas (ChecklistRuleEngine) inyectado al servicio.
- Manejo de excepciones con errores de dominio (InvalidUrlError, FetchError).

## Estructura

```text
SEO/
|-- app.py
|-- seo_checker.py
|-- requirements.txt
|-- seo_auditor/
|   |-- application/
|   |   |-- normalizer.py
|   |   |-- rule_engine.py
|   |   |-- serializers.py
|   |   `-- service.py
|   |-- domain/
|   |   |-- exceptions.py
|   |   |-- models.py
|   |   `-- protocols.py
|   `-- infrastructure/
|       `-- http_client.py
`-- tests/
    |-- test_normalizer.py
    |-- test_serializers.py
    `-- test_service.py
```

## Requisitos

- Python 3.10+
- Dependencias de requirements.txt

## Instalacion

```bash
python -m pip install -r requirements.txt
```

## Ejecutar app web

```bash
streamlit run app.py
```

## Ejecutar CLI

```bash
python seo_checker.py https://www.ejemplo.com --out-json reporte.json --out-csv reporte.csv
```

## Ejecutar pruebas unitarias

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Cobertura funcional

- Se mantienen las 30 reglas del checklist SEO con estados PASS, FAIL, WARN y MANUAL.
- Soporta exportacion de resultados a JSON y CSV.
- Mantiene compatibilidad de uso por CLI y Streamlit.

## Escalabilidad sugerida

- Agregar nuevas estrategias de reglas para sectores o stacks especificos.
- Incorporar adaptadores de almacenamiento para historial en base de datos.
- Añadir un motor JS headless (Playwright) para automatizar reglas MANUAL.

---

## 🚀 CI/CD y Deployment

Este proyecto incluye pipelines completos de CI/CD configurados para:

- ✅ **Tests automáticos** en múltiples versiones de Python (3.10, 3.11, 3.12)
- ✅ **Linting y formateo** con Black, Flake8, isort, MyPy
- ✅ **Security scanning** con Safety y Bandit
- ✅ **Coverage reporting** integrado con Codecov
- ✅ **Deployment automático** a Streamlit Cloud
- ✅ **Notificaciones** de estado del pipeline

### Herramientas Disponibles

#### GitHub Actions (Recomendado)
Pipeline configurado en `.github/workflows/ci-cd.yml`

```bash
# Ver documentación completa
cat ANALISIS_CICD.md
cat DEPLOYMENT_GUIDE.md
```

#### GitLab CI/CD (Alternativa)
Pipeline configurado en `.gitlab-ci.yml`

### Quick Start - Desarrollo

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd seo-auditor

# 2. Ejecutar setup automático
python setup_dev.py

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Ejecutar tests
python -m unittest discover -s tests -v

# 5. Verificar linting
python -m black --check .
python -m flake8 seo_auditor/
```

### Deploy a Producción

**Streamlit Cloud (Recomendado)**:
1. Push código a GitHub/GitLab
2. Conectar en https://share.streamlit.io/
3. Deployment automático en cada push a `main`

Ver [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) para opciones avanzadas (Heroku, Docker, Cloud Run).

---

## 📚 Documentación Adicional

- 📊 [**ANALISIS_CICD.md**](ANALISIS_CICD.md) - Análisis comparativo de herramientas CI/CD
- 🚀 [**DEPLOYMENT_GUIDE.md**](DEPLOYMENT_GUIDE.md) - Guía completa de deployment
- ✅ [**CICD_BEST_PRACTICES.md**](CICD_BEST_PRACTICES.md) - Mejores prácticas y optimizaciones
- 📖 [**REPORTE_TECNICO_DETALLADO.md**](REPORTE_TECNICO_DETALLADO.md) - Documentación técnica completa

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```text
SEO/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
├── .gitlab-ci.yml             # GitLab CI/CD pipeline
├── seo_auditor/               # Código principal
│   ├── application/           # Capa de aplicación
│   ├── domain/                # Lógica de dominio
│   └── infrastructure/        # Adaptadores externos
├── tests/                     # Tests unitarios
├── app.py                     # Aplicación Streamlit
├── seo_checker.py             # CLI
├── requirements.txt           # Dependencias producción
├── requirements-dev.txt       # Dependencias desarrollo
├── pyproject.toml             # Configuración herramientas
├── setup_dev.py               # Script de setup
└── .gitignore                 # Archivos ignorados
```

### Comandos de Desarrollo

```bash
# Formatear código automáticamente
python -m black .
python -m isort .

# Análisis de código
python -m flake8 seo_auditor/
python -m mypy seo_auditor/ --ignore-missing-imports

# Tests con coverage
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m coverage html  # Genera reporte HTML en htmlcov/

# Security checks
python -m safety check
python -m bandit -r seo_auditor/
```

### Pre-commit Hooks

```bash
# Instalar pre-commit
pip install pre-commit

# Activar hooks
pre-commit install

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

**El pipeline CI/CD se ejecutará automáticamente** en tu PR para validar:
- Tests pasan ✅
- Linting OK ✅
- Security checks OK ✅
- Coverage >= 80% ✅

---

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles

---

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial*

---

## 🙏 Agradecimientos

- Arquitectura hexagonal inspirada en Clean Architecture
- Configuración CI/CD basada en mejores prácticas de la comunidad Python
- Testing patterns de pytest y unittest best practices
