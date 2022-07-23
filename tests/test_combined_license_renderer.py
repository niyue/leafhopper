from leafhopper.combined_license_renderer import CombinedLicenseRenderer


def test_render_combined_licenses():
    pkg_infos = [
        {
            "name": "com.google.code.findbugs.jsr305",
            "license": "Apache v2",
            "description": "this is findbugs",
        },
        {"name": "log4j", "license": "Apache v2"},
        {
            "name": "spdlog",
            "license_text": "The MIT License",
            "disclosed_source": "https://github.com/gabime/spdlog",
        },
    ]
    license_txt = CombinedLicenseRenderer().render(pkg_infos)
    assert "jsr305" in license_txt
    assert "LICENSE" in license_txt
    assert "Apache v2" in license_txt
    assert "The MIT License" in license_txt
    assert "Disclosed source" in license_txt
