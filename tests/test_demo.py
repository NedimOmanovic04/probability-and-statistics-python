import unittest
import numpy as np
from scipy import stats
from examples.demo import experiment, mean_interval


class StatisticsTests(unittest.TestCase):
    def test_interval_against_reference(self):
        sample = np.array([2., 4., 5., 7., 9.])
        reference = stats.t.interval(0.95, len(sample) - 1,
                                     loc=sample.mean(), scale=stats.sem(sample))
        np.testing.assert_allclose(mean_interval(sample), reference)

    def test_invalid_samples(self):
        for sample in ([], [1], [1, np.nan], [[1, 2], [3, 4]]):
            with self.assertRaises(ValueError):
                mean_interval(sample)
        with self.assertRaises(ValueError):
            mean_interval([1, 2], confidence=1)

    def test_simulation_matches_analytic_probability(self):
        report, *_ = experiment()
        self.assertAlmostEqual(report['binomial_exact_probability'], 6 / 32)
        self.assertLess(abs(report['binomial_simulated_probability'] - 6 / 32),
                        5 * report['monte_carlo_standard_error'])
        self.assertLess(abs(report['clt']['observed_mean_of_means'] - 2), 0.03)


if __name__ == '__main__':
    unittest.main()
