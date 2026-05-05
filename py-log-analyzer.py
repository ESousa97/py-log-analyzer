import argparse
import re
import sys
import json

def parse_log_line(line):
    # Common Log Format (CLF) regex
    # Example: 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
    # Pattern explanation:
    # (?P<ip>\S+) -> IP address
    # .*?\[(?P<timestamp>.*?)\] -> Skip until [timestamp]
    # "(?P<method>\S+)\s+(?P<url>\S+)\s+.*?" -> "METHOD URL PROTOCOL"
    # \s+(?P<status>\d{3}) -> Status code
    
    regex = r'(?P<ip>\S+) .*?\[(?P<timestamp>.*?)\] "(?P<method>\S+)\s+(?P<url>\S+)\s+.*?"\s+(?P<status>\d{3})'
    match = re.search(regex, line)
    if match:
        return match.groupdict()
    return None

def main():
    parser = argparse.ArgumentParser(description="Analyze Nginx/Apache log files.")
    parser.add_argument("file", help="Path to the log file")
    args = parser.parse_args()

    logs = []
    try:
        with open(args.file, 'r') as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
                else:
                    print(f"Warning: Could not parse line: {line.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Simple output for verification
    print(json.dumps(logs, indent=4))
    print(f"\nTotal lines parsed: {len(logs)}")

if __name__ == "__main__":
    main()
