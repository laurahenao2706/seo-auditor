# 🚀 Guía de Deployment CI/CD - SEO Auditor

## 📋 Tabla de Contenidos
1. [Preparación Inicial](#preparación-inicial)
2. [Opción A: GitHub Actions](#opción-a-github-actions)
3. [Opción B: GitLab CI/CD](#opción-b-gitlab-cicd)
4. [Configuración de Deployment](#configuración-de-deployment)
5. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Preparación Inicial

### 1. Inicializar Git (si aún no está inicializado)

```powershell
# En la raíz del proyecto
git init
git add .
git commit -m "Initial commit: SEO Auditor project"
```

### 2. Instalar Dependencias de Desarrollo

```powershell
# Actualizar requirements.txt con herramientas de desarrollo
pip install black flake8 isort mypy coverage pytest pytest-cov safety bandit
pip freeze > requirements-dev.txt
```

### 3. Configurar Pre-commit Hooks (Opcional pero Recomendado)

```powershell
pip install pre-commit

# Crear .pre-commit-config.yaml
```

Contenido de `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

Activar:
```powershell
pre-commit install
```

---

## 🔵 Opción A: GitHub Actions

### Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Crea un nuevo repositorio (público o privado)
3. **NO** inicialices con README, .gitignore o licencia (ya los tienes)

### Paso 2: Conectar Repositorio Local

```powershell
git remote add origin https://github.com/TU_USUARIO/seo-auditor.git
git branch -M main
git push -u origin main
```

### Paso 3: Verificar Pipeline

1. Ve a tu repositorio en GitHub
2. Click en la pestaña **"Actions"**
3. Deberías ver el workflow **"CI/CD Pipeline"** ejecutándose

### Paso 4: Configurar Branch Protection (Recomendado)

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. ✅ Require status checks to pass before merging
4. ✅ Require branches to be up to date before merging
5. Selecciona los checks: `lint`, `test`, `security`

### Paso 5: Configurar Secrets (Para Notificaciones)

Si quieres notificaciones en Slack/Discord:

1. Settings → Secrets and variables → Actions → New repository secret
2. Nombre: `SLACK_WEBHOOK` o `DISCORD_WEBHOOK`
3. Valor: Tu webhook URL

Luego descomentar sección de notificaciones en `.github/workflows/ci-cd.yml`

---

## 🟠 Opción B: GitLab CI/CD

### Paso 1: Crear Repositorio en GitLab

1. Ve a https://gitlab.com/projects/new
2. Crea un nuevo proyecto
3. Elige "Create blank project"

### Paso 2: Conectar Repositorio Local

```powershell
git remote add origin https://gitlab.com/TU_USUARIO/seo-auditor.git
git branch -M main
git push -u origin main
```

### Paso 3: Verificar Pipeline

1. Ve a tu proyecto en GitLab
2. Click en **CI/CD → Pipelines**
3. Deberías ver el pipeline ejecutándose automáticamente

### Paso 4: Configurar Variables (Opcional)

Para secrets y configuraciones:

1. Settings → CI/CD → Variables → Expand
2. Add variable: `SLACK_WEBHOOK`, `API_KEY`, etc.
3. ✅ Protect variable (solo en branches protegidas)
4. ✅ Mask variable (ocultar en logs)

### Paso 5: Configurar Schedules (Opcional)

Para builds nocturnos:

1. CI/CD → Schedules → New schedule
2. Description: "Nightly tests"
3. Interval pattern: `0 2 * * *` (2 AM diario)
4. Target branch: `main`

---

## 🎨 Configuración de Deployment a Streamlit Cloud

### Método 1: Streamlit Cloud (Recomendado - Gratis)

#### Paso 1: Conectar con GitHub/GitLab
1. Ve a https://share.streamlit.io/
2. Sign in con tu cuenta GitHub o GitLab
3. Click **"New app"**

#### Paso 2: Configurar App
- **Repository**: Selecciona tu repo `seo-auditor`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: Elige tu subdominio personalizado

#### Paso 3: Configuración Avanzada (Opcional)
- Python version: `3.11`
- ✅ Auto-deploy on push (deployment automático)

#### Paso 4: Deploy
- Click **"Deploy!"**
- Espera 2-3 minutos
- Tu app estará en: `https://TU_APP.streamlit.app`

### Método 2: Heroku (Alternativa)

#### requirements.txt adicional
```txt
gunicorn==21.2.0
```

#### Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Deploy
```powershell
heroku login
heroku create seo-auditor-app
git push heroku main
```

### Método 3: Docker + Cloud Run (Avanzado)

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Deploy a Google Cloud Run
```powershell
gcloud builds submit --tag gcr.io/PROJECT_ID/seo-auditor
gcloud run deploy seo-auditor --image gcr.io/PROJECT_ID/seo-auditor --platform managed
```

---

## 📊 Monitoreo y Mantenimiento

### 1. GitHub Actions - Badges

Agrega al README.md:

```markdown
[![CI/CD Pipeline](https://github.com/TU_USUARIO/seo-auditor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/TU_USUARIO/seo-auditor/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/TU_USUARIO/seo-auditor/branch/main/graph/badge.svg)](https://codecov.io/gh/TU_USUARIO/seo-auditor)
```

### 2. GitLab CI/CD - Badges

Settings → General → Badges:
- Pipeline status
- Coverage report
- Latest release

### 3. Configurar Codecov (Coverage Reports)

1. Ve a https://codecov.io/
2. Sign up con GitHub/GitLab
3. Autoriza acceso al repositorio
4. El workflow ya está configurado para enviar coverage automáticamente

### 4. Monitorear Dependencias

**Dependabot (GitHub)**:
1. Settings → Security → Code security and analysis
2. ✅ Enable Dependabot alerts
3. ✅ Enable Dependabot security updates

**Renovate (GitLab/GitHub)**:
```json
// renovate.json
{
  "extends": ["config:base"],
  "python": {
    "enabled": true
  },
  "schedule": ["before 3am on Monday"]
}
```

---

## 🔧 Troubleshooting

### Problema: Pipeline falla en tests

**Solución:**
```powershell
# Ejecutar tests localmente primero
python -m unittest discover -s tests -v

# Verificar coverage
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

### Problema: Import errors en CI/CD

**Causa**: Dependencias faltantes o versiones incompatibles

**Solución:**
```powershell
# Regenerar requirements.txt limpiamente
pip freeze | grep -E "beautifulsoup4|requests|streamlit" > requirements.txt
```

### Problema: Linting falla pero código funciona

**Solución:**
```powershell
# Auto-fix con black e isort
black .
isort .

# Commit cambios
git add .
git commit -m "style: apply black and isort formatting"
git push
```

### Problema: GitHub Actions minutos agotados

**Soluciones:**
1. **Optimizar cache**: Ya configurado en workflow
2. **Reducir matriz de tests**: Comentar algunas versiones de Python
3. **Upgrade a GitHub Pro**: 3000 minutos/mes
4. **Self-hosted runner**: Ilimitado

```yaml
# Reducir a solo 3.11
strategy:
  matrix:
    python-version: ['3.11']  # Solo una versión
```

### Problema: Deploy a Streamlit Cloud falla

**Checklist:**
- ✅ `requirements.txt` existe y es correcto
- ✅ `app.py` está en la raíz del repo
- ✅ No hay errores de sintaxis en `app.py`
- ✅ Branch seleccionado es `main`

**Logs:**
- Streamlit Cloud → Apps → Tu app → Manage app → Logs

---

## 📈 Optimizaciones Avanzadas

### 1. Cachear Dependencias (Ya configurado)

GitHub Actions:
```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'  # ✓ Ya está
```

GitLab CI:
```yaml
cache:
  paths:
    - .cache/pip  # ✓ Ya está
```

### 2. Paralelizar Tests

```yaml
# GitHub Actions
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.10', '3.11', '3.12']
```

### 3. Conditional Deployments

```yaml
# Solo deploy si todos los tests pasan Y está en main
if: |
  github.ref == 'refs/heads/main' && 
  github.event_name == 'push' &&
  needs.test.result == 'success'
```

### 4. Notificaciones Slack

```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deploy ${{ job.status }} - ${{ github.event.head_commit.message }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

---

## 📝 Checklist Final

### Antes del Primer Push
- [ ] `.gitignore` configurado
- [ ] `requirements.txt` actualizado
- [ ] Tests pasan localmente
- [ ] Linting pasa localmente
- [ ] README.md actualizado

### Después del Primer Push
- [ ] Pipeline ejecuta correctamente
- [ ] Todos los jobs pasan
- [ ] Badges agregados al README
- [ ] Branch protection configurada
- [ ] Codecov integrado

### Para Production
- [ ] Tests de integración agregados
- [ ] Secrets configurados
- [ ] Deployment funciona
- [ ] Monitoring configurado
- [ ] Documentación completa

---

## 🎓 Recursos Adicionales

### GitHub Actions
- [Documentación oficial](https://docs.github.com/en/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Python Actions Tutorial](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

### GitLab CI/CD
- [Documentación oficial](https://docs.gitlab.com/ee/ci/)
- [CI/CD Examples](https://docs.gitlab.com/ee/ci/examples/)
- [Pipeline Efficiency](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)

### Streamlit Cloud
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

### Best Practices
- [12 Factor App](https://12factor.net/)
- [CI/CD Best Practices](https://www.gitops.tech/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa los logs**: Actions/Pipelines → Click en el job fallido
2. **Ejecuta localmente**: Replica el comando que falla en tu máquina
3. **GitHub Issues**: Busca problemas similares en repos con workflows Python
4. **Community**: Stack Overflow tag `github-actions` o `gitlab-ci`

---

✅ **¡Tu proyecto ahora tiene CI/CD completo!**

Cada push ejecutará:
- ✅ Linting automático
- ✅ Tests en múltiples versiones Python
- ✅ Security scanning
- ✅ Build validation
- ✅ Auto-deployment (en main)
- ✅ Notificaciones de estado
