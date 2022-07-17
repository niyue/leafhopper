from leafhopper.main import process_descriptors, _get_columns
import io


def test_get_columns():
    columns = _get_columns("name, version")
    assert columns == ["name", "version"]


def test_get_none_columns():
    columns = _get_columns(None)
    assert columns is None


def test_get_empty_columns():
    columns = _get_columns("")
    assert columns == None


def test_get_whitespace_columns():
    columns = _get_columns("   ")
    assert columns == None


def test_get_tab_separated_columns():
    columns = _get_columns(" \t")
    assert columns == None


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


def test_process_maven_pom():
    output = io.StringIO()
    process_descriptors(["tests/data/pom.xml"], "json", output)
    table = output.getvalue()
    assert "findbugs" in table
