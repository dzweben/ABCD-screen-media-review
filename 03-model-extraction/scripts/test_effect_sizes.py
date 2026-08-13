"""
Unit tests for effect_sizes.py.

Run from this directory:
    python3 -m unittest test_effect_sizes -v
or
    python3 test_effect_sizes.py
"""

import math
import unittest

from effect_sizes import (
    linear_continuous_to_d,
    or_to_d,
    rr_to_d,
    d_passthrough,
    standardized_beta_to_d,
    to_d,
)


CHINN = math.sqrt(3) / math.pi  # ~ 0.5513


class TestLinearContinuous(unittest.TestCase):
    def test_zero_B_gives_zero_d(self):
        self.assertAlmostEqual(linear_continuous_to_d(0, 1.0, 10.0), 0.0)

    def test_paper_394_texting_depressive(self):
        # Hand-checked: B=0.26, SD_IV=0.6, SD_DV=10
        # beta_std = 0.0156, r ~ 0.0156, d = 2(0.0156)/sqrt(1-0.0156^2)
        d = linear_continuous_to_d(0.26, 0.6, 10.0)
        expected = 2 * 0.0156 / math.sqrt(1 - 0.0156 ** 2)
        self.assertAlmostEqual(d, expected, places=6)
        self.assertAlmostEqual(d, 0.03120, places=4)

    def test_negative_sign_preserved(self):
        d = linear_continuous_to_d(-1.0, 0.5, 5.0)
        self.assertLess(d, 0)
        # beta_std = -0.1, d = -0.2/sqrt(0.99) = -0.20101
        self.assertAlmostEqual(d, -0.20101, places=4)

    def test_zero_sd_raises(self):
        with self.assertRaises(ValueError):
            linear_continuous_to_d(1.0, 0.5, 0.0)
        with self.assertRaises(ValueError):
            linear_continuous_to_d(1.0, 0.0, 5.0)
        with self.assertRaises(ValueError):
            linear_continuous_to_d(1.0, -0.1, 5.0)


class TestOR(unittest.TestCase):
    def test_or_one_gives_zero(self):
        self.assertAlmostEqual(or_to_d(1.0), 0.0)

    def test_or_e_gives_chinn(self):
        # ln(e) = 1; d = sqrt(3)/pi
        self.assertAlmostEqual(or_to_d(math.e), CHINN, places=10)

    def test_or_two(self):
        # ln(2) * sqrt(3)/pi
        self.assertAlmostEqual(or_to_d(2.0), math.log(2) * CHINN, places=10)
        self.assertAlmostEqual(or_to_d(2.0), 0.38214, places=4)

    def test_or_half_negative(self):
        self.assertLess(or_to_d(0.5), 0)
        self.assertAlmostEqual(or_to_d(0.5), -or_to_d(2.0), places=10)

    def test_or_invalid_raises(self):
        with self.assertRaises(ValueError):
            or_to_d(0.0)
        with self.assertRaises(ValueError):
            or_to_d(-1.0)


class TestRR(unittest.TestCase):
    def test_rr_one_gives_zero(self):
        self.assertAlmostEqual(rr_to_d(1.0, 0.1), 0.0)

    def test_rr_to_or_conversion_explicit(self):
        # RR=2, p0=0.1: OR = 2 * 0.9 / 0.8 = 2.25, d = ln(2.25) * sqrt(3)/pi
        expected = math.log(2.25) * CHINN
        self.assertAlmostEqual(rr_to_d(2.0, 0.1), expected, places=10)

    def test_rare_outcome_approximates_or(self):
        # As p0 -> 0, RR -> OR
        self.assertAlmostEqual(rr_to_d(1.5, 0.001), or_to_d(1.5), places=2)
        self.assertAlmostEqual(rr_to_d(1.5, 1e-6), or_to_d(1.5), places=5)

    def test_rr_p0_validation(self):
        with self.assertRaises(ValueError):
            rr_to_d(1.5, 0.0)
        with self.assertRaises(ValueError):
            rr_to_d(1.5, 1.0)
        with self.assertRaises(ValueError):
            rr_to_d(2.0, 0.6)  # RR*p0 = 1.2 >= 1

    def test_rr_invalid(self):
        with self.assertRaises(ValueError):
            rr_to_d(0.0, 0.1)
        with self.assertRaises(ValueError):
            rr_to_d(-0.5, 0.1)


class TestPassthrough(unittest.TestCase):
    def test_passthrough(self):
        self.assertEqual(d_passthrough(0.5), 0.5)
        self.assertEqual(d_passthrough(-0.21), -0.21)
        self.assertEqual(d_passthrough(0), 0.0)


class TestStandardizedBeta(unittest.TestCase):
    def test_zero(self):
        self.assertAlmostEqual(standardized_beta_to_d(0.0), 0.0)

    def test_small(self):
        # beta = 0.1, d = 0.2/sqrt(0.99) = 0.20101
        self.assertAlmostEqual(standardized_beta_to_d(0.1), 0.20101, places=4)

    def test_extreme_raises(self):
        with self.assertRaises(ValueError):
            standardized_beta_to_d(0.999)


class TestToD(unittest.TestCase):
    def test_dispatch_linear(self):
        out = to_d({
            "kind": "linear_continuous",
            "B": 0.26, "sd_iv": 0.6, "sd_dv": 10.0,
            "B_lo": 0.09, "B_hi": 0.44,
        })
        self.assertAlmostEqual(out["d"], 0.03120, places=4)
        self.assertLess(out["d_lo"], out["d"])
        self.assertGreater(out["d_hi"], out["d"])

    def test_dispatch_rr(self):
        out = to_d({"kind": "rr", "RR": 1.5, "p0": 0.155})
        # OR = 1.5 * 0.845 / (1 - 1.5*0.155) = 1.2675 / 0.7675 = 1.6515
        # d = ln(1.6515) * 0.5513 = 0.5018 * 0.5513 = 0.27660
        expected_OR = 1.5 * (1 - 0.155) / (1 - 1.5 * 0.155)
        expected_d = math.log(expected_OR) * CHINN
        self.assertAlmostEqual(out["d"], expected_d, places=10)

    def test_dispatch_passthrough(self):
        out = to_d({"kind": "d_passthrough", "d": -0.28})
        self.assertEqual(out["d"], -0.28)

    def test_dispatch_unknown_raises(self):
        with self.assertRaises(ValueError):
            to_d({"kind": "wat"})


if __name__ == "__main__":
    unittest.main()
