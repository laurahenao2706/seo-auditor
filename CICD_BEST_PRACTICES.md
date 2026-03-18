# 📋 Mejores Prácticas CI/CD - SEO Auditor

## 🎯 Objetivo
Documento de referencia para mantener calidad y eficiencia en el pipeline CI/CD.

---

## 📐 Principios Fundamentales

### 1. Pipeline Rápido
- ⏱️ **Objetivo**: Pipeline completo < 10 minutos
- 🚀 **Estrategias**:
  - Cachear dependencias (pip cache)
  - Paralelizar jobs independientes
  - Ejecutar tests más críticos primero (fail-fast)

### 2. Feedback Temprano
- 🔍 Linting antes que tests (más rápido, detecta errores obvios)
- ✅ Tests unitarios antes que integración
- 🔒 Security scan en paralelo con tests

### 3. Reproducibilidad
- 📌 Pin de versiones en requirements.txt
- 🐳 Usar mismas imágenes Docker en CI y local
- 🔄 Test matrix con versiones Python múltiples

---

## 🔧 Configuración de Workflows

### Triggers Recomendados

```yaml
# GitHub Actions
on:
  push:
    branches: [main, develop]        # CI en branches principales
  pull_request:
    branches: [main]                 # CI en PRs a main
  schedule:
    - cron: '0 2 * * 1'              # Tests semanales (Lunes 2AM)
  workflow_dispatch:                 # Ejecución manual
```

### Jobs Paralelos vs Secuenciales

**✅ Ejecutar en Paralelo:**
- Linting (black, flake8, isort, mypy)
- Security scans
- Tests en diferentes versiones Python
- Build de documentación

**❌ Ejecutar Secuencialmente:**
- Lint → Test → Deploy
- Tests → Build → Security Final
- Test → Package → Publish

---

## 🧪 Testing Best Practices

### Estructura de Tests

```
tests/
├── unit/              # Tests rápidos, sin I/O
│   ├── test_models.py
│   └── test_normalizer.py
├── integration/       # Tests con HTTP, DB
│   └── test_service.py
├── e2e/              # Tests completos
│   └── test_streamlit.py
└── conftest.py       # Fixtures compartidas
```

### Markers de Pytest

```python
# tests/conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "unit: unit tests")

# Uso en tests
@pytest.mark.unit
def test_normalizer():
    ...

@pytest.mark.integration
@pytest.mark.slow
def test_full_service():
    ...
```

### Ejecución Selectiva en CI

```yaml
# Ejecutar solo unit tests en cada commit
- name: Quick Tests
  run: pytest -m "unit" -v

# Full test suite en PRs
- name: Full Test Suite
  if: github.event_name == 'pull_request'
  run: pytest -v

# Incluir slow tests solo nocturnos
- name: Nightly Tests
  if: github.event_name == 'schedule'
  run: pytest -v --run-slow
```

---

## 🎨 Linting y Formateo

### Herramientas Recomendadas

| Herramienta | Propósito | Orden Ejecución |
|-------------|-----------|-----------------|
| **Black** | Formateo automático | 1 (más rápido) |
| **isort** | Organizar imports | 2 |
| **Flake8** | Linting PEP8 | 3 |
| **MyPy** | Type checking | 4 (más lento) |
| **Bandit** | Security linting | 5 |

### Configuración Progresiva

**Nivel 1: Básico (Inicio del proyecto)**
```toml
[tool.black]
line-length = 100
target-version = ['py310']

[flake8]
max-line-length = 100
ignore = E203, W503  # Compatible con Black
```

**Nivel 2: Intermedio (Proyecto maduro)**
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual typing
```

**Nivel 3: Estricto (Producción crítica)**
```toml
[tool.mypy]
strict = true
disallow_untyped_defs = true
disallow_any_generics = true
warn_redundant_casts = true
```

### Auto-fix en CI (Opcional)

```yaml
- name: Auto-format code
  run: |
    black .
    isort .
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git add -A
    git diff --quiet && git diff --staged --quiet || \
      (git commit -m "style: auto-format code [skip ci]" && git push)
```

---

## 🔒 Security Best Practices

### 1. Escaneo de Dependencias

```yaml
- name: Check vulnerabilities
  run: |
    pip install safety
    safety check --full-report
  continue-on-error: true  # Warning, no bloqueante
```

### 2. Secrets Management

**❌ NUNCA:**
- Hardcodear secrets en código
- Commitear .env files
- Loggear variables sensibles

**✅ SIEMPRE:**
- Usar GitHub Secrets / GitLab Variables
- Enmascarar en logs (mask: true)
- Rotar secrets periódicamente

```yaml
# GitHub Actions
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}  # ✅ Correcto
  run: |
    echo "Deploying..."
    # API_KEY está disponible pero oculta en logs
```

### 3. Dependabot/Renovate

**GitHub Dependabot:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "tu-usuario"
```

---

## 📊 Coverage y Reportes

### Metas de Coverage

| Tipo Proyecto | Target Coverage | Min Aceptable |
|---------------|-----------------|---------------|
| Prototipo | 60% | 40% |
| Producción | 80% | 70% |
| Crítico | 90% | 85% |

### Configuración Estricta

```yaml
- name: Coverage Check
  run: |
    coverage run -m pytest
    coverage report --fail-under=80  # Falla si < 80%
```

### Excluir código de coverage

```python
def debug_function():  # pragma: no cover
    """Solo para debugging, no testeado"""
    print("Debug info")

if __name__ == "__main__":  # pragma: no cover
    main()
```

---

## 🚀 Deployment Strategies

### 1. Gitflow + Environments

```
main (production)
  ↑
develop (staging) ← feature/* branches
  ↑
release/*
```

**CI/CD Mapping:**
- `push to main` → Deploy Production
- `push to develop` → Deploy Staging (auto)
- `push to feature/*` → Tests only

### 2. Trunk-Based Development

```
main (production)
  ↑
short-lived-feature-branches (< 2 días)
```

**CI/CD Mapping:**
- `push to main` → Tests + Deploy Production
- `pull_request` → Tests + Preview deployment
- Feature flags para controlar releases

### 3. Semantic Versioning + Tags

```bash
# Crear release
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3

# Trigger deployment automático
```

**Version Bumping:**
- `v1.0.0` → `v1.0.1`: Bug fix
- `v1.0.0` → `v1.1.0`: New feature (compatible)
- `v1.0.0` → `v2.0.0`: Breaking change

---

## 📈 Optimización de Pipeline

### 1. Cachear Dependencias

**GitHub Actions:**
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
    cache-dependency-path: |
      requirements.txt
      requirements-dev.txt
```

**GitLab CI:**
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - venv/
```

### 2. Matrix Strategy Inteligente

```yaml
strategy:
  fail-fast: false  # No cancelar otros jobs si uno falla
  matrix:
    os: [ubuntu-latest]  # Solo Linux en commits
    python-version: ['3.11']  # Una versión en commits
    
    # Full matrix solo en PRs
    include:
      - os: windows-latest
        python-version: '3.10'
        if: github.event_name == 'pull_request'
      - os: macos-latest
        python-version: '3.12'
        if: github.event_name == 'pull_request'
```

### 3. Conditional Steps

```yaml
- name: Heavy Integration Tests
  if: |
    github.event_name == 'pull_request' ||
    github.ref == 'refs/heads/main'
  run: pytest tests/integration/ -v
```

---

## 🔄 Rollback Strategies

### 1. Git Revert (Recomendado)

```bash
# Revertir commit problemático
git revert <commit-hash>
git push origin main
# CI/CD automáticamente deploya versión anterior
```

### 2. Re-deploy Tag Anterior

```bash
# Trigger deployment de versión anterior
git checkout v1.2.2
git tag -f v1.2.3  # Forzar tag
git push -f origin v1.2.3
```

### 3. Manual Rollback (Último recurso)

```yaml
- name: Rollback
  if: github.event.inputs.rollback == 'true'
  run: |
    # Revertir a versión específica
    ./scripts/rollback.sh ${{ github.event.inputs.version }}
```

---

## 📢 Notificaciones

### Slack Integration

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: |
      Deployment ${{ job.status }}
      Commit: ${{ github.event.head_commit.message }}
      Author: ${{ github.actor }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

### Discord Integration

```yaml
- name: Notify Discord
  uses: sarisia/actions-status-discord@v1
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}
    title: "CI/CD Pipeline"
    description: "${{ github.event.head_commit.message }}"
  if: always()
```

### Email (GitHub Native)

1. Settings → Notifications
2. ✅ Email notifications for failed workflows

---

## 📝 Checklist de Revisión

### Antes de Merge

```markdown
- [ ] Todos los tests pasan
- [ ] Coverage >= 80%
- [ ] Linting sin errores
- [ ] No hay security warnings críticos
- [ ] Changelog actualizado
- [ ] Documentación actualizada
- [ ] PR revisado por al menos 1 persona
```

### Antes de Release

```markdown
- [ ] Tests pasan en todas las versiones (3.10, 3.11, 3.12)
- [ ] Tests pasan en todos los OS (Ubuntu, Windows, macOS)
- [ ] Staging deployment exitoso
- [ ] Performance benchmarks OK
- [ ] Security audit completo
- [ ] Release notes escritas
- [ ] Rollback plan documentado
```

---

## 🎓 Recursos Recomendados

### Libros
- "Continuous Delivery" - Jez Humble
- "The DevOps Handbook" - Gene Kim
- "Accelerate" - Nicole Forsgren

### Cursos
- [GitHub Actions Tutorial](https://docs.github.com/en/actions/learn-github-actions)
- [GitLab CI/CD Pipeline Tutorial](https://docs.gitlab.com/ee/ci/quick_start/)
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)

### Herramientas
- [act](https://github.com/nektos/act) - Test GitHub Actions localmente
- [gitlab-runner](https://docs.gitlab.com/runner/) - Test GitLab CI localmente
- [pre-commit](https://pre-commit.com/) - Git hooks

---

## 🔍 Debugging Pipeline

### GitHub Actions

```bash
# Ver logs detallados
gh run view <run-id> --log

# Re-ejecutar workflow
gh run rerun <run-id>

# Listar runs recientes
gh run list
```

### GitLab CI

```bash
# Ver logs de pipeline
gitlab-runner exec shell <job-name>

# Test pipeline localmente
gitlab-ci-validate .gitlab-ci.yml
```

---

## ✅ Métricas de Éxito

### KPIs del Pipeline

| Métrica | Target | Excelente |
|---------|--------|-----------|
| Duración total | < 15 min | < 5 min |
| Tasa de éxito | > 90% | > 95% |
| Time to feedback | < 5 min | < 2 min |
| Tests ejecutados | 100% | 100% |
| Coverage | > 80% | > 90% |

### Monitoreo

```yaml
- name: Pipeline Metrics
  run: |
    echo "Duration: ${{ github.run.duration }}"
    echo "Status: ${{ job.status }}"
    # Enviar a sistema de monitoring (Datadog, Grafana, etc.)
```

---

**Mantén este documento actualizado conforme el proyecto evoluciona** 🚀
