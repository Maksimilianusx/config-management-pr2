"""Tests for dependency installation order."""

import unittest

from src.install_order import installation_order


class InstallationOrderTests(unittest.TestCase):
    """Check ordering and cyclic dependencies."""

    def test_chain(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        self.assertEqual(
            installation_order(graph, "A"), ["C", "B", "A"]
        )

    def test_diamond(self):
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        order = installation_order(graph, "A")
        self.assertEqual(len(order), 4)
        for name, deps in graph.items():
            for dep in deps:
                self.assertLess(order.index(dep), order.index(name))

    def test_cycle(self):
        graph = {"A": ["B"], "B": ["A"]}
        with self.assertRaises(ValueError):
            installation_order(graph, "A")

    def test_single_package(self):
        self.assertEqual(installation_order({"A": []}, "A"), ["A"])
