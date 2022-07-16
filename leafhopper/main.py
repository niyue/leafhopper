import sys
import os
import argparse
from leafhopper.descriptors.vcpkg import VcpkgDescriptor
from leafhopper.descriptors.poetry import PoetryDescriptor
from leafhopper.pkg_table_writer import PkgTableWriter
from leafhopper.logger import logger


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
    if base_name == "vcpkg.json":
        return VcpkgDescriptor
    elif base_name == "pyproject.toml":
        return PoetryDescriptor
    else:
        raise ValueError(f"Unsupported descriptor {file}. Only vcpkg.json and pyproject.toml files are supported")


def process_descriptors(files, format, output):
    _validate_format(format)
    table_writer = PkgTableWriter(format)
    for file in files:
        descriptor = _get_descriptor(file)()
        # open file and read content
        descriptor_content = _read_descriptor(file)
        pkg_infos = descriptor.parse(descriptor_content)
        if output:
            if isinstance(output, str):
                with open(output, "w") as f:
                    table_writer.write(pkg_infos, f)
            else:  # assume output is a file-like object
                table_writer.write(pkg_infos, output)
        else:
            table_writer.write(pkg_infos)


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


def main():
    args = parse_sys_args(sys.argv[1:])
    files = args["file"]
    format = args["format"]
    logging_level = args["logging_level"]
    _set_logging_level(logging_level)
    output = args.get("output", None)
    process_descriptors(files, format, output)


if __name__ == "__main__":
    main()
