from pytablewriter import (
    MarkdownTableWriter,
    HtmlTableWriter,
    CsvTableWriter,
    JsonTableWriter,
    LatexTableWriter,
)

WRITER_MAP = {
    "md": MarkdownTableWriter,
    "markdown": MarkdownTableWriter,
    "html": HtmlTableWriter,
    "csv": CsvTableWriter,
    "json": JsonTableWriter,
    "latex": LatexTableWriter,
}


class PkgTableWriter(object):
    def __init__(self, format: str):
        self.format = format
        if format not in WRITER_MAP:
            raise ValueError(f"{format} is not supported")

    def write(self, pkg_infos: list, output=None, columns=None):
        table_name = "Package Dependencies"
        pkg_attrs = ["name", "version", "homepage", "license", "description"]
        if columns:
            pkg_attrs = columns
        # retrieve package attributes from pkg_infos
        pkg_list = [self._get_attrs(pkg_info, pkg_attrs) for pkg_info in pkg_infos]
        writer = WRITER_MAP[self.format]()
        writer.table_name = table_name
        writer.headers = pkg_attrs
        writer.value_matrix = pkg_list
        if output:
            writer.stream = output

        writer.write_table()
        writer.write_null_line()

    def _get_attrs(self, pkg_info: dict, attrs: list):
        return [pkg_info.get(attr, "") for attr in attrs]

    @staticmethod
    def supported_formats():
        return list(WRITER_MAP.keys())
