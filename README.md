# Python Log Analyzer

A lightweight CLI tool to parse and analyze Nginx/Apache log files using Regular Expressions.

## Features

- Extracts key fields from log files:
  - Source IP Address
  - Timestamp (Date/Time)
  - HTTP Method (GET, POST, etc.)
  - Requested URL
  - HTTP Status Code
- Stores results in a structured list of dictionaries.
- Easy-to-use Command Line Interface (CLI).

## Requirements

- Python 3.x

## Installation

No external dependencies are required. Simply clone the repository and run the script.

```bash
git clone https://github.com/esousa97/py-log-analyzer.git
cd py-log-analyzer
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

## Output Format

The tool outputs a JSON-formatted list of parsed entries:

```json
[
    {
        "ip": "127.0.0.1",
        "timestamp": "10/Oct/2000:13:55:36 -0700",
        "method": "GET",
        "url": "/index.html",
        "status": "200"
    }
]
```

## License

This project is open-source and available under the MIT License.
