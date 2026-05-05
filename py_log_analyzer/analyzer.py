from collections import Counter

from .parser import log_generator


def process_file(file_path):
    """Worker function to process a single log file and return aggregated data."""
    ip_counts = Counter()
    url_counts = Counter()
    status_counts = Counter()
    suspicious_ips = Counter()  # For 401/404 errors
    total_count = 0

    for entry in log_generator(file_path):
        ip = entry["ip"]
        url = entry["url"]
        status = entry["status"]

        ip_counts[ip] += 1
        url_counts[url] += 1
        status_counts[status] += 1
        total_count += 1

        if status in ("401", "404"):
            suspicious_ips[ip] += 1

    return {
        "ip_counts": ip_counts,
        "url_counts": url_counts,
        "status_counts": status_counts,
        "suspicious_ips": suspicious_ips,
        "total_count": total_count,
    }


def get_status_categories(status_counts):
    """Categorize status codes into 2xx, 3xx, 4xx, 5xx."""
    categories = {
        "2xx (Success)": 0,
        "3xx (Redirection)": 0,
        "4xx (Client Error)": 0,
        "5xx (Server Error)": 0,
    }
    for status, count in status_counts.items():
        if status.startswith("2"):
            categories["2xx (Success)"] += count
        elif status.startswith("3"):
            categories["3xx (Redirection)"] += count
        elif status.startswith("4"):
            categories["4xx (Client Error)"] += count
        elif status.startswith("5"):
            categories["5xx (Server Error)"] += count
    return categories


def detect_anomalies(suspicious_ips, threshold=50):
    """Detect IPs with more than the threshold of 401/404 errors."""
    return {ip: count for ip, count in suspicious_ips.items() if count > threshold}
