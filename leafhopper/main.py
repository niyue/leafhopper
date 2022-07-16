import sys
import argparse
from distutils.util import strtobool
import importlib.metadata
from leafhopper.descriptors.vcpkg import VcpkgDescriptor
from leafhopper.pkg_table_writer import PkgTableWriter


package_metadada = importlib.metadata.metadata("leafhopper")
# info from pyproject.toml's `version` and `description`
LEAFHOPPER_VERSION = package_metadada.get("Version")
LEAFHOOPER_SUMMARY = package_metadada.get("Summary")


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
        help=f"specify the output format, {PkgTableWriter.supported_formats()} are supported",
    )

    parser.add_argument(
        "-o",
        "--output",
        help=f"specify a file for the output, default is stdout",
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


def process_descriptors(files, format, output):
    _validate_format(format)
    table_writer = PkgTableWriter(format)
    for file in files:
        descriptor = VcpkgDescriptor()
        # open file and read content
        descriptor_content = _read_descriptor(file)
        pkg_infos = descriptor.parse(descriptor_content)
        if output:
            if isinstance(output, str):
                with open(output, "w") as f:
                    table_writer.write(pkg_infos, f)
            else: # assume output is a file-like object
                table_writer.write(pkg_infos, output)
        else:
            table_writer.write(pkg_infos)


def main():
    args = parse_sys_args(sys.argv[1:])
    files = args["file"]
    format = args["format"]
    output = args.get("output", None)
    process_descriptors(files, format, output)


if __name__ == "__main__":
    main()
