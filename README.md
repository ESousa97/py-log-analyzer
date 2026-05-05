# Python Log Analyzer

A lightweight CLI tool to parse and analyze Nginx/Apache log files using Regular Expressions.

## Features

- **Detailed Parsing**: Extracts IP, Timestamp, Method, URL, and Status Code.
- **Aggregation Logic**:
  - **Top 10 IP Addresses**: Identifies the most frequent visitors.
  - **Status Code Distribution**: Summarizes requests by category (2xx, 3xx, 4xx, 5xx).
  - **Top 5 Accessed Paths**: Shows the most requested URLs.
- **Rich Terminal UI**: Displays summaries in elegant tables using the `rich` library.

## Requirements

- Python 3.x
- `rich` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/esousa97/py-log-analyzer.git
   cd py-log-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install rich
   ```

## Usage

Run the script by providing the path to your log file as an argument:

```bash
python py-log-analyzer.py <path_to_log_file>
```

### Example

```bash
python py-log-analyzer.py access.log
```

## Output Example

The tool displays elegant tables in the terminal:

```text
       Top 10 IP Addresses
┏━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ IP Address  ┃ Requests ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 127.0.0.1   │       15 │
└─────────────┴──────────┘

   Requests by Status Code
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Category           ┃ Count ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ 2xx (Success)      │    20 │
└────────────────────┴───────┘
```

## License

This project is open-source and available under the MIT License.
