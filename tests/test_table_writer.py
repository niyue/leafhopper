from leafhopper.pkg_table_writer import PkgTableWriter
import io

PKG_INFOS = [
    {"name": "librdkafka", "version": "1.0", "license": "MIT"},
    {
        "name": "arrow",
        "version": "8.0",
        "license": "Apache 2.0",
        "homepage": "http://arrow.apache.org/",
        "description": "memory format",
    },
]


def test_write_csv_table():
    output = io.StringIO()
    PkgTableWriter("csv").write(PKG_INFOS, output)
    csv = output.getvalue()
    assert '"name","description","version","homepage","license"' in csv
    assert "librdkafka" in csv
    assert "arrow" in csv
    assert "arrow.apache.org" in csv


def test_write_markdown_table():
    output = io.StringIO()
    PkgTableWriter("markdown").write(PKG_INFOS, output)
    md = output.getvalue()
    assert "librdkafka" in md
    assert "arrow" in md


def test_write_all_other_formats():
    for format in ["html", "json", "md", "latex"]:
        output = io.StringIO()
        PkgTableWriter(format).write(PKG_INFOS, output)
        table = output.getvalue()
        assert "librdkafka" in table
        assert "librdkafka" in table


def test_supported_formats():
    supported_formats = PkgTableWriter.supported_formats()
    assert set(supported_formats) == {"csv", "html", "json", "latex", "markdown", "md"}
