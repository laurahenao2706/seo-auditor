#!/usr/bin/env python3
"""
Script de configuración de entorno de desarrollo
Automatiza la configuración inicial del proyecto

Uso:
    python setup_dev.py
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Ejecuta un comando y reporta el resultado"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - COMPLETADO")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FALLÓ")
        if e.stderr:
            print(e.stderr)
        return False


def check_python_version() -> bool:
    """Verifica que la versión de Python sea >= 3.10"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
    else:
        print(f"❌ Python 3.10+ requerido. Actual: {version.major}.{version.minor}")
        return False


def create_venv() -> bool:
    """Crea entorno virtual si no existe"""
    if Path("venv").exists():
        print("ℹ️  Entorno virtual ya existe")
        return True
    
    return run_command(
        f"{sys.executable} -m venv venv",
        "Crear entorno virtual"
    )


def get_pip_cmd() -> str:
    """Retorna el comando pip según el OS"""
    if sys.platform == "win32":
        return "venv\\Scripts\\pip"
    return "venv/bin/pip"


def get_python_cmd() -> str:
    """Retorna el comando python según el OS"""
    if sys.platform == "win32":
        return "venv\\Scripts\\python"
    return "venv/bin/python"


def install_dependencies() -> bool:
    """Instala dependencias de desarrollo"""
    pip = get_pip_cmd()
    
    success = True
    
    # Actualizar pip
    success &= run_command(
        f"{pip} install --upgrade pip",
        "Actualizar pip"
    )
    
    # Instalar dependencias principales
    success &= run_command(
        f"{pip} install -r requirements.txt",
        "Instalar dependencias principales"
    )
    
    # Instalar dependencias de desarrollo
    success &= run_command(
        f"{pip} install -r requirements-dev.txt",
        "Instalar dependencias de desarrollo"
    )
    
    return success


def setup_pre_commit() -> bool:
    """Configura pre-commit hooks"""
    python_cmd = get_python_cmd()
    
    # Crear configuración de pre-commit si no existe
    pre_commit_config = Path(".pre-commit-config.yaml")
    if not pre_commit_config.exists():
        config_content = """repos:
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
"""
        pre_commit_config.write_text(config_content)
        print("✅ Archivo .pre-commit-config.yaml creado")
    
    return run_command(
        f"{python_cmd} -m pre_commit install",
        "Instalar pre-commit hooks"
    )


def run_tests() -> bool:
    """Ejecuta tests para verificar instalación"""
    python_cmd = get_python_cmd()
    return run_command(
        f"{python_cmd} -m unittest discover -s tests -v",
        "Ejecutar tests unitarios"
    )


def run_linting() -> bool:
    """Ejecuta herramientas de linting"""
    python_cmd = get_python_cmd()
    
    print("\n🔍 Ejecutando herramientas de linting...")
    
    # Black (check only)
    run_command(
        f"{python_cmd} -m black --check .",
        "Verificar formateo con Black"
    )
    
    # isort (check only)
    run_command(
        f"{python_cmd} -m isort --check-only .",
        "Verificar imports con isort"
    )
    
    # Flake8
    run_command(
        f"{python_cmd} -m flake8 seo_auditor/",
        "Análisis con Flake8"
    )
    
    return True


def init_git() -> bool:
    """Inicializa repositorio git si no existe"""
    if Path(".git").exists():
        print("ℹ️  Repositorio Git ya existe")
        return True
    
    success = run_command("git init", "Inicializar repositorio Git")
    
    if success:
        print("\n📝 Próximos pasos:")
        print("   1. git add .")
        print("   2. git commit -m 'Initial commit'")
        print("   3. git remote add origin <URL>")
        print("   4. git push -u origin main")
    
    return success


def print_summary():
    """Imprime resumen final"""
    print("\n" + "="*60)
    print("🎉 ¡CONFIGURACIÓN COMPLETA!")
    print("="*60)
    
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"""
📚 Comandos útiles:

  Activar entorno virtual:
    {activate_cmd}

  Ejecutar tests:
    python -m unittest discover -s tests -v

  Ejecutar con coverage:
    python -m coverage run -m unittest discover -s tests
    python -m coverage report
    python -m coverage html

  Formatear código:
    python -m black .
    python -m isort .

  Linting:
    python -m flake8 seo_auditor/
    python -m mypy seo_auditor/

  Ejecutar app Streamlit:
    streamlit run app.py

  Ejecutar CLI:
    python seo_checker.py https://www.ejemplo.com

  Verificar seguridad:
    python -m safety check
    python -m bandit -r seo_auditor/

📖 Documentación:
  - README.md
  - ANALISIS_CICD.md
  - DEPLOYMENT_GUIDE.md

🚀 Para CI/CD:
  - GitHub Actions: .github/workflows/ci-cd.yml
  - GitLab CI/CD: .gitlab-ci.yml

💡 Próximos pasos:
  1. Revisar y ajustar pyproject.toml según necesidades
  2. Configurar pre-commit: pre-commit install
  3. Subir código a GitHub/GitLab
  4. Verificar que pipeline ejecuta correctamente
  5. Configurar deployment a Streamlit Cloud
""")


def main():
    """Función principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║         Setup de Desarrollo - SEO Auditor               ║
║              Configuración Automatizada                  ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_venv():
        print("❌ Error al crear entorno virtual")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("⚠️  Algunas dependencias fallaron, pero continuando...")
    
    # Setup pre-commit
    setup_pre_commit()
    
    # Inicializar Git
    init_git()
    
    # Ejecutar tests
    print("\n🧪 Verificando instalación con tests...")
    if not run_tests():
        print("⚠️  Algunos tests fallaron, revisar antes de continuar")
    
    # Ejecutar linting
    run_linting()
    
    # Resumen final
    print_summary()


if __name__ == "__main__":
    main()
