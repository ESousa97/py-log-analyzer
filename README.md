# Python Log Analyzer

A lightweight CLI tool to parse and analyze Nginx/Apache log files using Regular Expressions.

## Features

- **Detailed Parsing**: Extracts IP, Timestamp, Method, URL, and Status Code.
- **Aggregation Logic**:
  - **Top 10 IP Addresses**: Identifies the most frequent visitors.
  - **Status Code Distribution**: Summarizes requests by category (2xx, 3xx, 4xx, 5xx).
  - **Top 5 Accessed Paths**: Shows the most requested URLs.
- **Anomaly Detection**:
  - **Suspicious IP Activity**: Detects IPs with more than 50 errors (401/404).
  - **Error Rate Calculation**: Calculates the total error percentage.
  - **Service Health Alerts**: Displays a critical alert if 5xx errors exceed a configurable threshold.
- **Report Export**:
  - **JSON**: Export raw analysis data for further processing.
  - **HTML**: Generate a visually appealing, interactive report with charts (Chart.js) and tables.
- **Rich Terminal UI**: Displays summaries and alerts in elegant tables and panels using the `rich` library.

## Requirements

- Python 3.x
- `rich` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/esousa97/py-log-analyzer.git
   cd py-log-analyzer
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script by providing the path to your log file as an argument:

```bash
python py-log-analyzer.py <path_to_log_file> [options]
```

### Options

- `--threshold <float>`: 5xx error rate threshold for critical alert (default: `5.0`).
- `--format {json,html}`: Export the report to `report.json` or `report.html`.

### Examples

**Standard analysis:**
```bash
python py-log-analyzer.py access.log
```

**Exporting to HTML with custom threshold:**
```bash
python py-log-analyzer.py access.log --threshold 2.0 --format html
```

## Output Example (Terminal)

The tool displays elegant tables and alerts in the terminal:

```text
Anomaly Detected: Suspicious IP Activity
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ IP Address  ┃ 401/404 Errors ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 10.10.10.10 │             52 │
└─────────────┴────────────────┘

       Top 10 IP Addresses
┏━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ IP Address  ┃ Requests ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 127.0.0.1   │       15 │
└─────────────┴──────────┘
```

## License

This project is open-source and available under the MIT License.
