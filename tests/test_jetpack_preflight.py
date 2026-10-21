"""Basic read-only preflight contract tests; NOT Jetson hardware validation."""
import json
import subprocess
import sys
import unittest

from infra.jetson.preflight import _family, preflight


class JetPackPreflightTests(unittest.TestCase):
    def test_hardware_classification(self):
        self.assertEqual(_family("NVIDIA Jetson Nano Developer Kit"), "jetson_nano")
        self.assertEqual(_family("NVIDIA Jetson Orin Nano"), "jetson_other")
        self.assertEqual(_family("ordinary AMD PC"), "unidentified")

    def test_no_false_compatibility_claim(self):
        report = preflight()
        self.assertEqual(report["schema"], "jerp.jetpack.office_preflight.v1")
        self.assertFalse(report["compatible_verified"])
        self.assertFalse(report["installed_or_changed_anything"])
        self.assertIn("libreoffice", report["office"])
        self.assertIn("architecture", report)

    def test_machine_readable_cli(self):
        completed = subprocess.run(
            [sys.executable, "-m", "infra.jetson.preflight", "--json"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        report = json.loads(completed.stdout)
        self.assertFalse(report["compatible_verified"])
        self.assertFalse(report["installed_or_changed_anything"])


if __name__ == "__main__":
    unittest.main()
