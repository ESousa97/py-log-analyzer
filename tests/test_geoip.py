from collections import Counter
from unittest.mock import MagicMock

import geoip2.errors

from py_log_analyzer.geoip import country_label, enrich_ip_geo


def test_country_label_private_ipv4_skips_reader():
    reader = MagicMock()
    assert country_label(reader, "10.0.0.1") == "Private / local"
    reader.country.assert_not_called()


def test_country_label_loopback_skips_reader():
    reader = MagicMock()
    assert country_label(reader, "127.0.0.1") == "Private / local"
    reader.country.assert_not_called()


def test_country_label_uses_country_name():
    reader = MagicMock()
    rec = MagicMock()
    rec.country.name = "Brazil"
    rec.country.iso_code = "BR"
    reader.country.return_value = rec
    assert country_label(reader, "200.160.2.3") == "Brazil"


def test_country_label_falls_back_to_iso_code():
    reader = MagicMock()
    rec = MagicMock()
    rec.country.name = None
    rec.country.iso_code = "DE"
    reader.country.return_value = rec
    assert country_label(reader, "5.6.7.8") == "DE"


def test_country_label_address_not_found():
    reader = MagicMock()
    reader.country.side_effect = geoip2.errors.AddressNotFoundError("not found")
    assert country_label(reader, "8.8.8.8") == "Unknown"


def test_enrich_ip_geo_aggregates_and_labels():
    reader = MagicMock()

    def fake_country(ip):
        r = MagicMock()
        if ip == "1.1.1.1":
            r.country.name = "Australia"
            r.country.iso_code = "AU"
        else:
            r.country.name = "Brazil"
            r.country.iso_code = "BR"
        return r

    reader.country.side_effect = fake_country

    ip_counts = Counter({"1.1.1.1": 10, "2.2.2.2": 5})
    anomalies = {"1.1.1.1": 60}
    out = enrich_ip_geo(reader, ip_counts, anomalies)

    assert out["country_distribution"]["Australia"] == 10
    assert out["country_distribution"]["Brazil"] == 5
    assert out["top_ips"][0]["country"] == "Australia"
    assert out["anomalies_detail"][0]["ip"] == "1.1.1.1"
    assert out["anomalies_detail"][0]["country"] == "Australia"
