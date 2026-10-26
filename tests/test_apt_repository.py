"""Tests for Ubuntu package metadata parsing."""

import unittest

from src.apt_repository import (
    find_package,
    get_direct_dependencies,
    parse_record,
)


class AptRepositoryTests(unittest.TestCase):
    """Test package metadata processing."""

    def test_parse_record(self):
        """Read the package name and version."""
        record = parse_record("Package: demo\nVersion: 1.0")
        self.assertEqual(record["Package"], "demo")
        self.assertEqual(record["Version"], "1.0")

    def test_find_package(self):
        """Find the requested package version."""
        index = "Package: demo\nVersion: 1.0\n"
        record = find_package(index, "demo", "1.0")
        self.assertEqual(record["Package"], "demo")

    def test_dependencies(self):
        """Extract direct package dependencies."""
        record = {"Depends": "libc6, zlib1g"}
        result = get_direct_dependencies(record)
        self.assertEqual(result, ["libc6", "zlib1g"])

    def test_missing_package(self):
        """Report a missing package version."""
        with self.assertRaises(ValueError):
            find_package("", "demo", "1.0")


if __name__ == "__main__":
    unittest.main()
