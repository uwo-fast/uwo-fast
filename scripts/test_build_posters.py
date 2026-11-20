import unittest

import build_posters as p


SOURCE = p.ROOT / "posters" / "demo.md"


class ImageSlotTest(unittest.TestCase):
    def test_placeholder_is_reported(self):
        self.assertTrue(p.resolve_image({"placeholder": "A photo."}, "hero", SOURCE))

    def test_missing_named_image_fails(self):
        with self.assertRaises(p.BuildError):
            p.resolve_image({"image": "images/no-such-photo.jpg"}, "hero", SOURCE)

    def test_empty_slot_fails(self):
        with self.assertRaises(p.BuildError):
            p.resolve_image({}, "hero", SOURCE)


class ApprovedPosterTest(unittest.TestCase):
    def test_approved_poster_with_placeholder_fails(self):
        metadata = {
            "title": "Demo", "slug": "demo", "version": "1", "status": "approved",
            "review_owner": "PI", "eyebrow": "", "subtitle": "",
            "hero": {"placeholder": "A photo."}, "facts": [{"label": "L", "value": "V"}], "work": [],
            "looking_for": [], "apply": {"url": "https://example.org/"}, "supervisor": "",
        }
        original = p.parse_frontmatter
        p.parse_frontmatter = lambda path, required: (dict(metadata), "Body.\n")
        try:
            with self.assertRaises(p.BuildError):
                p.prepare(SOURCE, p.LOGO)
        finally:
            p.parse_frontmatter = original



class HeroLayoutTest(unittest.TestCase):
    def test_unknown_layout_fails(self):
        with self.assertRaises(p.BuildError):
            p.layout_panels("collage")

    def test_wrong_panel_count_fails(self):
        hero = {"layout": "diagonal", "panels": [{"placeholder": "A photo."}]}
        with self.assertRaises(p.BuildError):
            p.hero_panels(hero, SOURCE)

    def test_placeholder_panel_is_reported(self):
        hero = {"layout": "diagonal", "panels": [{"placeholder": "A."}, {"placeholder": "B."}]}
        panels, placeholder = p.hero_panels(hero, SOURCE)
        self.assertEqual(len(panels), 2)
        self.assertTrue(placeholder)

    def test_panels_stay_inside_the_hero(self):
        for layout in ("diagonal", "diagonal3", "mosaic"):
            for shape in p.layout_panels(layout):
                for x, y in shape["points"]:
                    self.assertTrue(0 <= x <= p.CONTENT_WIDTH_IN + 1e-9, (layout, x))
                    self.assertTrue(0 <= y <= p.HERO_HEIGHT_IN + 1e-9, (layout, y))

if __name__ == "__main__":
    unittest.main()
