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
    assert_dict_equal(args, {"file": ["vcpkg.json"], "format": "json", "output": None})


def test_vcpkg_json_with_invalid_format():
    args = parse_sys_args(["vcpkg.json", "--format", "no_such_format"])
    assert_dict_equal(
        args, {"file": ["vcpkg.json"], "format": "no_such_format", "output": None}
    )
