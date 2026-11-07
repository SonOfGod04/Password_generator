import string
import unittest

from password_core import (
    AMBIGUOUS, MAX_LENGTH, MIN_LENGTH, SYMBOLS,
    estimate_entropy_bits, generate_password,
)


class GeneratePasswordTests(unittest.TestCase):
    def test_length_respected_across_range(self):
        for n in (MIN_LENGTH, 16, MAX_LENGTH):
            self.assertEqual(len(generate_password(n)), n)

    def test_every_selected_class_present(self):
        for _ in range(200):
            pw = generate_password(MIN_LENGTH)
            self.assertTrue(any(c in string.ascii_lowercase for c in pw))
            self.assertTrue(any(c in string.ascii_uppercase for c in pw))
            self.assertTrue(any(c in string.digits for c in pw))
            self.assertTrue(any(c in SYMBOLS for c in pw))

    def test_unselected_classes_absent(self):
        pw = generate_password(64, upper=False, symbols=False)
        self.assertTrue(set(pw) <= set(string.ascii_lowercase + string.digits))

    def test_ambiguous_excluded(self):
        for _ in range(100):
            self.assertFalse(set(generate_password(64, exclude_ambiguous=True)) & AMBIGUOUS)

    def test_invalid_input(self):
        for bad in (MIN_LENGTH - 1, MAX_LENGTH + 1, "12", 12.5, True):
            with self.assertRaises(ValueError):
                generate_password(bad)
        with self.assertRaises(ValueError):
            generate_password(16, lower=False, upper=False, digits=False, symbols=False)

    def test_passwords_differ(self):
        self.assertEqual(len({generate_password(20) for _ in range(500)}), 500)

    def test_entropy(self):
        self.assertAlmostEqual(estimate_entropy_bits(10, upper=False, symbols=False, digits=False),
                               10 * 4.700439718, places=3)


if __name__ == "__main__":
    unittest.main()
