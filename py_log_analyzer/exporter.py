import json


def export_json(report_data, output_file):
    """Export analysis results to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(report_data, f, indent=4)


def export_html(report_data, output_file):
    """Export analysis results to a styled HTML report with Chart.js."""
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
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
