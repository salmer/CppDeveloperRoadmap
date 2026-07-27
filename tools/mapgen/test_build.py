#!/usr/bin/env python3
"""
Unit tests for build.py's deterministic pieces — the DSL parser, text wrapping, coordinate
formatting, and the hint geometry/arrow math. These guard the class of regression mapcheck
CANNOT see: e.g. `arrow=` silently no longer parsed, a flipped sign in the angle math, or
broken side/stage inheritance. No Pillow and no draw.io needed (text metrics are injected),
so it runs anywhere in a fraction of a second.

    python tools/mapgen/test_build.py            # or: python -m unittest -v
"""
import math, os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build


def parse(dsl_text):
    """Run build.parse_dsl over an in-memory DSL string via a temp file."""
    with tempfile.NamedTemporaryFile("w", suffix=".dsl", delete=False, encoding="utf-8") as f:
        f.write(dsl_text)
        path = f.name
    try:
        return build.parse_dsl(path)
    finally:
        os.unlink(path)


DSL = """\
# a comment, ignored
spine center=root

[a] side=left grade=middle
  [a1] stage=2
    [a2]
[b] side=right grade=senior stage=1
[c]

frame [f] title=libs contains=a
hint [h1] angle=90 dist=50 arrow=top -> a1, a2
hint [h2] -> b
"""


class ParseDsl(unittest.TestCase):
    def setUp(self):
        self.nodes, self.order, self.hints, self.frames, self.spine = parse(DSL)

    def test_order_and_hierarchy(self):
        self.assertEqual(self.order, ["a", "a1", "a2", "b", "c"])
        self.assertEqual(self.nodes["a"]["children"], ["a1"])
        self.assertEqual(self.nodes["a1"]["children"], ["a2"])
        self.assertEqual(self.nodes["a1"]["parent"], "a")
        self.assertEqual(self.nodes["a2"]["parent"], "a1")
        self.assertIsNone(self.nodes["a"]["parent"])

    def test_depth_from_indentation(self):
        self.assertEqual(self.nodes["a"]["depth"], 0)
        self.assertEqual(self.nodes["a1"]["depth"], 1)
        self.assertEqual(self.nodes["a2"]["depth"], 2)

    def test_grade_default_and_explicit(self):
        self.assertEqual(self.nodes["a"]["grade"], "middle")
        self.assertEqual(self.nodes["b"]["grade"], "senior")
        self.assertEqual(self.nodes["a2"]["grade"], "junior")   # default

    def test_side_inheritance_and_default(self):
        self.assertEqual(self.nodes["a"]["side"], "left")
        self.assertEqual(self.nodes["a1"]["side"], "left")      # inherited
        self.assertEqual(self.nodes["a2"]["side"], "left")      # inherited two levels
        self.assertEqual(self.nodes["b"]["side"], "right")
        self.assertEqual(self.nodes["c"]["side"], "right")      # default when no parent

    def test_stage_inheritance(self):
        self.assertIsNone(self.nodes["a"]["stage"])
        self.assertEqual(self.nodes["a1"]["stage"], 2)
        self.assertEqual(self.nodes["a2"]["stage"], 2)          # inherited
        self.assertEqual(self.nodes["b"]["stage"], 1)

    def test_spine(self):
        self.assertEqual(self.spine["center"], "root")
        self.assertIsNone(self.spine["hubx"])
        self.assertIsNone(self.spine["gate"])

    def test_frame(self):
        self.assertEqual(len(self.frames), 1)
        self.assertEqual(self.frames[0]["id"], "f")
        self.assertEqual(self.frames[0]["titleKey"], "libs")
        self.assertEqual(self.frames[0]["contains"], ["a"])

    def test_hint_attributes(self):
        h1, h2 = self.hints
        self.assertEqual(h1["id"], "h1")
        self.assertEqual(h1["targets"], ["a1", "a2"])
        self.assertEqual(h1["angle"], 90.0)
        self.assertEqual(h1["dist"], 50.0)
        self.assertEqual(h1["arrow"], "top")

    def test_hint_optional_fields_default_none(self):
        _, h2 = self.hints
        self.assertEqual(h2["targets"], ["b"])
        self.assertIsNone(h2["angle"])
        self.assertIsNone(h2["dist"])
        self.assertIsNone(h2["arrow"])          # -> the required-arrow validation flags this

    def test_negative_angle_parses(self):
        _, _, hints, _, _ = parse("spine center=r\n[r]\nhint [h] angle=-15 dist=10 arrow=left -> r\n")
        self.assertEqual(hints[0]["angle"], -15.0)


class TreeHelpers(unittest.TestCase):
    def setUp(self):
        self.nodes = parse(DSL)[0]

    def test_descendants(self):
        self.assertEqual(build.descendants(self.nodes, "a"), ["a", "a1", "a2"])
        self.assertEqual(build.descendants(self.nodes, "a2"), ["a2"])

    def test_section_of_is_depth1_ancestor(self):
        self.assertEqual(build.section_of(self.nodes, "a2"), "a1")
        self.assertEqual(build.section_of(self.nodes, "a1"), "a1")
        self.assertEqual(build.section_of(self.nodes, "a"), "a")


class Num(unittest.TestCase):
    def test_integers_have_no_decimal(self):
        self.assertEqual(build.num(5), "5")
        self.assertEqual(build.num(5.0), "5")
        self.assertEqual(build.num(-12.0), "-12")
        self.assertEqual(build.num(0), "0")

    def test_fractions_trimmed(self):
        self.assertEqual(build.num(5.5), "5.5")
        self.assertEqual(build.num(5.25), "5.25")
        self.assertEqual(build.num(-3.5), "-3.5")
        self.assertEqual(build.num(15494.5), "15494.5")


class XmlEsc(unittest.TestCase):
    def test_escapes(self):
        self.assertEqual(build.xml_esc('a & b < c > "d"'), 'a &amp; b &lt; c &gt; &quot;d&quot;')

    def test_ampersand_first(self):   # must escape & before it can double-escape &lt;
        self.assertEqual(build.xml_esc("<&>"), "&lt;&amp;&gt;")


class IsCjk(unittest.TestCase):
    def test_ranges(self):
        self.assertTrue(build.is_cjk("中"))
        self.assertTrue(build.is_cjk("（"))     # fullwidth paren
        self.assertFalse(build.is_cjk("a"))
        self.assertFalse(build.is_cjk(" "))
        self.assertFalse(build.is_cjk("+"))


class Wrap(unittest.TestCase):
    measure = staticmethod(lambda s: len(s) * 10)      # 10px per character

    def test_latin_wraps_on_spaces(self):
        self.assertEqual(build.wrap("hello world", 100, self.measure), ["hello", "world"])

    def test_latin_keeps_words_whole(self):
        self.assertEqual(build.wrap("aa bb cc", 60, self.measure), ["aa bb", "cc"])

    def test_overlong_token_not_broken(self):
        self.assertEqual(build.wrap("hello", 20, self.measure), ["hello"])  # can't fit, stays whole

    def test_cjk_wraps_per_character(self):
        self.assertEqual(build.wrap("中文字", 20, self.measure), ["中文", "字"])


class FacingSide(unittest.TestCase):
    def test_dominant_axis(self):
        self.assertEqual(build.facing_side(100, 0), "right")
        self.assertEqual(build.facing_side(-100, 0), "left")
        self.assertEqual(build.facing_side(0, 100), "bottom")
        self.assertEqual(build.facing_side(0, -100), "top")

    def test_ties_go_horizontal(self):
        self.assertEqual(build.facing_side(50, 50), "right")
        self.assertEqual(build.facing_side(-50, 50), "left")

    def test_side_anchor_table(self):
        self.assertEqual(build.SIDE_ANCHOR["left"], (0, 0.5))
        self.assertEqual(build.SIDE_ANCHOR["right"], (1, 0.5))
        self.assertEqual(build.SIDE_ANCHOR["top"], (0.5, 0))
        self.assertEqual(build.SIDE_ANCHOR["bottom"], (0.5, 1))


class HintXy(unittest.TestCase):
    def test_right(self):
        x, cy = build.hint_xy(100, 200, 0, 50, 20)      # 0deg = +x
        self.assertAlmostEqual(x, 100 + 50 - 10)        # centre 150, minus half-width
        self.assertAlmostEqual(cy, 200)

    def test_up(self):
        x, cy = build.hint_xy(100, 200, 90, 50, 20)     # 90deg = up -> cy decreases
        self.assertAlmostEqual(x, 90)
        self.assertAlmostEqual(cy, 150)

    def test_left(self):
        x, cy = build.hint_xy(100, 200, 180, 50, 20)
        self.assertAlmostEqual(x, 100 - 50 - 10)
        self.assertAlmostEqual(cy, 200)

    def test_down(self):
        x, cy = build.hint_xy(100, 200, 270, 50, 20)    # 270deg = down -> cy increases
        self.assertAlmostEqual(x, 90)
        self.assertAlmostEqual(cy, 250)


if __name__ == "__main__":
    unittest.main(verbosity=2)
