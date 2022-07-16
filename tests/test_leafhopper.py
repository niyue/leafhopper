from leafhopper.main import process_descriptors
import io


def test_process_vcpkg_json():
    output = io.StringIO()
    process_descriptors(["tests/data/vcpkg.json"], "json", output)
    table = output.getvalue()
    assert "librdkafka" in table


def test_process_pyproject():
    output = io.StringIO()
    process_descriptors(["tests/data/pyproject.toml"], "json", output)
    table = output.getvalue()
    assert "pyarrow" in table
