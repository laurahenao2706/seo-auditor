# ⚡ Quick Start - CI/CD en 5 Minutos

> 🎯 **Objetivo**: Tener tu pipeline CI/CD funcionando en menos de 5 minutos

---

## 📋 Pre-requisitos

- ✅ Python 3.10+ instalado
- ✅ Git instalado
- ✅ Cuenta en GitHub o GitLab
- ✅ Código del proyecto (ya lo tienes ✅)

---

## 🚀 Opción A: GitHub Actions (Recomendado)

### Paso 1: Crear Repositorio en GitHub (1 min)

1. Ve a: https://github.com/new
2. Nombre: `seo-auditor` (o el que prefieras)
3. Visibilidad: Público o Privado
4. **NO** marques "Initialize with README"
5. Click "Create repository"

### Paso 2: Conectar y Subir Código (2 min)

```powershell
# En la carpeta del proyecto
cd "C:\Users\laura.munoz_pragma\Desktop\SEO py"

# Inicializar Git (si aún no está)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: SEO Auditor with CI/CD"

# Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/seo-auditor.git

# Cambiar a branch main
git branch -M main

# Subir código
git push -u origin main
```

### Paso 3: Ver Pipeline en Acción (1 min)

1. Ve a tu repo: `https://github.com/TU_USUARIO/seo-auditor`
2. Click en tab **"Actions"**
3. Verás el workflow "CI/CD Pipeline" ejecutándose
4. Click en el workflow para ver detalles en tiempo real

### Paso 4: Verificar Resultados (1 min)

Espera ~13 minutos para que el pipeline complete. Deberías ver:

- ✅ **Linting**: Black, isort, Flake8, MyPy
- ✅ **Testing**: Python 3.10, 3.11, 3.12 en Ubuntu/Windows
- ✅ **Security**: Safety, Bandit
- ✅ **Build**: Validación de Streamlit app
- ✅ **All checks passed!**

---

## 🚀 Opción B: GitLab CI/CD

### Paso 1: Crear Proyecto en GitLab (1 min)

1. Ve a: https://gitlab.com/projects/new
2. Click "Create blank project"
3. Project name: `seo-auditor`
4. Visibility: Private o Public
5. Click "Create project"

### Paso 2: Conectar y Subir Código (2 min)

```powershell
# En la carpeta del proyecto
cd "C:\Users\laura.munoz_pragma\Desktop\SEO py"

# Inicializar Git (si aún no está)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: SEO Auditor with CI/CD"

# Conectar con GitLab (reemplaza TU_USUARIO)
git remote add origin https://gitlab.com/TU_USUARIO/seo-auditor.git

# Cambiar a branch main
git branch -M main

# Subir código
git push -u origin main
```

### Paso 3: Ver Pipeline en Acción (1 min)

1. Ve a tu proyecto: `https://gitlab.com/TU_USUARIO/seo-auditor`
2. Menú izquierda → **CI/CD** → **Pipelines**
3. Verás el pipeline ejecutándose automáticamente
4. Click en el pipeline para ver stages

### Paso 4: Verificar Resultados (1 min)

El pipeline tiene 6 stages:

- ✅ **lint**: Black, isort, Flake8, MyPy
- ✅ **test**: Python 3.10, 3.11, 3.12
- ✅ **security**: Safety, Bandit
- ✅ **build**: Validación app
- ✅ **deploy**: (solo en main)
- ✅ **notify**: Notificaciones

---

## 🎨 Bonus: Deploy a Streamlit Cloud (2 min)

### Para GitHub:

1. Ve a: https://share.streamlit.io/
2. Click "New app"
3. Conecta con GitHub
4. Selecciona tu repositorio
5. Main file: `app.py`
6. Click "Deploy"

### Para GitLab:

1. Ve a: https://share.streamlit.io/
2. Click "New app"
3. Conecta con GitLab
4. Selecciona tu proyecto
5. Main file: `app.py`
6. Click "Deploy"

**Tu app estará live en**: `https://TU_USUARIO-seo-auditor.streamlit.app`

---

## 🔧 Comandos Útiles

```powershell
# Ver status de Git
git status

# Ver logs del pipeline (GitHub CLI)
gh run list
gh run view --log

# Ver branches
git branch -a

# Crear nuevo branch
git checkout -b feature/nueva-funcionalidad

# Volver a main
git checkout main

# Pull últimos cambios
git pull origin main
```

---

## 🐛 Troubleshooting Rápido

### Problema: "remote origin already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/seo-auditor.git
```

### Problema: "Authentication failed"

**GitHub**: Usa Personal Access Token en vez de password
1. Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → Selecciona `repo` scope
3. Usa el token como password

**GitLab**: Usa Personal Access Token
1. Settings → Access Tokens
2. Create personal access token → Selecciona `api` y `write_repository`
3. Usa el token como password

### Problema: Pipeline falla en tests

```powershell
# Ejecutar tests localmente primero
python -m unittest discover -s tests -v

# Si fallan, revisa los errores y corrige
# Luego commit y push de nuevo
git add .
git commit -m "fix: corrección de tests"
git push
```

### Problema: Linting falla

```powershell
# Auto-fix con black e isort
pip install black isort
black .
isort .

# Commit cambios
git add .
git commit -m "style: apply formatting"
git push
```

---

## 📊 Verificación Final

### Checklist ✅

- [ ] Código subido a GitHub/GitLab
- [ ] Pipeline visible en Actions/Pipelines
- [ ] Pipeline ejecutándose (color amarillo/azul)
- [ ] Esperar a que termine (~13 min)
- [ ] Pipeline exitoso (verde ✅)
- [ ] Badges visibles en README (opcional)
- [ ] App deployada en Streamlit Cloud (opcional)

### Si Todo Está Verde

**🎉 ¡Felicitaciones! Tu CI/CD está funcionando.**

Ahora cada vez que hagas push:
1. Pipeline se ejecuta automáticamente
2. Tests corren en múltiples versiones
3. Linting valida el código
4. Security escanea vulnerabilidades
5. Deploy automático a producción (en main)

---

## 📚 ¿Qué Sigue?

1. **Lee la documentación completa**:
   - [EXECUTIVE_SUMMARY_CICD.md](EXECUTIVE_SUMMARY_CICD.md) - Resumen ejecutivo
   - [ANALISIS_CICD.md](ANALISIS_CICD.md) - Por qué GitHub Actions
   - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guía detallada
   - [CICD_BEST_PRACTICES.md](CICD_BEST_PRACTICES.md) - Optimizaciones

2. **Configura protección de branches**:
   - Settings → Branches → Add rule
   - Branch: `main`
   - ✅ Require status checks before merging

3. **Agrega badges al README**:
   - Edita README.md
   - Reemplaza `TU_USUARIO` con tu usuario real

4. **Configura notificaciones**:
   - Slack webhook (opcional)
   - Email notifications (GitHub settings)

5. **Haz tu primer PR**:
   - Crea branch: `git checkout -b feature/test`
   - Haz un cambio
   - Push y crea Pull Request
   - Verás el pipeline ejecutarse en el PR

---

## 🆘 Ayuda

**¿Pipeline falla?**
- Revisa los logs en Actions/Pipelines
- Click en el job que falló
- Busca el error en rojo
- Copia el error y búscalo en Google/Stack Overflow

**¿Necesitas ayuda?**
- GitHub Community: https://github.community/
- Stack Overflow: `[github-actions]` o `[gitlab-ci]`
- Documentación: Links en la sección anterior

---

## ⏱️ Resumen de Tiempos

| Tarea | Tiempo |
|-------|--------|
| Crear repositorio | 1 min |
| Subir código | 2 min |
| Ver pipeline | 1 min |
| Verificar resultados | 1 min |
| **TOTAL** | **5 min** ⚡ |

*Nota: Pipeline tarda ~13 min en ejecutar, pero no necesitas esperar. Puedes hacer otras cosas.*

---

**🚀 ¡Manos a la obra! En 5 minutos tendrás CI/CD funcionando.**

Cualquier duda, consulta la documentación completa o los recursos de ayuda.

**¡Éxito!** 🎉
