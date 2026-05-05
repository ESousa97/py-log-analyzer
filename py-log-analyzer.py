import argparse
import re
import sys
import json
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def parse_log_line(line):
    # Common Log Format (CLF) regex
    regex = r'(?P<ip>\S+) .*?\[(?P<timestamp>.*?)\] "(?P<method>\S+)\s+(?P<url>\S+)\s+.*?"\s+(?P<status>\d{3})'
    match = re.search(regex, line)
    if match:
        return match.groupdict()
    return None

def detect_anomalies(logs):
    suspicious_ips = Counter()
    for log in logs:
        if log['status'] in ('401', '404'):
            suspicious_ips[log['ip']] += 1
    return {ip: count for ip, count in suspicious_ips.items() if count > 50}

def get_summary_data(logs):
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
            
    return ip_counts, url_counts, status_categories

def export_json(report_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(report_data, f, indent=4)

def export_html(report_data, output_file):
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Log Analysis Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f4f7f6; }}
            .container {{ max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #333; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
            .card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
            th {{ background-color: #f8f8f8; }}
            .alert {{ background-color: #ffebee; border-left: 5px solid #f44336; padding: 10px; margin-bottom: 20px; color: #c62828; }}
            .health-panel {{ background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; margin-bottom: 20px; }}
            .health-critical {{ background-color: #ffebee; border-left: 5px solid #f44336; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Log Analysis Report</h1>
            
            <div class="health-panel {'health-critical' if report_data['is_critical'] else ''}">
                <strong>Service Health:</strong> { 'CRITICAL' if report_data['is_critical'] else 'HEALTHY' }<br>
                Total Requests: {report_data['total_requests']}<br>
                Global Error Rate: {report_data['error_rate']:.2f}%<br>
                5xx Rate: {report_data['rate_5xx']:.2f}% (Threshold: {report_data['threshold']}%)
            </div>

            {f'<div class="alert"><strong>Anomalies Detected:</strong> Suspicious activity from {len(report_data["anomalies"])} IP(s).</div>' if report_data['anomalies'] else ''}

            <div class="grid">
                <div class="card">
                    <h2>Requests by Status</h2>
                    <canvas id="statusChart"></canvas>
                </div>
                <div class="card">
                    <h2>Top 5 Paths</h2>
                    <table>
                        <thead><tr><th>Path</th><th>Requests</th></tr></thead>
                        <tbody>
                            {''.join([f"<tr><td>{p}</td><td>{c}</td></tr>" for p, c in report_data['top_paths']])}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="grid">
                <div class="card" style="grid-column: span 2;">
                    <h2>Top 10 IP Addresses</h2>
                    <table>
                        <thead><tr><th>IP Address</th><th>Requests</th></tr></thead>
                        <tbody>
                            {''.join([f"<tr><td>{ip}</td><td>{c}</td></tr>" for ip, c in report_data['top_ips']])}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('statusChart').getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: {list(report_data['status_distribution'].keys())},
                    datasets: [{{
                        data: {list(report_data['status_distribution'].values())},
                        backgroundColor: ['#4caf50', '#2196f3', '#ff9800', '#f44336']
                    }}]
                }}
            }});
        </script>
    </body>
    </html>
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

def display_summary(logs, error_threshold_5xx, export_format=None):
    console = Console()
    total_logs = len(logs)
    
    ip_counts, url_counts, status_categories = get_summary_data(logs)
    anomalies = detect_anomalies(logs)

    total_errors = status_categories["4xx (Client Error)"] + status_categories["5xx (Server Error)"]
    error_rate = (total_errors / total_logs) * 100
    rate_5xx = (status_categories["5xx (Server Error)"] / total_logs) * 100
    is_critical = rate_5xx >= error_threshold_5xx

    # Prepare report data
    report_data = {
        "total_requests": total_logs,
        "error_rate": error_rate,
        "rate_5xx": rate_5xx,
        "threshold": error_threshold_5xx,
        "is_critical": is_critical,
        "status_distribution": status_categories,
        "top_ips": ip_counts.most_common(10),
        "top_paths": url_counts.most_common(5),
        "anomalies": anomalies
    }

    # Handle Exports
    if export_format == 'json':
        export_json(report_data, 'report.json')
        console.print("[bold green]Report exported to report.json[/bold green]")
    elif export_format == 'html':
        export_html(report_data, 'report.html')
        console.print("[bold green]Report exported to report.html[/bold green]")

    # Terminal Output
    if anomalies:
        table = Table(title="[bold red]Anomaly Detected: Suspicious IP Activity[/bold red]", border_style="red")
        table.add_column("IP Address", style="bright_red")
        table.add_column("401/404 Errors", justify="right")
        for ip, count in anomalies.items():
            table.add_row(ip, str(count))
        console.print(table)
    else:
        console.print("[bold green]No IP anomalies detected (threshold > 50 errors).[/bold green]")

    if is_critical:
        console.print(Panel(f"[bold white on red] CRITICAL SERVICE HEALTH [/bold white on red]\n5xx Error Rate: {rate_5xx:.2f}% (Threshold: {error_threshold_5xx}%)", expand=False))
    
    ip_table = Table(title="Top 10 IP Addresses")
    ip_table.add_column("IP Address", style="cyan")
    ip_table.add_column("Requests", justify="right", style="magenta")
    for ip, count in ip_counts.most_common(10):
        ip_table.add_row(ip, str(count))
    
    status_table = Table(title="Requests by Status Code")
    status_table.add_column("Category", style="green")
    status_table.add_column("Count", justify="right", style="yellow")
    for cat, count in status_categories.items():
        status_table.add_row(cat, str(count))
        
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
    parser.add_argument("--format", choices=['json', 'html'], help="Export format for the analysis report")
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
        display_summary(logs, args.threshold, args.format)
    else:
        print("No valid log entries found.")

if __name__ == "__main__":
    main()
