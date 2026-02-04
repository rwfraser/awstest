"""
Unit tests for application configuration.
"""
import os
import re
import unittest
from pathlib import Path


class GunicornConfigTests(unittest.TestCase):
    """Tests for Gunicorn application server configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.project_root = Path(__file__).resolve().parent.parent
        self.apprunner_yaml_path = (
            self.project_root / "django-apprunner" / "awstest" / "apprunner.yaml"
        )

    def test_gunicorn_binds_to_port_8000(self):
        """Test that the gunicorn application server binds to port 8000 as configured."""
        self.assertTrue(
            self.apprunner_yaml_path.exists(),
            f"apprunner.yaml not found at {self.apprunner_yaml_path}",
        )

        content = self.apprunner_yaml_path.read_text()

        # Check that gunicorn command binds to port 8000
        # Pattern matches: --bind <anything>:8000
        bind_pattern = r"gunicorn.*--bind\s+\S+:8000"
        self.assertRegex(
            content,
            bind_pattern,
            "Gunicorn should be configured to bind to port 8000",
        )

        # Check that network port is configured as 8000
        port_pattern = r"port:\s*8000"
        self.assertRegex(
            content,
            port_pattern,
            "Network port should be configured as 8000 in apprunner.yaml",
        )


if __name__ == "__main__":
    unittest.main()
