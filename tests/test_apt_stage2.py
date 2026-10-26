"""Additional tests for Ubuntu APT repository handling."""

import gzip
import io
import unittest
from unittest.mock import patch

from src.apt_repository import (
    download_index,
    find_package,
    get_direct_dependencies,
)


class AptStage2Tests(unittest.TestCase):
    """Check package versions and repository data."""

    def test_exact_version(self):
        """Select the requested package version."""
        index = (
            "Package: demo\nVersion: 1.0\n"
            "Depends: old-lib\n\n"
            "Package: demo\nVersion: 2.0\n"
            "Depends: new-lib\n"
        )
        record = find_package(index, "demo", "2.0")
        self.assertEqual(
            get_direct_dependencies(record),
            ["new-lib"],
        )

    def test_complex_dependencies(self):
        """Preserve version constraints and alternatives."""
        record = {
            "Pre-Depends": "base-files (>= 1)",
            "Depends": "libc6 (>= 2.34), x | y",
        }
        self.assertEqual(
            get_direct_dependencies(record),
            ["base-files (>= 1)", "libc6 (>= 2.34)", "x | y"],
        )

    def test_download_index(self):
        """Decode a compressed repository index."""
        content = "Package: demo\nVersion: 1.0\n"
        compressed = gzip.compress(content.encode("utf-8"))

        with patch(
            "src.apt_repository.urlopen",
            return_value=io.BytesIO(compressed),
        ):
            result = download_index("https://example.com/Packages.gz")

        self.assertEqual(result, content)

    def test_invalid_gzip(self):
        """Reject an invalid compressed repository index."""
        with patch(
            "src.apt_repository.urlopen",
            return_value=io.BytesIO(b"invalid data"),
        ):
            with self.assertRaises(ValueError):
                download_index("https://example.com/Packages.gz")


if __name__ == "__main__":
    unittest.main()
