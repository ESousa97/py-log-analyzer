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
python py-log-analyzer.py <path_to_log_file> [--threshold <percentage>]
```

### Options

- `--threshold`: (Optional) 5xx error rate threshold to trigger a "Critical Health" alert. Default is `5.0`.

### Example

```bash
python py-log-analyzer.py access.log --threshold 2.5
```

## Output Example

The tool displays elegant tables and alerts in the terminal:

```text
Anomaly Detected: Suspicious IP Activity
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ IP Address  ┃ 401/404 Errors ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 10.10.10.10 │             52 │
└─────────────┴────────────────┘

╭─────────────────────────────────────────╮
│  CRITICAL SERVICE HEALTH                │
│ 5xx Error Rate: 6.25% (Threshold: 5.0%) │
╰─────────────────────────────────────────╯

       Top 10 IP Addresses
┏━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ IP Address  ┃ Requests ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 127.0.0.1   │       15 │
└─────────────┴──────────┘
```

## License

This project is open-source and available under the MIT License.
