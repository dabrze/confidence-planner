import os, sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
print(current)
parent = os.path.dirname(current)
print(parent)
sys.path.append(parent)
from confidence_planner import *


class TestConfidencePlannerMethods(unittest.TestCase):

    def test_clopper_pearson(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            clopper_pearson_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            clopper_pearson_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            clopper_pearson_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            clopper_pearson_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            clopper_pearson_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = clopper_pearson_ci(555, 0.80, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.8)
        self.assertGreaterEqual(ci[1], 0.8)

        self.assertEqual(0.7700069530457014, ci[0])
        self.assertEqual(0.827594221331594, ci[1])

        ci = clopper_pearson_ci(555, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = clopper_pearson_ci(555, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)


    def test_cv_interval(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=0, n_splits=10, accuracy=0.78, confidence_level=0.9)

        # number of folds out of bounds
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=453, n_splits=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=100, n_splits=10, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=57, n_splits=10, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=79, n_splits=10, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            cross_validation_ci(sample_size=79, n_splits=10, accuracy=0.88, confidence_level=1)

        # should not raise exception
        ci = cross_validation_ci(888, 7, 0.8, 0.88)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        self.assertLessEqual(ci[0], 0.8)
        self.assertGreaterEqual(ci[1], 0.8)
        self.assertEqual(ci[0], 0.6946961843481754)
        self.assertEqual(ci[1], 0.9053038156518247)

        ci = cross_validation_ci(555, 10, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = cross_validation_ci(555, 10, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_loose_langford_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            langford_confidence_level(sample_size=0, radius=0.1)

        # Difference out of bounds
        with self.assertRaises(Exception):
            langford_confidence_level(sample_size=100, radius=-0.00948)
        with self.assertRaises(Exception):
            langford_confidence_level(sample_size=100, radius=1.03421)

        langford_confidence_level(200, 0.1)

    def test_loose_langford_reverse(self):
        # Difference out of bounds
        with self.assertRaises(Exception):
            langford_sample_size(interval_radius=-0.00948, confidence_level=0.9)
        with self.assertRaises(Exception):
            langford_sample_size(interval_radius=1.03421, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            langford_sample_size(interval_radius=0.1, confidence_level=0)
        with self.assertRaises(Exception):
            langford_sample_size(interval_radius=0.1, confidence_level=1)

        langford_sample_size(0.15, 0.9)

    def test_langford(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            langford_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            langford_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            langford_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            langford_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            langford_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = langford_ci(555, 0.80, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.8)
        self.assertGreaterEqual(ci[1], 0.8)

        self.assertEqual(ci[0], 0.748049466758245)
        self.assertEqual(ci[1], 0.8519505332417551)

        ci = langford_ci(555, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = langford_ci(555, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_percentiles(self):
        # accuracies out of bounds
        with self.assertRaises(Exception):
            percentiles_ci(accuracies=[0.88, 1.08, 0.68, 0.79], confidence_level=0.9)
        with self.assertRaises(Exception):
            percentiles_ci(accuracies=[0.88, 0.54, 0.68, -0.07], confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            percentiles_ci(accuracies=[0.88, 0.77, 0.68, 0.79], confidence_level=0)
        with self.assertRaises(Exception):
            percentiles_ci(accuracies=[0.88, 0.77, 0.68, 0.79], confidence_level=1)

        accuracies = [0.8, 0.77, 0.9, 0.87, 0.7]
        median_acc = np.median(accuracies)
        ci = percentiles_ci(accuracies, 0.9)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], median_acc)
        self.assertGreaterEqual(ci[1], median_acc)

        self.assertEqual(ci[0], 0.714)
        self.assertEqual(ci[1], 0.894)

    def test_prog_val(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            progressive_validation_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            progressive_validation_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            progressive_validation_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            progressive_validation_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            progressive_validation_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = progressive_validation_ci(100, 0.9, 0.7)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.9)
        self.assertGreaterEqual(ci[1], 0.9)

        self.assertEqual(ci[0], 0.8026059553954689)
        self.assertEqual(ci[1], 0.9973940446045312)

        ci = progressive_validation_ci(100, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = progressive_validation_ci(100, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_reverse_ttest_pr_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            t_test_confidence_level(sample_size=0, radius=0.1)

        # Difference out of bounds
        with self.assertRaises(Exception):
            t_test_confidence_level(sample_size=100, radius=-0.00948)
        with self.assertRaises(Exception):
            t_test_confidence_level(sample_size=100, radius=1.03421)

        t_test_confidence_level(321, 0.09)

    def test_reverse_ztest_pr_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            z_test_confidence_level(sample_size=0, radius=0.1)

        # Difference out of bounds
        with self.assertRaises(Exception):
            z_test_confidence_level(sample_size=100, radius=-0.00948)
        with self.assertRaises(Exception):
            z_test_confidence_level(sample_size=100, radius=1.03421)

        # should not raise exception
        z_test_confidence_level(82, 0.2)

    def test_reverse_ztest_pr(self):
        # Difference out of bounds
        with self.assertRaises(Exception):
            z_test_sample_size(interval_radius=-0.00948, confidence_level=0.9)
        with self.assertRaises(Exception):
            z_test_sample_size(interval_radius=1.03421, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            z_test_sample_size(interval_radius=0.1, confidence_level=0)
        with self.assertRaises(Exception):
            z_test_sample_size(interval_radius=0.1, confidence_level=1)

        # should not raise exception
        z_test_sample_size(0.08, 0.9)

    def test_ttest_pr(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            t_test_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            t_test_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            t_test_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            t_test_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            t_test_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = t_test_ci(100, 0.7, 0.88)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.7)
        self.assertGreaterEqual(ci[1], 0.7)

        self.assertEqual(ci[0], 0.6215845716640249)
        self.assertEqual(ci[1], 0.778415428335975)

        ci = t_test_ci(100, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = t_test_ci(100, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_wilson(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            wilson_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            wilson_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            wilson_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            wilson_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            wilson_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = wilson_ci(132, 0.8, 0.8)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.8)
        self.assertGreaterEqual(ci[1], 0.8)

        self.assertEqual(0.7518173122096052, ci[0])
        self.assertEqual(0.8408090934988961, ci[1])

        ci = wilson_ci(100, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = wilson_ci(100, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_ztest_pr(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            z_test_ci(sample_size=0, accuracy=0.78, confidence_level=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            z_test_ci(sample_size=100, accuracy=1.0034, confidence_level=0.9)
        with self.assertRaises(Exception):
            z_test_ci(sample_size=57, accuracy=-0.000432, confidence_level=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            z_test_ci(sample_size=79, accuracy=0.88, confidence_level=0)
        with self.assertRaises(Exception):
            z_test_ci(sample_size=79, accuracy=0.88, confidence_level=1)

        ci = z_test_ci(321, 0.8, 0.9)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)
        self.assertLessEqual(ci[0], 0.8)
        self.assertGreaterEqual(ci[1], 0.8)

        self.assertEqual(ci[0], 0.754096611561152)
        self.assertEqual(ci[1], 0.845903388438848)

        ci = z_test_ci(100, 0.02, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

        ci = z_test_ci(100, 0.98, 0.90)
        self.assertGreaterEqual(ci[0], 0.0)
        self.assertLessEqual(ci[1], 1.0)

    def test_ci_estimation(self):
        with self.assertRaises(Exception):
            estimate_confidence_interval(300, 0.75, 0.90, method="random_method")

        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_z_test"),
            z_test_ci(300, 0.75, 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_t_test"),
            t_test_ci(300, 0.75, 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_langford"),
            langford_ci(300, 0.75, 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_wilson"),
            wilson_ci(300, 0.75, 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_clopper_pearson"),
            clopper_pearson_ci(300, 0.75, 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, [0.88, 0.9, 0.68, 0.79], 0.90, method="bootstrap"),
            percentiles_ci([0.88, 0.9, 0.68, 0.79], 0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="cv", n_splits=5),
            cross_validation_ci(sample_size=300, n_splits=5, accuracy=0.75, confidence_level=0.90)
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="progressive"),
            progressive_validation_ci(300, 0.75, 0.90)
        )

    def test_cv_sample_size(self):
        for n, splits, conf in [(700, 10, 0.9), (500, 5, 0.8), (1000, 3, 0.95)]:
            acc = 0.8
            ci = cross_validation_ci(n, splits, acc, conf)
            n_estimated = cross_validation_sample_size(acc - ci[0], conf, splits)
            self.assertAlmostEqual(n_estimated, n, delta=1)

    def test_z_test_sample_size(self):
        for n, conf in [(700, 0.9), (500, 0.8), (1000, 0.95)]:
            acc = 0.8
            ci = z_test_ci(n, acc, conf)
            n_estimated = z_test_sample_size(acc - ci[0], conf)
            self.assertAlmostEqual(n_estimated, n, delta=1)

    def test_langford_test_sample_size(self):
        for n, conf in [(700, 0.9), (500, 0.8), (1000, 0.95)]:
            acc = 0.8
            ci = langford_ci(n, acc, conf)
            n_estimated = langford_sample_size(acc - ci[0], conf)
            self.assertAlmostEqual(n_estimated, n, delta=1)
