#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
from textwrap import dedent


# -------------------- UTIL --------------------
def write_file(path: Path, content: str, force: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def write_init(path: Path, force: bool = False) -> None:
    """Ensure __init__.py exists in a directory."""
    init_file = path / "__init__.py"
    if not init_file.exists() or force:
        init_file.write_text("# Auto-generated __init__.py\n", encoding="utf-8")


# -------------------- FILES --------------------
def make_pyproject(project_name: str) -> str:
    return dedent(f"""
    [project]
    name = "{project_name}"
    version = "0.1.0"
    description = "DDD FastAPI service"
    requires-python = ">=3.11"
    dependencies = [
      "fastapi[all]>=0.116.1",
      "pydantic>=2.3.0",
      "python-dotenv",
    ]

    [tool.pytest.ini_options]
    addopts = "-q"
    testpaths = ["tests"]
    """).lstrip()


def make_requirements() -> str:
    return dedent("""
    fastapi[all]==0.116.1
    pydantic>=2.3.0
    python-dotenv
    """).lstrip()


def make_importlinter() -> str:
    return dedent("""
    [importlinter]
    root_package = src

    [importlinter:contract:layered-architecture]
    name = Layered architecture
    type = layers
    layers =
        src.api
        src.infrastructure
        src.application
        src.domain
    rules =
        src.api -> src.infrastructure
        src.infrastructure -> src.application
        src.application -> src.domain
    """).lstrip()


def make_dockerfile() -> str:
    return dedent("""
    # syntax=docker/dockerfile:1.4
    FROM python:3.12-slim AS base
    WORKDIR /app
    COPY requirements.txt .
    RUN --mount=type=cache,target=/root/.cache/pip \
        pip install --upgrade pip && pip install -r requirements.txt

    FROM base AS final
    COPY . .
    EXPOSE 8000
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """).lstrip()


def make_compose(project_name: str) -> str:
    return dedent(f"""
    services:
      app:
        build:
          context: ../
          dockerfile: Dockerfile
        container_name: {project_name}-app
        ports:
          - "8000:8000"
        volumes:
          - ../:/app
        env_file:
          - ../.env
        command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    """).lstrip()


def make_makefile() -> str:
    return (
        ".PHONY: run test test-cov lint format precommit-install up down shell sec contracts clean-pyc\n\n"
        "COMPOSE_DEV = docker compose -f infra/docker-compose.yml\n\n"
        "run:\n"
        "\tuvicorn src.main:app --host 0.0.0.0 --port 8000 --reload\n\n"
        "test:\n"
        "\tPYTHONPATH=. pytest -q\n\n"
        "test-cov:\n"
        "\tPYTHONPATH=. pytest --cov=src --cov-report=term-missing\n\n"
        "lint:\n"
        "\truff check --config=ruff.toml src/ --fix\n\n"
        "format:\n"
        '\truff check --config=pyproject.toml src --fix --select I --exclude "migrations"\n'
        "\truff format src\n\n"
        "precommit-install:\n"
        "\tpython -m pip install pre-commit && pre-commit install\n\n"
        "build:\n"
        "\t$(COMPOSE_DEV) build --no-cache\n\n"
        "up:\n"
        "\t$(COMPOSE_DEV) up\n\n"
        "down:\n"
        "\t$(COMPOSE_DEV) down\n\n"
        "shell:\n"
        "\t$(COMPOSE_DEV) exec -it app bash\n\n"
        "sec:\n"
        "\tbandit -r src && \\\n"
        "\tpip-audit -r requirements-tests.txt\n\n"
        "contracts:\n"
        "\tlint-imports\n\n"
        "clean-pyc:\n"
        '\tfind . -type d -name "__pycache__" -exec rm -rf {} +\n'
        '\tfind . -type f -name "*.pyc" -delete\n'
        '\tfind . -type f -name "*.pyo" -delete\n'
    )


def make_gitignore() -> str:
    return dedent("""
    __pycache__/
    *.pyc
    .env
    .venv/
    .env.local
    .cache/
    htmlcov/
    coverage.xml
    .idea/
    .vscode/
    """).lstrip()


def make_pytest_ini() -> str:
    return dedent("""
    [pytest]
    addopts = -ra -q
    python_files = test_*.py
    python_classes = Test*
    testpaths = tests 
    """).lstrip()


def make_ruff_toml() -> str:
    return dedent("""
    line-length = 120

    [lint]
    select = [
        "ANN001", # missing-type-function-argument
        "ANN002", # missing-type-args
        "ANN003", # missing-type-kwargs
        "ANN201", # missing-return-type-undocumented-public-function
        "ANN202", # missing-return-type-private-function
        "ANN205", # missing-return-type-static-method
        "ANN206", # missing-return-type-class-method
        "ANN401", # any_type
        "B904",   # raise-without-from-inside-except
        "RSE102", # Unnecessary parentheses on raised exception
        "T20",    # print_found
        "TRY002", # raise-vanilla-class
        "C4",     # flake8-comprehensions
        "E",      # pycodestyle errors
        "F",      # pyflakes
        "I",      # isort
        "ICN",    # flake8-import-conventions
        "ISC",    # flake8-str-concat
        "RET",    # flake8-return
        "RUF",    # ruff
        "SIM",    # common simplification rules
        "UP",     # pyupgrade
        "W"       # pycodestyle warnings
    ]
    """).lstrip()


def make_requirements_tests() -> str:
    return dedent("""
    -r requirements.txt
    pytest==8.4.1
    pytest-cov==6.2.1
    pytest-mock==3.14.1
    bandit==1.8.5
    pip-audit==2.7.3
    import-linter==2.3
    ruff
    """).lstrip()


def make_precommit() -> str:
    return dedent("""
    repos:
      - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.6.4
        hooks:
          - id: ruff
          - id: ruff-format
      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.6.0
        hooks:
          - id: end-of-file-fixer
          - id: trailing-whitespace
    """).lstrip()


def make_env_example() -> str:
    return dedent("""
    # Example environment variables
    APP_ENV=development
    APP_DEBUG=true
    """).lstrip()


def make_main() -> str:
    return dedent("""
    from fastapi import FastAPI
    from src.api.v1.endpoints import health

    app = FastAPI(title="DDD FastAPI Service")
    app.include_router(health.router, prefix="/v1")
    """).lstrip()


def make_dependencies() -> str:
    return dedent("""
    from fastapi import Depends

    # Placeholder dependencies
    def get_example_dep():
        return "dep"
    """).lstrip()


def make_schemas() -> str:
    return dedent("""
    from pydantic import BaseModel

    class HealthResponse(BaseModel):
        status: str
    """).lstrip()


def make_sample_endpoint() -> str:
    return dedent("""
    from fastapi import APIRouter
    from src.api.v1.schemas import HealthResponse

    router = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    def health():
        return {"status": "ok"}
    """).lstrip()


def make_test_health() -> str:
    return dedent("""
    from fastapi.testclient import TestClient
    from src.main import app

    client = TestClient(app)

    def test_health():
        resp = client.get("/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
    """).lstrip()


def make_config() -> str:
    return dedent("""
    from pydantic import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        app_env: str = "development"
        app_debug: bool = True
        
        model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    settings = Settings()
    """).lstrip()


# -------------------- SCAFFOLD --------------------
def scaffold(project_path: str, project_name: str, force: bool = False) -> None:
    root = Path(project_path) / project_name
    if root.exists() and any(root.iterdir()) and not force:
        print(f"[ERROR] Target path already exists and is not empty: {root}")
        sys.exit(1)

    # Directory structure
    dirs = [
        root / "src",
        root / "src" / "api",
        root / "src" / "api" / "v1" / "endpoints",
        root / "src" / "api" / "v1",
        root / "src" / "application",
        root / "src" / "domain",
        root / "src" / "infrastructure",
        root / "tests" / "api",
        root / "tests" / "application",
        root / "tests" / "domain",
        root / "tests" / "infrastructure",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        write_init(d)  # Add __init__.py

    # Base files
    write_file(root / "pyproject.toml", make_pyproject(project_name), force)
    write_file(root / "requirements.txt", make_requirements(), force)
    write_file(root / "requirements-tests.txt", make_requirements_tests(), force)
    write_file(root / "Dockerfile", make_dockerfile(), force)
    write_file(root / "infra" / "docker-compose.yml", make_compose(project_name), force)
    write_file(root / "Makefile", make_makefile(), force)
    write_file(root / ".gitignore", make_gitignore(), force)
    write_file(root / "pytest.ini", make_pytest_ini(), force)
    write_file(root / ".importlinter", make_importlinter(), force)
    write_file(root / "ruff.toml", make_ruff_toml(), force)
    write_file(root / ".pre-commit-config.yaml", make_precommit(), force)
    write_file(root / ".env.example", make_env_example(), force)
    write_file(root / ".env", make_env_example(), force)

    # Base code
    write_file(root / "src" / "main.py", make_main(), force)
    write_file(
        root / "src" / "api" / "v1" / "dependencies.py", make_dependencies(), force
    )
    write_file(root / "src" / "api" / "v1" / "schemas.py", make_schemas(), force)
    write_file(
        root / "src" / "api" / "v1" / "endpoints" / "health.py",
        make_sample_endpoint(),
        force,
    )
    write_file(root / "src/config.py", make_config(), force)
    write_file(root / "src/.env", make_env_example(), force)
    # Base tests
    write_file(root / "tests" / "api" / "test_health.py", make_test_health(), force)

    print(f"[OK] Project generated at: {root}")


# -------------------- ARGPARSE --------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold DDD FastAPI project")
    parser.add_argument(
        "--path", "-p", required=True, help="Path to generate the project"
    )
    parser.add_argument("--name", "-n", required=True, help="Project name")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing files"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scaffold(args.path, args.name, force=args.force)


if __name__ == "__main__":
    main()
