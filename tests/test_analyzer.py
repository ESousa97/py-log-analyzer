from collections import Counter

from py_log_analyzer.analyzer import detect_anomalies, get_status_categories
from py_log_analyzer.parser import parse_log_line


def test_parse_log_line_valid():
    line = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326'
    parsed = parse_log_line(line)
    assert parsed is not None
    assert parsed["ip"] == "127.0.0.1"
    assert parsed["method"] == "GET"
    assert parsed["url"] == "/index.html"
    assert parsed["status"] == "200"


def test_parse_log_line_invalid():
    line = "invalid log line"
    assert parse_log_line(line) is None


def test_get_status_categories():
    status_counts = Counter({"200": 10, "301": 5, "404": 3, "500": 2})
    categories = get_status_categories(status_counts)
    assert categories["2xx (Success)"] == 10
    assert categories["3xx (Redirection)"] == 5
    assert categories["4xx (Client Error)"] == 3
    assert categories["5xx (Server Error)"] == 2


def test_detect_anomalies_no_anomalies():
    suspicious_ips = Counter({"1.1.1.1": 50})
    anomalies = detect_anomalies(suspicious_ips)
    assert len(anomalies) == 0


def test_detect_anomalies_with_anomalies():
    suspicious_ips = Counter({"1.1.1.1": 51})
    anomalies = detect_anomalies(suspicious_ips)
    assert anomalies["1.1.1.1"] == 51
