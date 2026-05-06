"""GeoIP lookup using MaxMind GeoLite2 (geoip2 + local Country MMDB file)."""

from __future__ import annotations

import ipaddress
from collections import Counter
from typing import TYPE_CHECKING

import geoip2.errors

if TYPE_CHECKING:
    from geoip2.database import Reader


def country_label(reader: Reader, ip: str) -> str:
    """Resolve IP to a country label; private/local ranges skip the database."""
    try:
        addr = ipaddress.ip_address(ip)
        if addr.is_private or addr.is_loopback or addr.is_link_local:
            return "Private / local"
    except ValueError:
        pass

    try:
        rec = reader.country(ip)
        if rec.country.name:
            return rec.country.name
        if rec.country.iso_code:
            return rec.country.iso_code
        return "Unknown"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"
    except (ValueError, OSError):
        return "Unknown"


def enrich_ip_geo(reader: Reader, ip_counts: Counter, anomalies: dict[str, int]):
    """
    Aggregate requests by country and attach country labels to top IPs and anomalies.
    Unique IPs are resolved once (cached per run).
    """
    cache: dict[str, str] = {}

    def label(ip: str) -> str:
        if ip not in cache:
            cache[ip] = country_label(reader, ip)
        return cache[ip]

    country_requests: Counter[str] = Counter()
    for ip, cnt in ip_counts.items():
        country_requests[label(ip)] += cnt

    top_ips = [{"ip": ip, "requests": cnt, "country": label(ip)} for ip, cnt in ip_counts.most_common(10)]

    anomalies_detail = sorted(
        ({"ip": ip, "errors": err, "country": label(ip)} for ip, err in anomalies.items()),
        key=lambda x: x["errors"],
        reverse=True,
    )

    return {
        "country_distribution": dict(country_requests.most_common()),
        "top_ips": top_ips,
        "anomalies_detail": anomalies_detail,
    }
