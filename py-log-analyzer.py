import argparse
import re
import sys
from collections import Counter
from rich.console import Console
from rich.table import Table

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

def display_summary(logs):
    console = Console()
    
    # Aggregate data
    ip_counts = Counter(log['ip'] for log in logs)
    url_counts = Counter(log['url'] for log in logs)
    
    status_categories = {
        "2xx (Success)": 0,
        "3xx (Redirection)": 0,
        "4xx (Client Error)": 0,
        "5xx (Server Error)": 0
    }
    
    for log in logs:
        status = log['status']
        if status.startswith('2'):
            status_categories["2xx (Success)"] += 1
        elif status.startswith('3'):
            status_categories["3xx (Redirection)"] += 1
        elif status.startswith('4'):
            status_categories["4xx (Client Error)"] += 1
        elif status.startswith('5'):
            status_categories["5xx (Server Error)"] += 1

    # Top 10 IPs Table
    ip_table = Table(title="Top 10 IP Addresses")
    ip_table.add_column("IP Address", style="cyan")
    ip_table.add_column("Requests", justify="right", style="magenta")
    for ip, count in ip_counts.most_common(10):
        ip_table.add_row(ip, str(count))
    
    # Status Categories Table
    status_table = Table(title="Requests by Status Code")
    status_table.add_column("Category", style="green")
    status_table.add_column("Count", justify="right", style="yellow")
    for cat, count in status_categories.items():
        status_table.add_row(cat, str(count))
        
    # Top 5 Paths Table
    url_table = Table(title="Top 5 Accessed Paths")
    url_table.add_column("Path", style="blue")
    url_table.add_column("Requests", justify="right", style="magenta")
    for url, count in url_counts.most_common(5):
        url_table.add_row(url, str(count))

    console.print(ip_table)
    console.print(status_table)
    console.print(url_table)
    console.print(f"\n[bold green]Total requests processed: {len(logs)}[/bold green]")

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
                    # Only show warning if line is not empty
                    if line.strip():
                        print(f"Warning: Could not parse line: {line.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    if logs:
        display_summary(logs)
    else:
        print("No valid log entries found.")

if __name__ == "__main__":
    main()
