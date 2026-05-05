import argparse
import re
import sys
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def parse_log_line(line):
    # Common Log Format (CLF) regex
    # Example: 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
    
    regex = r'(?P<ip>\S+) .*?\[(?P<timestamp>.*?)\] "(?P<method>\S+)\s+(?P<url>\S+)\s+.*?"\s+(?P<status>\d{3})'
    match = re.search(regex, line)
    if match:
        return match.groupdict()
    return None

def detect_anomalies(logs, console):
    # Detect IPs with more than 50 401 or 404 errors
    suspicious_ips = Counter()
    for log in logs:
        if log['status'] in ('401', '404'):
            suspicious_ips[log['ip']] += 1
    
    anomalies = {ip: count for ip, count in suspicious_ips.items() if count > 50}
    
    if anomalies:
        table = Table(title="[bold red]Anomaly Detected: Suspicious IP Activity[/bold red]", border_style="red")
        table.add_column("IP Address", style="bright_red")
        table.add_column("401/404 Errors", justify="right")
        for ip, count in anomalies.items():
            table.add_row(ip, str(count))
        console.print(table)
    else:
        console.print("[bold green]No IP anomalies detected (threshold > 50 errors).[/bold green]")

def display_summary(logs, error_threshold_5xx):
    console = Console()
    total_logs = len(logs)
    
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

    # Anomaly Detection
    detect_anomalies(logs, console)

    # Health Check
    total_errors = status_categories["4xx (Client Error)"] + status_categories["5xx (Server Error)"]
    error_rate = (total_errors / total_logs) * 100
    rate_5xx = (status_categories["5xx (Server Error)"] / total_logs) * 100

    if rate_5xx >= error_threshold_5xx:
        console.print(Panel(f"[bold white on red] CRITICAL SERVICE HEALTH [/bold white on red]\n5xx Error Rate: {rate_5xx:.2f}% (Threshold: {error_threshold_5xx}%)", expand=False))
    
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
    
    console.print(f"\n[bold green]Total requests processed: {total_logs}[/bold green]")
    console.print(f"[bold]Total Error Rate: {error_rate:.2f}%[/bold]")

def main():
    parser = argparse.ArgumentParser(description="Analyze Nginx/Apache log files.")
    parser.add_argument("file", help="Path to the log file")
    parser.add_argument("--threshold", type=float, default=5.0, help="5xx error threshold for critical health alert (default: 5.0%%)")
    args = parser.parse_args()

    logs = []
    try:
        with open(args.file, 'r') as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
                else:
                    if line.strip():
                        print(f"Warning: Could not parse line: {line.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    if logs:
        display_summary(logs, args.threshold)
    else:
        print("No valid log entries found.")

if __name__ == "__main__":
    main()
