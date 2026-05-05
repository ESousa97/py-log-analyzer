# Python Log Analyzer

![Python CI](https://github.com/esousa97/py-log-analyzer/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A high-performance, modular CLI tool to parse and analyze Nginx/Apache log files. Designed for scalability, it handles large log files efficiently using Python generators and parallel processing.

## 🚀 Features

- **Performance First**: Memory-efficient processing via generators and multi-core scalability via `multiprocessing`.
- **Modular Architecture**: Clean, extensible code structure following Python best practices.
- **Anomaly Detection**: Automatically identifies suspicious IP activity (401/404 spikes).
- **Service Health Alerts**: Real-time monitoring with configurable 5xx error thresholds.
- **Rich Visualization**: 
  - Elegant terminal tables powered by `rich`.
  - Interactive HTML dashboards with Chart.js.
  - Structured JSON exports for data integration.
- **Modern Tooling**: Fully integrated with `ruff` for linting, `pytest` for testing, and `GitHub Actions` for CI/CD.
- **Docker Ready**: Run anywhere as an isolated utility.

## 🛠️ Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/esousa97/py-log-analyzer.git
   cd py-log-analyzer
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # .\venv\Scripts\activate # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install .
   ```

### Docker

```bash
docker build -t py-log-analyzer .
```

## 📖 Usage

### CLI Commands

The tool can be run directly if installed via `pip install .`, or via `python -m py_log_analyzer`.

```bash
# Basic analysis of multiple files
py-log-analyzer access.log access.log.1

# Export to HTML with custom error threshold
py-log-analyzer access.log --format html --threshold 2.5
```

### Docker Usage

```bash
docker run --rm -v $(pwd):/logs py-log-analyzer /logs/access.log --format json
```

## 🧪 Development

We value code quality and testing.

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=py_log_analyzer

# Lint and format
ruff check .
ruff format .
```

## 🤝 Contributing

Contributions are welcome! Please check our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.
