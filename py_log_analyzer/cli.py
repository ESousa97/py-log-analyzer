import argparse
import multiprocessing
from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .analyzer import detect_anomalies, get_status_categories, process_file
from .exporter import export_html, export_json


def display_summary(merged_data, error_threshold_5xx, export_format=None):
    console = Console()
    total_requests = merged_data["total_count"]

    if total_requests == 0:
        console.print("[bold yellow]No valid log entries found to analyze.[/bold yellow]")
        return

    ip_counts = merged_data["ip_counts"]
    url_counts = merged_data["url_counts"]
    status_counts = merged_data["status_counts"]
    suspicious_ips = merged_data["suspicious_ips"]

    status_categories = get_status_categories(status_counts)
    anomalies = detect_anomalies(suspicious_ips)

    total_errors = status_categories["4xx (Client Error)"] + status_categories["5xx (Server Error)"]
    error_rate = (total_errors / total_requests) * 100
    rate_5xx = (status_categories["5xx (Server Error)"] / total_requests) * 100
    is_critical = rate_5xx >= error_threshold_5xx

    report_data = {
        "total_requests": total_requests,
        "error_rate": error_rate,
        "rate_5xx": rate_5xx,
        "threshold": error_threshold_5xx,
        "is_critical": is_critical,
        "status_distribution": status_categories,
        "top_ips": ip_counts.most_common(10),
        "top_paths": url_counts.most_common(5),
        "anomalies": anomalies,
    }

    if export_format == "json":
        export_json(report_data, "report.json")
        console.print("[bold green]Report exported to report.json[/bold green]")
    elif export_format == "html":
        export_html(report_data, "report.html")
        console.print("[bold green]Report exported to report.html[/bold green]")

    if anomalies:
        table = Table(
            title="[bold red]Anomaly Detected: Suspicious IP Activity[/bold red]",
            border_style="red",
        )
        table.add_column("IP Address", style="bright_red")
        table.add_column("401/404 Errors", justify="right")
        for ip, count in anomalies.items():
            table.add_row(ip, str(count))
        console.print(table)
    else:
        console.print("[bold green]No IP anomalies detected (threshold > 50 errors).[/bold green]")

    if is_critical:
        console.print(
            Panel(
                f"[bold white on red] CRITICAL SERVICE HEALTH [/bold white on red]\n5xx Error Rate: {rate_5xx:.2f}% (Threshold: {error_threshold_5xx}%)",
                expand=False,
            )
        )

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

    console.print(f"\n[bold green]Total requests processed: {total_requests}[/bold green]")
    console.print(f"[bold]Total Error Rate: {error_rate:.2f}%[/bold]")


def run():
    parser = argparse.ArgumentParser(description="Analyze Nginx/Apache log files with performance optimizations.")
    parser.add_argument("files", nargs="+", help="Path to one or more log files")
    parser.add_argument(
        "--threshold",
        type=float,
        default=5.0,
        help="5xx error threshold for critical health alert (default: 5.0%%)",
    )
    parser.add_argument("--format", choices=["json", "html"], help="Export format for the analysis report")
    args = parser.parse_args()

    # Process files in parallel
    with multiprocessing.Pool() as pool:
        results = pool.map(process_file, args.files)

    # Merge results from all files
    merged_data = {
        "ip_counts": Counter(),
        "url_counts": Counter(),
        "status_counts": Counter(),
        "suspicious_ips": Counter(),
        "total_count": 0,
    }

    for res in results:
        merged_data["ip_counts"].update(res["ip_counts"])
        merged_data["url_counts"].update(res["url_counts"])
        merged_data["status_counts"].update(res["status_counts"])
        merged_data["suspicious_ips"].update(res["suspicious_ips"])
        merged_data["total_count"] += res["total_count"]

    display_summary(merged_data, args.threshold, args.format)
