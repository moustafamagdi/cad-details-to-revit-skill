"""Synthetic fixtures only; no customer CAD, fonts or model data."""
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'cad-details-to-revit' / 'scripts'))
from conversion_math import (pdf_calibration, pdf_point, cad_point_to_feet,
                             hatch_grid, hatch_segments)
from make_cad_script import make_script, lisp_string


class ConversionTests(unittest.TestCase):
    def test_borders_and_y_inversion(self):
        c = pdf_calibration((10, 20, 110, 220), (1000, 2000, 2000, 4000))
        self.assertEqual(pdf_point((10, 20), c), (1000, 4000))
        self.assertEqual(pdf_point((110, 220), c), (2000, 2000))
        self.assertEqual(pdf_point((60, 120), c), (1500, 3000))

    def test_bad_calibration_is_rejected(self):
        for border in [(0, 0, 100, 300), (0, 0, 0, 200),
                       (0, 0, math.inf, 200)]:
            with self.assertRaises(ValueError):
                pdf_calibration(border, (0, 0, 1000, 2000))

    def test_units_and_origin(self):
        self.assertEqual(cad_point_to_feet((22, 34), 25.4, (10, 10)),
                         (1.0, 2.0, 0.0))

    def test_grid_direction_and_scale(self):
        g = hatch_grid(90, (20, 10), (100, 200), 1, 100, (100, 100))
        self.assertAlmostEqual(g['offset'], -20/30480)
        self.assertAlmostEqual(g['shift'], 10/30480)
        self.assertAlmostEqual(g['origin'][1], 100/30480)

    def test_segments_and_repeat_length(self):
        values = hatch_segments([2, -8, 0, -10], 0.1, 0.05)
        self.assertEqual(values[:2], [0.2, 0.8])
        self.assertAlmostEqual(sum(values), 2.0)
        self.assertTrue(all(x > 0 for x in values))
        self.assertEqual(hatch_segments([], 1, 0.01), [])

    def test_nonconventional_patterns_are_not_guessed(self):
        for a in [[-2, 8], [2], [0, 0], [1, math.nan]]:
            with self.assertRaises(ValueError):
                hatch_segments(a, 1, 0.01)
        with self.assertRaises(ValueError):
            hatch_segments([0, -0.001], 1, 0.01)

    def test_cad_export_is_non_destructive(self):
        s = make_script('scratch/a.dxf', 'scratch/a.pdf', (0, 0, 300, 500),
                        'Example.pc3', 'Example paper', 'Example.ctb')
        self.assertIn('"_W" "scratch/a.pdf" "_No" "_Yes"', s)
        self.assertNotIn('save', s.lower())
        self.assertNotIn('explode', s.lower())
        with self.assertRaises(ValueError):
            lisp_string('bad\n(command)')
        self.assertEqual(lisp_string('a"b'), '"a\\"b"')


if __name__ == '__main__':
    unittest.main()
