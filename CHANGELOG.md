# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-04

### Added
- **Modular Structure**: Reorganized the project into a professional Python package (`py_log_analyzer`).
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing, linting (Ruff), security scanning (Bandit), and Docker builds.
- **Unit Tests**: Comprehensive test suite using `pytest`.
- **Performance Optimization**: Use of Python generators for memory-efficient log reading and `multiprocessing` for parallel file processing.
- **Docker Support**: Added `Dockerfile` to run the tool as an isolated container.
- **Report Export**: Support for exporting analysis results to JSON and interactive HTML dashboards with Chart.js.
- **Anomaly Detection**: Logic to identify suspicious IP activity (brute force/scrapers) based on 401/404 error counts.
- **Service Health Monitoring**: Configurable 5xx error rate thresholds with visual alerts.
- **Rich Terminal UI**: Elegant tables and panels using the `rich` library.
- **Aggregation Logic**: Top 10 IPs, Top 5 Paths, and Status Code distribution.

### Changed
- Refactored monolithic script into a modular architecture.
- Renamed project files to follow standard Python naming conventions.

## [0.1.0] - 2026-05-04

### Added
- Initial implementation of the log parser using Regular Expressions.
- Basic Command Line Interface (CLI) to process Nginx/Apache log files.
- Basic JSON output for parsed log entries.
