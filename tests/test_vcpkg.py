from leafhopper.descriptors.vcpkg import VcpkgDescriptor


def test_load_vcpkg_package():
    vcpkg_desp = VcpkgDescriptor()
    vcpkg_json = open("tests/data/vcpkg.json").read()
    pkg_infos = vcpkg_desp.parse(vcpkg_json)
    assert len(pkg_infos) == 4
    names = {pkg_info["name"] for pkg_info in pkg_infos}
    for pkg in ["librdkafka", "arrow", "ip2region", "zstd"]:
        assert pkg in names
    assert "homepage" in pkg_infos[1]
