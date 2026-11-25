#!/usr/bin/env python3
"""Source contract tests for the Lidar board DTS dead-node removals."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DTS = ROOT / "arch/arm64/boot/dts/mediatek/libreecho-lidar.dts"


class LidarDtsNodeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dts = DTS.read_text()

    def test_duplicate_bl31_carve_out_is_not_reintroduced(self) -> None:
        """The board re-added a secmon window mt8516.dtsi already reserves."""
        self.assertNotIn("atf@43000000", self.dts)
        self.assertNotIn("/delete-node/ secmon@43000000", self.dts)

    def test_unused_core_regulator_is_not_reintroduced(self) -> None:
        """A fixed regulator with no consumer came back into the board file."""
        self.assertNotIn("regulator-core", self.dts)

    def test_pwrap_compatible_override_is_not_reintroduced(self) -> None:
        """No driver or binding matches mediatek,mt8167-pwrap."""
        self.assertNotIn("mediatek,mt8167-pwrap", self.dts)


if __name__ == "__main__":
    unittest.main()
