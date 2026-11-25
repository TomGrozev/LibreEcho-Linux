#!/usr/bin/env python3
"""Source contract test for the LibreEcho IIO light-sensor Kconfig hookup."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
IIO_KCONFIG = ROOT / "drivers/iio/light/Kconfig"
SOURCE = r'source\s+"drivers/iio/light/libreecho/Kconfig"'


class IioKconfigContractTests(unittest.TestCase):
    def test_iio_light_kconfig_sources_libreecho_exactly_once(self) -> None:
        """A second source line redefined every light-sensor symbol."""
        kconfig = IIO_KCONFIG.read_text()
        self.assertEqual(len(re.findall(SOURCE, kconfig)), 1,
                         "drivers/iio/light/libreecho/Kconfig is not sourced once")


if __name__ == "__main__":
    unittest.main()
