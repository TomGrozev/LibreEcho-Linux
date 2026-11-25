#!/usr/bin/env python3
"""Source contract tests for the MT8163 CONSYS misc build wiring."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MISC_MAKEFILE = ROOT / "drivers/misc/Makefile"


class ConsysBuildContractTests(unittest.TestCase):
    def test_misc_makefile_builds_the_mt8163_consys_subtree(self) -> None:
        """Dropping the CONSYS object line silently unbuilds Wi-Fi and Bluetooth."""
        makefile = MISC_MAKEFILE.read_text()
        self.assertRegex(
            makefile,
            r"(?m)^obj-\$\(CONFIG_MTK_MT8163_CONSYS\)\s*\+=\s*mediatek/\s*$")

    def test_consys_neighbours_amz_privacy_in_the_misc_makefile(self) -> None:
        """The privacy driver line once replaced, rather than joined, its neighbour."""
        makefile = MISC_MAKEFILE.read_text()
        self.assertRegex(
            makefile,
            r"(?m)^obj-\$\(CONFIG_AMZ_PRIVACY\)\s*\+=\s*amz_privacy\.o\s*$")


if __name__ == "__main__":
    unittest.main()
