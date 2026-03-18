#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de inicialización de Git para SEO Auditor

.DESCRIPTION
    Automatiza la configuración inicial de Git, incluyendo:
    - Inicialización del repositorio
    - Primer commit
    - Configuración de remote
    - Creación de branches
    - Setup de pre-commit hooks

.PARAMETER Remote
    URL del repositorio remoto (GitHub/GitLab)

.PARAMETER Platform
    Plataforma: 'github' o 'gitlab' (default: github)

.EXAMPLE
    .\init_git.ps1 -Remote "https://github.com/usuario/seo-auditor.git"

.EXAMPLE
    .\init_git.ps1 -Remote "https://gitlab.com/usuario/seo-auditor.git" -Platform gitlab
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Remote = "",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('github', 'gitlab')]
    [string]$Platform = "github"
)

# Colores para output
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }

Write-Host @"

╔══════════════════════════════════════════════════════════╗
║         Inicialización Git - SEO Auditor                 ║
║              Configuración Automatizada                  ║
╚══════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Verificar si Git está instalado
try {
    $gitVersion = git --version
    Write-Success "Git detectado: $gitVersion"
} catch {
    Write-Error "Git no está instalado. Descarga desde: https://git-scm.com/"
    exit 1
}

# Verificar si ya es un repositorio Git
if (Test-Path ".git") {
    Write-Warning "Este directorio ya es un repositorio Git"
    $continue = Read-Host "¿Deseas continuar? (s/n)"
    if ($continue -ne "s") {
        exit 0
    }
} else {
    # Inicializar repositorio
    Write-Info "Inicializando repositorio Git..."
    git init
    Write-Success "Repositorio inicializado"
}

# Configurar user.name y user.email si no están configurados
$userName = git config user.name
$userEmail = git config user.email

if (-not $userName) {
    Write-Info "Configurando Git user.name..."
    $userName = Read-Host "Ingresa tu nombre"
    git config user.name "$userName"
}

if (-not $userEmail) {
    Write-Info "Configurando Git user.email..."
    $userEmail = Read-Host "Ingresa tu email"
    git config user.email "$userEmail"
}

Write-Success "Git configurado para: $userName <$userEmail>"

# Crear .gitignore si no existe
if (-not (Test-Path ".gitignore")) {
    Write-Warning ".gitignore no encontrado"
    Write-Info "El archivo .gitignore debería haberse creado. Verifica el proyecto."
}

# Agregar todos los archivos
Write-Info "Agregando archivos al staging..."
git add .

# Verificar estado
$status = git status --porcelain
if ($status) {
    Write-Info "Archivos a commitear:"
    git status --short
    
    # Primer commit
    Write-Info "Creando commit inicial..."
    git commit -m "Initial commit: SEO Auditor with CI/CD pipeline

- Arquitectura hexagonal (Clean Architecture)
- Tests unitarios con coverage
- CI/CD pipeline (GitHub Actions + GitLab CI)
- Linting y formateo automático
- Security scanning
- Streamlit web app + CLI
- Deployment automation
- Comprehensive documentation"
    
    Write-Success "Commit inicial creado"
} else {
    Write-Info "No hay cambios para commitear"
}

# Renombrar branch a 'main' si es 'master'
$currentBranch = git branch --show-current
if ($currentBranch -eq "master") {
    Write-Info "Renombrando branch 'master' a 'main'..."
    git branch -M main
    Write-Success "Branch renombrado a 'main'"
}

# Configurar remote si se proporcionó
if ($Remote) {
    Write-Info "Configurando remote origin..."
    
    # Verificar si remote ya existe
    $existingRemote = git remote get-url origin 2>$null
    if ($existingRemote) {
        Write-Warning "Remote 'origin' ya existe: $existingRemote"
        $updateRemote = Read-Host "¿Deseas actualizarlo? (s/n)"
        if ($updateRemote -eq "s") {
            git remote set-url origin $Remote
            Write-Success "Remote actualizado"
        }
    } else {
        git remote add origin $Remote
        Write-Success "Remote configurado: $Remote"
    }
    
    # Preguntar si hacer push
    $doPush = Read-Host "¿Deseas hacer push al remote? (s/n)"
    if ($doPush -eq "s") {
        Write-Info "Haciendo push a origin/main..."
        try {
            git push -u origin main
            Write-Success "Push completado exitosamente"
        } catch {
            Write-Error "Error al hacer push. Verifica tus credenciales y permisos."
        }
    }
}

# Crear branch develop
Write-Info "¿Deseas crear branch 'develop'? (Recomendado para Gitflow)"
$createDevelop = Read-Host "(s/n)"
if ($createDevelop -eq "s") {
    git checkout -b develop
    git checkout main
    Write-Success "Branch 'develop' creado"
}

# Instalar pre-commit hooks
if (Test-Path ".pre-commit-config.yaml") {
    Write-Info "¿Deseas instalar pre-commit hooks?"
    $installHooks = Read-Host "(s/n)"
    if ($installHooks -eq "s") {
        try {
            pip install pre-commit
            pre-commit install
            Write-Success "Pre-commit hooks instalados"
            Write-Info "Ejecutando pre-commit en todos los archivos..."
            pre-commit run --all-files
        } catch {
            Write-Warning "Error al instalar pre-commit. Instalar manualmente con: pip install pre-commit"
        }
    }
}

# Resumen final
Write-Host @"

╔══════════════════════════════════════════════════════════╗
║              ✅ Configuración Completada                  ║
╚══════════════════════════════════════════════════════════╝

📊 Estado del repositorio:
   Branch actual: $(git branch --show-current)
   Último commit: $(git log -1 --oneline)
   Remote: $(git remote get-url origin 2>$null)

📝 Próximos pasos:

"@ -ForegroundColor Green

if ($Platform -eq "github") {
    Write-Host @"
   GitHub Actions:
   1. Sube tu código a GitHub (si aún no lo hiciste)
   2. Ve a tu repositorio → Actions
   3. El pipeline ejecutará automáticamente
   4. Configura Streamlit Cloud:
      - https://share.streamlit.io/
      - Conecta tu repositorio
      - Selecciona app.py
   5. Configura branch protection:
      - Settings → Branches → Add rule
      - Branch: main
      - ✅ Require status checks

"@ -ForegroundColor Yellow
} else {
    Write-Host @"
   GitLab CI/CD:
   1. Sube tu código a GitLab (si aún no lo hiciste)
   2. Ve a tu proyecto → CI/CD → Pipelines
   3. El pipeline ejecutará automáticamente
   4. Configura variables:
      - Settings → CI/CD → Variables
   5. Configura protected branches:
      - Settings → Repository → Protected branches

"@ -ForegroundColor Yellow
}

Write-Host @"
   📚 Documentación:
   - README.md - Información general
   - ANALISIS_CICD.md - Análisis de herramientas
   - DEPLOYMENT_GUIDE.md - Guía de deployment
   - CICD_BEST_PRACTICES.md - Mejores prácticas

   🛠️  Comandos útiles:
   - git status                    # Ver estado
   - git log --oneline --graph     # Ver historial
   - git push origin main          # Push a remote
   - pre-commit run --all-files    # Ejecutar hooks

"@ -ForegroundColor Cyan

Write-Success "¡Repositorio listo para desarrollo con CI/CD!"
