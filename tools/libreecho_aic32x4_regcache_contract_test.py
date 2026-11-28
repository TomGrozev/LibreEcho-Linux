#!/usr/bin/env python3
"""Source contract tests for the AIC32x4 regmap cache volatility."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CODEC = ROOT / "sound/soc/codecs/tlv320aic32x4.c"
CONFIG = "aic32x4_regmap_config"


def body_of(source: str, start: int, end: str) -> str:
    stop = source.index(end, start)
    return source[start:stop]


class Aic32x4RegcacheContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.codec = CODEC.read_text()
        self.config_start = self.codec.index(f"struct regmap_config {CONFIG}")
        self.config = body_of(self.codec, self.config_start,
                              f"EXPORT_SYMBOL({CONFIG})")
        match = re.search(r"\.volatile_reg\s*=\s*(\w+)", self.config)
        self.callback = match.group(1) if match else None

    def test_regmap_config_wires_a_volatile_reg_callback(self) -> None:
        """The maple cache served stale status reads, so every unmute timed out."""
        self.assertIn("REGCACHE_MAPLE", self.config)
        self.assertIsNotNone(self.callback,
                             "regmap cache has no volatile_reg callback")
        self.assertRegex(
            self.codec,
            r"static\s+bool\s+" + re.escape(self.callback) + r"\s*\(")

    def test_volatile_callback_covers_the_polled_gain_status(self) -> None:
        """Caching AIC32X4_GAIN_APPLIED broke the unmute wait-for-applied poll."""
        self.assertIsNotNone(self.callback)
        callback = body_of(self.codec,
                           self.codec.index(self.callback + "("), "\n}")
        self.assertIn("AIC32X4_GAIN_APPLIED", callback)


if __name__ == "__main__":
    unittest.main()
