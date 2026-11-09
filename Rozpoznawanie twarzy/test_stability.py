"""Decision regressions; no camera or model downloads needed."""
import unittest
import numpy as np
from main import Stability, identify


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.state = Stability()
        self.box = np.array([10., 10., 100., 100.])

    def test_three_consecutive_matches(self):
        self.assertFalse(self.state.update('A', self.box, 1.0))
        self.assertFalse(self.state.update('A', self.box, 1.1))
        self.assertTrue(self.state.update('A', self.box, 1.2))

    def test_change_person_starts_new_sequence(self):
        self.state.update('A', self.box, 1.0)
        self.state.update('A', self.box, 1.1)
        self.assertFalse(self.state.update('B', self.box, 1.2))
        self.assertEqual(self.state.count, 1)

    def test_reset_invalidates_previous_acceptance(self):
        for t in (1.0, 1.1, 1.2):
            self.state.update('A', self.box, t)
        self.state.reset()
        self.assertFalse(self.state.update('A', self.box, 1.3))
        self.assertEqual(self.state.count, 1)

    def test_gap_and_spatial_jump(self):
        self.state.update('A', self.box, 1.0)
        self.state.update('A', self.box, 2.1)
        self.assertEqual(self.state.count, 1)
        self.state.update('A', self.box + 400, 2.2)
        self.assertEqual(self.state.count, 1)

    def test_ambiguous_identity_is_rejected(self):
        gallery = {'A': [np.array([1., 0.])], 'B': [np.array([0.99, 0.1])]}
        name, _ = identify(np.array([1., 0.]), gallery, 0.363, 0.05)
        self.assertIsNone(name)

    def test_unknown_is_rejected(self):
        name, _ = identify(np.array([0., 1.]), {'A': [np.array([1., 0.])]}, 0.363, 0.05)
        self.assertIsNone(name)


if __name__ == '__main__':
    unittest.main()
