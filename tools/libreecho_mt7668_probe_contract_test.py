#!/usr/bin/env python3
"""Source contract test for the MT7668 late probe-failure cleanup."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
GL_INIT = ROOT / "drivers/net/wireless/mediatek/mt7668/os/linux/gl_init.c"
PROBE = "INT_32 wlanProbe(PVOID pvData, PVOID pvDriverData)"


def body_of(source: str, signature: str, end: str) -> str:
    start = source.index(signature)
    stop = source.index(end, start)
    return source[start:stop]


def strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    return re.sub(r"(?m)//.*$", "", source)


def function_bodies(source: str) -> dict[str, str]:
    source = strip_comments(source)
    bodies = {}
    pattern = (r"(?m)^(?:static\s+)?[A-Za-z_][A-Za-z0-9_ \t\*]*?"
               r"\b([A-Za-z_]\w*)\s*\([^;{]*\)\s*\{")
    for match in re.finditer(pattern, source):
        start = match.end() - 1
        depth = 0
        index = start
        while index < len(source):
            if source[index] == "{":
                depth += 1
            elif source[index] == "}":
                depth -= 1
                if depth == 0:
                    break
            index += 1
        bodies[match.group(1)] = source[start:index + 1]
    return bodies


class Mt7668ProbeContractTests(unittest.TestCase):
    def test_probe_failure_stops_the_adapter_before_net_destroy(self) -> None:
        """Freeing the adapter while the firmware still ran caused a use-after-free."""
        source = GL_INIT.read_text()
        probe = strip_comments(body_of(source, PROBE, "end of wlanProbe()"))
        window = probe[:probe.index("wlanNetDestroy(prWdev)")]
        bodies = function_bodies(source)
        probe_name = PROBE.split("(")[0].split()[-1]
        stopped = "wlanAdapterStop" in window or any(
            "wlanAdapterStop" in bodies.get(name, "")
            for name in re.findall(r"\b(\w+)\s*\(", window)
            if name != probe_name)
        self.assertTrue(stopped,
                        "probe failure destroys the netdev before wlanAdapterStop")


if __name__ == "__main__":
    unittest.main()
