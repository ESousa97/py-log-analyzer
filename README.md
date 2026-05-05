# Python Log Analyzer

![Python CI](https://github.com/esousa97/py-log-analyzer/actions/workflows/ci.yml/badge.svg)

A lightweight CLI tool to parse and analyze Nginx/Apache log files with high performance and parallel processing.

## Features

- **High Performance**: Uses Python generators to read files line-by-line, minimizing RAM usage.
- **Parallel Processing**: Automatically utilizes multiple CPU cores to process multiple log files simultaneously using `multiprocessing`.
- **Detailed Parsing**: Extracts IP, Timestamp, Method, URL, and Status Code.
- **Anomaly Detection**: Identifies suspicious IP activity (brute force/scrapers) and monitors service health.
- **Report Export**: Export results to structured **JSON** or interactive **HTML** dashboards with Chart.js.
- **Docker Ready**: Run as an isolated utility without local Python installation.

## Requirements

- Python 3.x
- `rich` library

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/esousa97/py-log-analyzer.git
   cd py-log-analyzer
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # .\venv\Scripts\activate # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Installation

Build the image locally:
```bash
docker build -t py-log-analyzer .
```

## Usage

### Local Usage

Run the script providing one or more log files:

```bash
python py_log_analyzer.py access.log access.log.1 [options]
```

### Docker Usage

Mount your logs directory and run the container:

```bash
docker run --rm -v $(pwd):/logs py_log_analyzer /logs/access.log --format html
```

### Options

- `--threshold <float>`: 5xx error rate threshold for critical alert (default: `5.0`).
- `--format {json,html}`: Export the report to `report.json` or `report.html`.

## Output Example

The tool displays elegant tables in the terminal and generates interactive reports:

```text
Anomaly Detected: Suspicious IP Activity
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ IP Address  ┃ 401/404 Errors ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 10.10.10.10 │             52 │
└─────────────┴────────────────┘
```

## License

MIT License
