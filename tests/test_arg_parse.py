from leafhopper.main import parse_sys_args
from unittest import TestCase


def assert_dict_equal(d1, d2):
    TestCase().assertDictEqual(d1, d2)


def _invalid_args(func):
    try:
        func()
        assert False
    except SystemExit:
        pass


def test_empty_args():
    _invalid_args(lambda: parse_sys_args([]))


def test_vcpkg_json_with_json_format():
    args = parse_sys_args(["vcpkg.json", "--format", "json"])
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": None,
            "columns": None,
            "extra": None,
            "combine": False,
        },
    )


def test_vcpkg_json_with_invalid_format():
    args = parse_sys_args(["vcpkg.json", "--format", "no_such_format"])
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "no_such_format",
            "output": None,
            "logging_level": None,
            "columns": None,
            "extra": None,
            "combine": False,
        },
    )


def test_logging_level():
    args = parse_sys_args(
        ["vcpkg.json", "--format", "json", "--logging-level", "debug"]
    )
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": "debug",
            "columns": None,
            "extra": None,
            "combine": False,
        },
    )

def test_custom_header():
    args = parse_sys_args(
        ["vcpkg.json", "--format", "json", "--columns", "name,version"]
    )
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": None,
            "columns": "name,version",
            "extra": None,
            "combine": False,
        },
    )

def test_extra():
    args = parse_sys_args(
        ["vcpkg.json", "--format", "json", "--extra", "extra.json"]
    )
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": None,
            "columns": None,
            "extra": "extra.json",
            "combine": False,
        },
    )

def test_combine_license():
    args = parse_sys_args(
        ["vcpkg.json", "--format", "json", "--combine"]
    )
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": None,
            "columns": None,
            "extra": None,
            "combine": True,
        },
    )

def test_default_combine_license_is_false():
    args = parse_sys_args(
        ["vcpkg.json", "--format", "json"]
    )
    assert_dict_equal(
        args,
        {
            "file": ["vcpkg.json"],
            "format": "json",
            "output": None,
            "logging_level": None,
            "columns": None,
            "extra": None,
            "combine": False,
        },
    )