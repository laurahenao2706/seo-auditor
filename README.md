# SEO Checklist Auditor

[![CI/CD](https://github.com/laurahenao2706/seo-auditor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/laurahenao2706/seo-auditor/actions/workflows/ci-cd.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Framework en Python para auditar SEO técnico de una URL con enfoque en POO, SOLID y arquitectura por capas.

## ✨ Características

- 🏗️ **Arquitectura Hexagonal**: Separación en capas (domain, application, infrastructure)
- 🧪 **Tests Unitarios**: Cobertura de tests incluida
- 🔄 **CI/CD**: Pipeline automático con GitHub Actions + Docker build
- ☁️ **GitHub Codespaces**: Desarrollo en la nube sin instalación
- 🐳 **Docker**: Contenedores listos para desarrollo y producción
- 🎨 **Interfaz Dual**: Web app (Streamlit) + CLI
- 📊 **Exportación**: Resultados en JSON y CSV

## Estructura

```text
SEO/
|--📁 Estructura del Proyecto

```
seo-auditor/
├── seo_auditor/       # Código principal (arquitectura hexagonal)
│   ├── domain/        # Lógica de negocio
│   ├── application/   # Casos de uso y servicios
│   └── infrastructure/# Adaptadores externos
├── tests/             # Tests unitarios
├── app.py             # Aplicación Streamlit
├── seo_checker.py     # CLI
└── requirements.txt   # Dependencias
- Python 3.10+
- Dependencias de requirements.txt

## Instalacion

```bash
python -m pip install -r requirements.txt
```

## 🚀 Inicio Rápido

### ⭐ Opción 1: GitHub Codespaces (Recomendado - SIN INSTALACIÓN)

**La forma más fácil de empezar. Todo en la nube, gratis 60h/mes.**

1. Click en el botón `Code` → `Codespaces` → `Create codespace on main`
2. Espera 30 segundos (crea ambiente con Docker incluido)
3. En la terminal del Codespace:
   ```bash
   docker-compose up
   ```
4. Cuando aparezca "Open in Browser", haz click para ver la app

**Ventajas:**
- ✅ Sin instalar nada en tu PC
- ✅ Docker ya incluido
- ✅ VS Code completo en el navegador
- ✅ 60 horas gratis al mes

---

### 🐳 Opción 2: Docker Local

**Si tienes Docker instalado localmente:**

#### Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/laurahenao2706/seo-auditor.git
cd seo-auditor

# Opción 1: Con docker-compose (más fácil)
docker-compose up

# Opción 2: Con Docker directamente
docker build -t seo-auditor .
docker run -p 8501:8501 seo-auditor
```

**Acceso**: Abre tu navegador en `http://localhost:8501`

#### Comandos Útiles

```bash
# Detener la aplicación
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar tests en Docker
docker-compose run tests

# Reconstruir imagen después de cambios
docker-compose up --build
```

#### Usar Imagen Pre-construida (desde GitHub)

```bash
# Descargar y ejecutar imagen publicada en CI/CD
docker run -p 8501:8501 ghcr.io/laurahenao2706/seo-auditor:latest
```

**Nota**: La imagen se construye automáticamente en cada push a `main` y se publica gratis en GitHub Container Registry.

---

### 💻 Opción 3: Python Local (Sin Docker)

**Si prefieres trabajar directamente con Python:**

#### Requisitos
- Python 3.10+

#### Setup

```bash
# Clonar repositorio
git clone https://github.com/laurahenao2706/seo-auditor.git
cd seo-auditor

# Instalar dependencias
pip install -r requirements.txt
```

#### Aplicación Web (Streamlit)

```bash
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`

#### CLI

```bash
# Análisis básico
python seo_checker.py https://www.ejemplo.com

# Con exportación
python seo_checker.py https://www.ejemplo.com --out-json reporte.json --out-csv reporte.csv
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m unittest discover -s tests -v

# Ejecutar tests específicos
python -m unittest tests.test_service -v
```

---

## 🔄 CI/CD

El proyecto incluye un pipeline completo de CI/CD con GitHub Actions:

- **Linting**: Black + Flake8
- **Tests**: Unitarios automáticos
- **Docker Build**: Construcción automática de imagen Docker
- **Registry**: Publicación gratis en GitHub Container Registry (ghcr.io)
- **Notificaciones**: Estado del pipeline

El pipeline se ejecuta automáticamente en cada push a `main` o en Pull Requests.

### Ver Pipeline
- Ve a la pestaña [Actions](../../actions) en GitHub
- Cada commit muestra el estado del pipeline
- Las imágenes Docker se publican en [Packages](../../packages)

---

## 📊 Funcionalidad

- ✅ Auditoría de 30 reglas SEO técnicas
- ✅ Estados: PASS, FAIL, WARN, MANUAL
- ✅ Exportación a JSON y CSV
- ✅ Interfaz web + CLI

---

## 🛣️ Roadmap

- [x] CI/CD básico con GitHub Actions
- [x] Contenerización con Docker
- [x] Publicación automática en GitHub Container Registry
- [x] GitHub Codespaces para desarrollo cloud
- [ ] Agregar más reglas SEO
- [ ] Security scanning en CI/CD
- [ ] Tests en múltiples versiones de Python
- [ ] Coverage reporting
- [ ] Deploy a cloud provider (Azure/AWS/GCP)

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License