import json
from pathlib import Path

def get_actual_log_stats():
    """Helper function to parse the log and get the real answers."""
    log_file = Path("/app/access.log")
    if not log_file.exists():
        return 0, 0, ""
   
    lines = log_file.read_text().strip().splitlines()
    total_requests = len(lines)
   
    ips = set()
    path_counts = {}
    for line in lines:
        parts = line.split()
        if len(parts) >= 7:
            ip = parts[0]
            req_path = parts[6]
            ips.add(ip)
            path_counts[req_path] = path_counts.get(req_path, 0) + 1
           
    top_path = max(path_counts, key=path_counts.get) if path_counts else ""
    return total_requests, len(ips), top_path

def test_total_requests():
    """1. The total number of requests."""
    expected_total, _, _ = get_actual_log_stats()
    report_text = Path("/app/report.json").read_text()
    assert str(expected_total) in report_text, f"Expected total requests ({expected_total}) not found in report"

def test_unique_ips():
    """2. The total number of unique client IPs."""
    _, expected_ips, _ = get_actual_log_stats()
    report_text = Path("/app/report.json").read_text()
    assert str(expected_ips) in report_text, f"Expected unique IPs ({expected_ips}) not found in report"

def test_top_path():
    """3. The most frequently requested path."""
    _, _, expected_path = get_actual_log_stats()
    report_text = Path("/app/report.json").read_text()
    assert expected_path in report_text, f"Expected top path ({expected_path}) not found in report"