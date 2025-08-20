# FastAPI DDD Project Scaffolder

This repository provides a simple Python script to scaffold a **FastAPI project** following a **Domain-Driven Design (DDD)** folder structure.  
It also sets up essential tools such as **Ruff**, **pytest**, **pre-commit**, **Bandit**, **pip-audit**, and **Import Linter** to ensure high code quality from the start.

---

## 📦 Features

- ✅ FastAPI with DDD structure (`src/api`, `src/application`, `src/domain`, `src/infrastructure`)  
- ✅ Dockerfile & docker-compose setup  
- ✅ Linting and formatting with [Ruff](https://github.com/astral-sh/ruff)  
- ✅ Testing with [pytest](https://docs.pytest.org/) and coverage reports  
- ✅ Security checks with [bandit](https://bandit.readthedocs.io/) and [pip-audit](https://pypi.org/project/pip-audit/)  
- ✅ Import contracts with [import-linter](https://github.com/seddonym/import-linter)  
- ✅ Pre-commit hooks (black, ruff, trailing whitespace, etc.)  

---

## 🚀 Usage

### 1. Clone this repository
```bash
git clone https://github.com/fabianfalon/fastapi-ddd-scaffolder.git
cd fastapi-ddd-scaffolder
```

### 2. Run the scaffolder
```bash
python scaffold.py --path ./projects --name my-service
```

This will generate the project under `./projects/my-service`.

### 3. Explore the generated structure
```
my-service/
├── infra/
│   └── docker-compose.yml
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── health.py
│   │       ├── dependencies.py
│   │       └── schemas.py
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── main.py
├── tests/
│   └── api/
│       └── test_health.py
├── .importlinter
├── .pre-commit-config.yaml
├── .gitignore
├── .env.example
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-tests.txt
├── ruff.toml
└── pytest.ini
```

### 4. Use Makefile commands
```bash
make run           # Run the FastAPI app with uvicorn
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run Ruff lint
make format        # Format code
make sec           # Run security checks (bandit + pip-audit)
make contracts     # Run Import Linter contracts
make build         # Build docker image
make up            # Start docker-compose
make down          # Stop docker-compose
```

---

## 🛠 Requirements

- Python **>=3.11**
- Docker & Docker Compose (optional, for containerized runs)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
