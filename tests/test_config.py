"""Tests for YAML configuration validation."""

import unittest

from src.main import validate_config


class ConfigTests(unittest.TestCase):
    """Check valid and invalid configuration values."""

    def setUp(self):
        """Create a valid configuration before each test."""
        self.config = {
            "package": "A",
            "repository": "tests/repository.txt",
            "test_mode": True,
            "version": "1.0",
            "max_depth": 3,
        }

    def test_valid_config(self):
        """Accept a correct configuration."""
        self.assertEqual(validate_config(self.config), self.config)

    def test_empty_package(self):
        """Reject an empty package name."""
        self.config["package"] = ""
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_missing_repository(self):
        """Reject a nonexistent repository file."""
        self.config["repository"] = "missing.txt"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_test_mode(self):
        """Reject a non-boolean test mode."""
        self.config["test_mode"] = "true"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_empty_version(self):
        """Reject an empty package version."""
        self.config["version"] = ""
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_negative_depth(self):
        """Reject negative dependency depth."""
        self.config["max_depth"] = -1
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_url(self):
        """Reject an invalid URL in normal mode."""
        self.config["test_mode"] = False
        self.config["repository"] = "invalid-url"
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_missing_parameter(self):
        """Reject a missing required parameter."""
        del self.config["version"]
        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_unknown_parameter(self):
        """Reject an unsupported parameter."""
        self.config["unknown"] = 123
        with self.assertRaises(ValueError):
            validate_config(self.config)


if __name__ == "__main__":
    unittest.main()
