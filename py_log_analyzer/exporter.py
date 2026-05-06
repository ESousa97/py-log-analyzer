import json


def export_json(report_data, output_file):
    """Export analysis results to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)


def export_html(report_data, output_file):
    """Export analysis results to a styled HTML report with Chart.js."""
    geo_enabled = report_data.get("geo_enabled") and report_data.get("country_distribution")

    top_ips_header = (
        "<th>IP Address</th><th>Requests</th><th>Country</th>"
        if geo_enabled
        else "<th>IP Address</th><th>Requests</th>"
    )
    top_ips_rows = ""
    for row in report_data["top_ips"]:
        country_cell = f"<td>{row.get('country') or ''}</td>" if geo_enabled else ""
        top_ips_rows += f"<tr><td>{row['ip']}</td><td>{row['requests']}</td>{country_cell}</tr>"

    country_chart_block = ""
    if geo_enabled:
        cd = report_data["country_distribution"]
        labels = list(cd.keys())[:12]
        values = [cd[k] for k in labels]
        country_chart_block = """
            <div class="card">
                <h2>Traffic by Country</h2>
                <canvas id="countryChart"></canvas>
            </div>
        """
        country_script = f"""
            const countryCtx = document.getElementById('countryChart').getContext('2d');
            new Chart(countryCtx, {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(labels)},
                    datasets: [{{
                        label: 'Requests',
                        data: {json.dumps(values)},
                        backgroundColor: '#2196f3'
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        """
    else:
        country_script = ""

    grid_geo_class = "grid-geo" if geo_enabled else ""

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
            .grid-geo {{ grid-template-columns: 1fr 1fr; }}
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
            {"<p><strong>GeoIP:</strong> MaxMind GeoLite2 Country (traffic shown by country)</p>" if geo_enabled else ""}

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

            <div class="grid {grid_geo_class}">
                {country_chart_block if geo_enabled else ''}
                <div class="card" style="{'grid-column: span 2;' if not geo_enabled else ''}">
                    <h2>Top 10 IP Addresses</h2>
                    <table>
                        <thead><tr>{top_ips_header}</tr></thead>
                        <tbody>
                            {top_ips_rows}
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
            {country_script}
        </script>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
