import sys
import os
import argparse
from leafhopper.descriptors.vcpkg import VcpkgDescriptor
from leafhopper.descriptors.poetry import PoetryDescriptor
from leafhopper.descriptors.mvn import MvnDescriptor
from leafhopper.pkg_table_writer import PkgTableWriter
from leafhopper.logger import logger
from leafhopper.extra_pkgs import ExtraPkgs
from leafhopper.combined_license_renderer import CombinedLicenseRenderer
from distutils.util import strtobool
from leafhopper.descriptors.extra.extra_info_loader import load_extra_info_for_pkgs
from leafhopper.license_resolver import LicenseResolver

# import importlib.metadata
# package_metadada = importlib.metadata.metadata("leafhopper")
# # info from pyproject.toml's `version` and `description`
# LEAFHOPPER_VERSION = package_metadada.get("Version")
# LEAFHOOPER_SUMMARY = package_metadada.get("Summary")


def _leafhopper_parser():
    parser = argparse.ArgumentParser(prog="leafhopper")

    parser.add_argument(
        "file",
        nargs="+",
        help="specify the path to the project descriptor, vcpkg.json are supported",
    )

    parser.add_argument(
        "-f",
        "--format",
        default="markdown",
        help=f"specify the output format, {PkgTableWriter.supported_formats()} are supported",
    )

    parser.add_argument(
        "-o",
        "--output",
        help=f"specify a file for the output, default is stdout",
    )

    parser.add_argument(
        "-l",
        "--logging-level",
        help=f"specify the logging level, debug|info|warning|error|critical are supported. Default is `info`",
    )

    parser.add_argument(
        "-c",
        "--columns",
        help=f"""specify the output table header. A comma separated column names, 
built-in column names are 'name,version,homepage,license,description'. 
You can change the header to alter the column orders, 
and non built-in names specifed in the column will be shown as empty.
""",
    )

    parser.add_argument(
        "-e",
        "--extra",
        help=f"optional. specify a json file for extra pkgs to override the pkgs in the descriptor",
    )

    parser.add_argument(
        "-b",
        "--combine",
        action='store_true',
        help=f"optional. whether to generate a combined license. Specify the argument to toggle it. Default is false",
    )
    return parser


def parse_sys_args(sys_args):
    parser = _leafhopper_parser()
    args = parser.parse_args(sys_args)
    return vars(args)


def _validate_format(format):
    supported_formats = PkgTableWriter.supported_formats()
    if format not in supported_formats:
        raise ValueError(
            f"Given format {format} is not supported. supported_formats={supported_formats}"
        )


def _read_descriptor(file):
    with open(file, "r") as f:
        content = f.read()
        return content


def _get_descriptor(file):
    base_name = os.path.basename(file)
    descriptors = {
        "vcpkg.json": VcpkgDescriptor,
        "pyproject.toml": PoetryDescriptor,
        "pom.xml": MvnDescriptor,
    }
    if base_name in descriptors:
        return descriptors[base_name]
    else:
        raise ValueError(
            f"Unsupported descriptor {file}. Only vcpkg.json and pyproject.toml files are supported"
        )


def _write_pkg_table(pkg_infos, table_writer, output, columns):
    if output:
        if isinstance(output, str):
            with open(output, "w") as f:
                table_writer.write(pkg_infos, f, columns)
        else:  # StringIO
            table_writer.write(pkg_infos, output, columns)
    else:
        table_writer.write(pkg_infos, columns=columns)


def process_descriptors(
    files, format, output, columns=None, extra_pkgs_file=None, combined_license=False
):
    _validate_format(format)
    table_writer = PkgTableWriter(format)
    all_pkg_infos = []
    license_resolver = LicenseResolver()
    for file in files:
        descriptor = _get_descriptor(file)()
        # open file and read content
        descriptor_content = _read_descriptor(file)
        pkg_infos = descriptor.parse(descriptor_content)
        # override pkg_infos with provided overrides
        if extra_pkgs_file:
            logger.info(f"loading extra package information extra_file={extra_pkgs_file} current_pkgs={len(pkg_infos)}")
            extra_pkgs = ExtraPkgs(extra_pkgs_file)
            pkg_infos = extra_pkgs.override_pkg_infos(pkg_infos)
            logger.info(f"overrideed package information pkg_infos={len(pkg_infos)}")
        license_resolver.resolve(pkg_infos)
        load_extra_info_for_pkgs(pkg_infos, combined_license)
        all_pkg_infos.extend(pkg_infos)
        _write_pkg_table(pkg_infos, table_writer, output, columns)
    if combined_license:
        combined_license_renderer = CombinedLicenseRenderer()
        combined_licenses_txt = combined_license_renderer.render(all_pkg_infos)
        # write combined licenses to a file called `LICENSES.txt`
        open("LICENSES.txt", "w").write(combined_licenses_txt)


def _map_logging_level(level):
    levels = {
        "debug": 10,
        "info": 20,
        "warning": 30,
        "error": 40,
        "critical": 50,
    }
    return levels.get(level, 20)


def _set_logging_level(level):
    logger.setLevel(_map_logging_level(level))


def _get_columns(columns: list) -> list:
    # split columns by comma and trim each value
    if columns and columns.strip():
        columns = columns.split(",")
        columns = [col.strip() for col in columns]
    else:
        columns = None
    return columns


def main():
    args = parse_sys_args(sys.argv[1:])
    files = args["file"]
    format = args["format"]
    extra_pkgs_file = args["extra"]
    combined_license = args["combine"]
    columns = _get_columns(args["columns"])

    logging_level = args["logging_level"]
    _set_logging_level(logging_level)
    output = args.get("output", None)
    process_descriptors(
        files, format, output, columns, extra_pkgs_file, combined_license
    )


if __name__ == "__main__":
    main()
