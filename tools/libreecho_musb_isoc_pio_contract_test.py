#!/usr/bin/env python3
"""Source contract tests for the MUSB isochronous PIO bypass."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
GADGET = ROOT / "drivers/usb/musb/musb_gadget.c"


def body_of(source: str, signature: str, end: str) -> str:
    start = source.index(signature)
    stop = source.index(end, start)
    return source[start:stop]


def strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    return re.sub(r"(?m)//.*$", "", source)


class MusbIsocPioContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = GADGET.read_text()
        self.txstate = strip_comments(
            body_of(self.source, "static void txstate(", "\n}\n"))

    def test_txstate_sizes_the_fifo_before_the_isoc_pio_bypass(self) -> None:
        """The bypass jumped over the fifo_count assignment, sending empty packets."""
        fifo = self.txstate.index("fifo_count = min(")
        self.assertLess(fifo, self.txstate.index("MUSB_G_ISOC_NO_DMA"))

    def test_isoc_no_dma_quirk_only_gates_the_dma_branch(self) -> None:
        """As a common-path goto the quirk skipped the PIO transmit path."""
        dma = self.txstate.index("is_buffer_mapped(req)")
        self.assertLess(dma, self.txstate.index("MUSB_G_ISOC_NO_DMA"))


if __name__ == "__main__":
    unittest.main()
