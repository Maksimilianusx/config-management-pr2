"""Tests for Mermaid graph visualization."""

import unittest

from src.visualize import to_mermaid


class MermaidTests(unittest.TestCase):
    """Check rendering for different dependency graphs."""

    def test_single_package(self):
        diagram = to_mermaid({"A": []})
        self.assertIn('n0["A"]', diagram)
        self.assertNotIn("-->", diagram)

    def test_dependency_chain(self):
        diagram = to_mermaid({
            "A": ["B"],
            "B": ["C"],
            "C": [],
        })
        self.assertIn("n0 --> n1", diagram)
        self.assertIn("n1 --> n2", diagram)

    def test_cyclic_dependencies(self):
        diagram = to_mermaid({
            "A": ["B"],
            "B": ["A"],
        })
        self.assertIn("n0 --> n1", diagram)
        self.assertIn("n1 --> n0", diagram)

    def test_shared_dependency(self):
        diagram = to_mermaid({
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        })
        self.assertIn("n1 --> n3", diagram)
        self.assertIn("n2 --> n3", diagram)
