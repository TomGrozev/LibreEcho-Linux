#!/usr/bin/env python3
"""Source contract tests for the Amazon Lidar sound-card node lifetimes."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "sound/soc/mediatek/mt8516/mt8516-amazon-lidar.c"


def body_of(source: str, signature: str, end: str) -> str:
    start = source.index(signature)
    stop = source.index(end, start)
    return source[start:stop]


class LidarCardNodeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = DRIVER.read_text()
        self.probe = body_of(self.source, "static int lidar_probe(", "\n}\n")

    def test_codec_references_are_released_after_parsing(self) -> None:
        """A devres put registered before the parse freed unallocated arrays."""
        self.assertNotIn("devm_add_action", self.probe.replace(
            "devm_add_action_or_reset(dev, lidar_put_node", ""),
            "a devres action must not manage the codec arrays")

        parses = [m.start() for m in
                  re.finditer(r"lidar_parse_codecs\s*\(\s*dev", self.probe)]
        self.assertTrue(parses, "probe no longer parses the codec links")

        releases = [m.start() for m in
                    re.finditer(r"clean_card_reference\s*\(", self.probe)]
        self.assertTrue(releases, "probe never releases the codec references")
        self.assertGreater(min(releases), parses[0],
                           "codec references released before the first parse")
        self.assertGreater(max(releases), parses[-1],
                           "the last parsed link is never released")

    def test_error_paths_release_the_codec_references(self) -> None:
        """The mic-link failure paths returned without releasing the nodes."""
        self.assertIn("err_put_codecs:", self.probe)
        cleanup = self.probe[self.probe.index("err_put_codecs:"):]
        self.assertIn("clean_card_reference(card)", cleanup)


if __name__ == "__main__":
    unittest.main()
