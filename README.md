<div align="center">
<h1>py-log-analyzer</h1>

<p>High-performance modular CLI tool to parse, analyze and audit Nginx/Apache logs with interactive dashboards and anomaly detection.</p>

  <img src="assets/python.png" alt="py-log-analyzer banner" width="600px">

  <br>

[![CI](https://github.com/esousa97/py-log-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/esousa97/py-log-analyzer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)](https://github.com/esousa97/py-log-analyzer/blob/master/pyproject.toml)
[![Rich](https://img.shields.io/badge/rich-15.0%2B-green?style=flat&logo=python&logoColor=white)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/github/license/esousa97/py-log-analyzer)](https://github.com/esousa97/py-log-analyzer/blob/master/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/esousa97/py-log-analyzer)](https://github.com/esousa97/py-log-analyzer/commits/master)

</div>

---

**py-log-analyzer** is a command-line tool designed for high-performance analysis of web server logs (Nginx/Apache). It features memory-efficient parsing using generators, parallel file processing via multiprocessing, and comprehensive reporting. It identifies traffic patterns, status code distributions, and suspicious IP activity (anomalies), exporting results to **JSON** or interactive **HTML dashboards**. The console entry point is `py-log-analyzer`. Canonical repository: `github.com/esousa97/py-log-analyzer`.

## Demo (quick smoke test)

Analyze a log file and generate an interactive HTML report.

**Linux / macOS (bash)**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run analysis with HTML report
py-log-analyzer access.log --format html --threshold 2.5
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# Run analysis with HTML report
py-log-analyzer access.log --format html --threshold 2.5
```

## Features

| Area | What you get |
| ---- | -------------- |
| Parsing | High-speed regex parsing of Common Log Format (CLF). |
| Performance | Memory-efficient generators and multi-core `multiprocessing` support. |
| Security | Anomaly detection for suspicious IPs (401/404 spikes). |
| Health | Service health monitoring with configurable 5xx error thresholds. |
| Export | Interactive **HTML reports** with Chart.js or structured **JSON**. |
| UI | Elegant terminal tables and panels powered by `rich`. |

## Tech stack

| Component | Role |
| --------- | ---- |
| Python 3.10+ | Language and runtime |
| rich | Terminal UI and tables |
| Chart.js | Interactive HTML visualizations |
| pytest | Unit testing and coverage |

## Prerequisites

- Python **3.10+** and `pip`.
- Optional: **Docker** for containerized execution.

## Installation and usage

### From source (recommended)

```bash
git clone https://github.com/esousa97/py-log-analyzer.git
cd py-log-analyzer
pip install .
py-log-analyzer --help
```

### Docker

```bash
docker build -t py-log-analyzer .
docker run --rm -v "$PWD:/logs" py-log-analyzer /logs/access.log --format html
```

## Documentation

| Document | Contents |
| -------- | -------- |
| [LICENSE](LICENSE) | MIT License |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## CLI summary

```bash
py-log-analyzer FILES [FILES ...] [--threshold PERCENT] [--format json|html]
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=py_log_analyzer
```

## Project layout

| Path | Role |
| ---- | ---- |
| `py_log_analyzer/parser.py` | Log parsing and generators |
| `py_log_analyzer/analyzer.py` | Data aggregation and anomaly detection |
| `py_log_analyzer/exporter.py` | JSON and HTML report generation |
| `py_log_analyzer/cli.py` | CLI orchestration and Terminal UI |
| `py_log_analyzer/__main__.py` | Module entry point |
| `tests/` | `pytest` suite |

## Troubleshooting

| Symptom | Likely cause | What to do |
| ------- | ------------- | ---------- |
| `ModuleNotFoundError` | Package not installed | Run `pip install .` or `pip install -e .` |
| `Permission Denied` | File access issues | Check log file permissions or use `sudo` if necessary. |
| `MemoryError` | Large file loading | The tool uses generators, but check if `--format html` with extreme log sizes is a factor. |

## Study roadmap (completed)

The implementation roadmap is **finished**.

### Delivered scope

- [x] **Stage 1 — Base CLI & Parsing** — Regex-based CLF parsing and basic terminal output.
- [x] **Stage 2 — Aggregation & UI** — Top IPs/Paths/Status distributions with `rich` tables.
- [x] **Stage 3 — Anomaly & Health** — Suspicious IP detection and 5xx health alerts.
- [x] **Stage 4 — Export & Visualization** — HTML dashboards with Chart.js and JSON export.
- [x] **Stage 5 — Performance & Scale** — Generators for RAM efficiency and `multiprocessing` for parallel files.
- [x] **Stage 6 — DevOps & CI/CD** — Dockerization and GitHub Actions for automated testing/linting.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE).

<div align="center">

## Author

**Enoque Sousa**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/enoque-sousa-bb89aa168/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/esousa97)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=flat&logo=target&logoColor=white)](https://enoquesousa.vercel.app)

**[⬆ Back to Top](#py-log-analyzer)**

Made with ❤️ by [Enoque Sousa](https://github.com/esousa97)

**Project status:** Study project

</div>
