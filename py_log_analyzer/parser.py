import re


def parse_log_line(line):
    """Common Log Format (CLF) regex parser."""
    regex = r'(?P<ip>\S+) .*?\[(?P<timestamp>.*?)\] "(?P<method>\S+)\s+(?P<url>\S+)\s+.*?"\s+(?P<status>\d{3})'
    match = re.search(regex, line)
    if match:
        return match.groupdict()
    return None


def log_generator(file_path):
    """Generator that yields parsed log entries line by line."""
    import sys

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    yield parsed
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
