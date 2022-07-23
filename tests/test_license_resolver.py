from leafhopper.license_resolver import LicenseResolver

def test_resolve_license():
    resolver = LicenseResolver()
    pkg_info = {"name": "curl", "license_url": "https://raw.githubusercontent.com/curl/curl/master/COPYING"}
    resolver.resolve([pkg_info])
    assert "license_text" in pkg_info
    assert "Copyright" in pkg_info["license_text"]
