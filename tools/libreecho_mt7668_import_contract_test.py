#!/usr/bin/env python3
"""Source contract tests for the MT7668 gen4 SDIO WLAN import."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MT7668 = ROOT / "drivers/net/wireless/mediatek/mt7668"


def source_files():
    return [path for path in MT7668.rglob("*") if path.suffix in (".c", ".h")]


class Mt7668ImportContractTests(unittest.TestCase):
    def test_no_duplicate_is_world_regdom_definition(self) -> None:
        """A second is_world_regdom clashes with net/wireless/reg.c at link time."""
        offenders = [str(path.relative_to(ROOT)) for path in source_files()
                     if "is_world_regdom" in path.read_text(errors="replace")]
        self.assertEqual(offenders, [])

    def test_every_imported_source_carries_an_spdx_tag(self) -> None:
        """Without SPDX lines checkpatch rejects every imported file."""
        offenders = [str(path.relative_to(ROOT)) for path in source_files()
                     if "SPDX-License-Identifier" not in
                     path.read_text(errors="replace")[:2048]]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
