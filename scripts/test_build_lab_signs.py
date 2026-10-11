import unittest

import build_lab_signs as b


BODY = """# Demo

See [Sink](sink.md) first.

## Related

- See [Waste Disposal](waste-disposal.md).

## Sources / Procedure Links

- Source A: <https://a.example/>
- Source B: <https://b.example/>
"""


class LinkGuardTest(unittest.TestCase):
    def test_every_link_becomes_a_code(self):
        body, links = b.replace_links_with_qr("demo", BODY)
        b.check_no_links_lost(BODY, body, links, b.ROOT / "demo.md")
        self.assertEqual(
            {url for _, url in links},
            {
                "https://a.example/",
                "https://b.example/",
                b.sign_url("sink"),
                b.sign_url("waste-disposal"),
            },
        )

    def test_guard_fails_when_one_link_is_dropped(self):
        body, links = b.replace_links_with_qr("demo", BODY)
        with self.assertRaises(b.BuildError):
            b.check_no_links_lost(BODY, body, links[:-1], b.ROOT / "demo.md")


class MissingGlyphTest(unittest.TestCase):
    STDERR = (
        "[WARNING] Missing character: There is no ⚠ (U+26A0) (U+26A0) "
        "in font [lmroman10-regular]:+tlig;!\n"
    )

    def test_missing_glyph_fails(self):
        with self.assertRaises(b.BuildError):
            b.check_missing_glyphs(self.STDERR, b.ROOT / "demo.md")

    def test_other_warnings_pass(self):
        b.check_missing_glyphs("[WARNING] Could not fetch resource\n", b.ROOT / "demo.md")


if __name__ == "__main__":
    unittest.main()
