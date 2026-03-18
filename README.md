# SEO Checklist Auditor

[![CI/CD](https://github.com/laurahenao2706/seo-auditor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/laurahenao2706/seo-auditor/actions/workflows/ci-cd.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Framework en Python para auditar SEO técnico de una URL con enfoque en POO, SOLID y arquitectura por capas.

## ✨ Características

- 🏗️ **Arquitectura Hexagonal**: Separación en capas (domain, application, infrastructure)
- 🧪 **Tests Unitarios**: Cobertura de tests incluida
- 🔄 **CI/CD**: Pipeline automático con GitHub Actions
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

## 🚀 Instalación

### Requisitos
- Python 3.10+

### Setup

```bash
# Clonar repositorio
git clone https://github.com/laurahenao2706/seo-auditor.git
cd seo-auditor

# Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Uso

### Aplicación Web (Streamlit)

```bash
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`

### CLI

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

El proyecto incluye un pipeline simple de CI/CD con GitHub Actions:

- **Linting**: Black + Flake8
- **Tests**: Unitarios automáticos
- **Notificaciones**: Estado del pipeline

El pipeline se ejecuta automáticamente en cada push a `main` o en Pull Requests.

### Ver Pipeline
- Ve a la pestaña [Actions](../../actions) en GitHub
- Cada commit muestra el estado del pipeline

---

## 📊 Funcionalidad

- ✅ Auditoría de 30 reglas SEO técnicas
- ✅ Estados: PASS, FAIL, WARN, MANUAL
- ✅ Exportación a JSON y CSV
- ✅ Interfaz web + CLI

---

## 🛣️ Roadmap

- [ ] Agregar más reglas SEO
- [ ] Security scanning en CI/CD
- [ ] Tests en múltiples versiones de Python
- [ ] Coverage reporting
- [ ] Deploy automático a Streamlit Cloud

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