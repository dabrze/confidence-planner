# Imports
import os, sys
import unittest

# Importing confidence planner module:
current = os.path.dirname(os.path.realpath(__file__))
print(current)
parent = os.path.dirname(current)
print(parent)
sys.path.append(parent)
from confidence_planner import *

# Boundary case tests
class TestConfidencePlannerMethods(unittest.TestCase):

    def test_clopper_pearson(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            clopper_pearson(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            clopper_pearson(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            clopper_pearson(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            clopper_pearson(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            clopper_pearson(n=79, acc=0.88, conf=1)
           
        # should not raise exception
        clopper_pearson(55, 0.80, 0.9)
        


    def test_cv_interval(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            cv_interval(n=0, k=10, acc=0.78, conf=0.9)

        # number of folds out of bounds
        with self.assertRaises(Exception):
            cv_interval(n=453, k=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            cv_interval(n=100, k=10, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            cv_interval(n=57, k=10, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            cv_interval(n=79, k=10, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            cv_interval(n=79, k=10, acc=0.88, conf=1)
           
        # should not raise exception
        cv_interval(888, 7, 0.8, 0.88)


    def test_loose_langford_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            langford_conf(diff=0.1, n=0)

        # Difference out of bounds
        with self.assertRaises(Exception):
            langford_conf(diff=-0.00948, n=100)
        with self.assertRaises(Exception):
            langford_conf(diff=1.03421, n=100)
           
        # should not raise exception
        langford_conf(0.1, 200)


    def test_loose_langford_reverse(self):
        # Difference out of bounds
        with self.assertRaises(Exception):
            langford_reverse(diff=-0.00948, conf=0.9)
        with self.assertRaises(Exception):
            langford_reverse(diff=1.03421, conf=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            langford_reverse(diff=0.1, conf=0)
        with self.assertRaises(Exception):
            langford_reverse(diff=0.1, conf=1)
           
        # should not raise exception
        langford_reverse(0.15, 0.9)


    def test_loose_langford(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            langford(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            langford(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            langford(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            langford(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            langford(n=79, acc=0.88, conf=1)
           
        # should not raise exception
        langford(100, 0.8, 0.77)


    def test_percentile_BM(self):
        # accuracies out of bounds
        with self.assertRaises(Exception):
            percentile_BM(accs=[0.88, 1.08, 0.68, 0.79], conf=0.9)
        with self.assertRaises(Exception):
            percentile_BM(accs=[0.88, 0.54, 0.68, -0.07], conf=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            percentile_BM(accs=[0.88, 0.77, 0.68, 0.79], conf=0)
        with self.assertRaises(Exception):
            percentile_BM(accs=[0.88, 0.77, 0.68, 0.79], conf=1)
           
        # should not raise exception
        percentile_BM([0.8, 0.77, 0.9, 0.87, 0.7], 0.9)


    def test_prog_val(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            prog_val(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            prog_val(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            prog_val(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            prog_val(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            prog_val(n=79, acc=0.88, conf=1)
           
        # should not raise exception
        prog_val(100, 0.9, 0.7)


    def test_reverse_ttest_pr_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            reverse_ttest_pr_conf(diff=0.1, n=0)

        # Difference out of bounds
        with self.assertRaises(Exception):
            reverse_ttest_pr_conf(diff=-0.00948, n=100)
        with self.assertRaises(Exception):
            reverse_ttest_pr_conf(diff=1.03421, n=100)
           
        # should not raise exception
        reverse_ttest_pr_conf(0.09, 321)


    def test_reverse_ztest_pr_conf(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            reverse_ztest_pr_conf(diff=0.1, n=0)

        # Difference out of bounds
        with self.assertRaises(Exception):
            reverse_ztest_pr_conf(diff=-0.00948, n=100)
        with self.assertRaises(Exception):
            reverse_ztest_pr_conf(diff=1.03421, n=100)
           
        # should not raise exception
        reverse_ztest_pr_conf(0.2, 82)


    def test_reverse_ztest_pr(self):
        # Difference out of bounds
        with self.assertRaises(Exception):
            reverse_ztest_pr(diff=-0.00948, conf=0.9)
        with self.assertRaises(Exception):
            reverse_ztest_pr(diff=1.03421, conf=0.9)

        # confidence out of bounds
        with self.assertRaises(Exception):
            reverse_ztest_pr(diff=0.1, conf=0)
        with self.assertRaises(Exception):
            reverse_ztest_pr(diff=0.1, conf=1)
           
        # should not raise exception
        reverse_ztest_pr(0.08, 0.9)


    def test_ttest_pr(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            ttest_pr(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            ttest_pr(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            ttest_pr(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            ttest_pr(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            ttest_pr(n=79, acc=0.88, conf=1)
           
        # should not raise exception
        ttest_pr(100, 0.7, 0.88)


    def test_wilson(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            wilson(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            wilson(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            wilson(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            wilson(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            wilson(n=79, acc=0.88, conf=1)
          
        # should not raise exception
        wilson(132, 0.8, 0.8)



    def test_ztest_pr(self):
        # number of samples out of bounds
        with self.assertRaises(Exception):
            ztest_pr(n=0, acc=0.78, conf=0.9)

        # accuracies out of bounds
        with self.assertRaises(Exception):
            ztest_pr(n=100, acc=1.0034, conf=0.9)
        with self.assertRaises(Exception):
            ztest_pr(n=57, acc=-0.000432, conf=0.9)
        
        # confidence out of bounds
        with self.assertRaises(Exception):
            ztest_pr(n=79, acc=0.88, conf=0)
        with self.assertRaises(Exception):
            ztest_pr(n=79, acc=0.88, conf=1)
           
        # should not raise exception
        ztest_pr(321, 0.7, 0.9)

    def test_ci_estimation(self):
        with self.assertRaises(Exception):
            estimate_confidence_interval(300, 0.75, 0.90, method="random_method")

        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_z_test"),
            ztest_pr(300, 0.75, 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_t_test"),
            ttest_pr(300, 0.75, 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_langford"),
            langford(300, 0.75, 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_wilson"),
            wilson(300, 0.75, 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="holdout_clopper_pearson"),
            clopper_pearson(300, 0.75, 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, [0.88, 0.9, 0.68, 0.79], 0.90, method="bootstrap"),
            percentile_BM([0.88, 0.9, 0.68, 0.79], 0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="cv", n_splits=5),
            cv_interval(n=300, k=5, acc=0.75, conf=0.90)[0]
        )
        self.assertEqual(
            estimate_confidence_interval(300, 0.75, 0.90, method="progressive"),
            prog_val(300, 0.75, 0.90)[0]
        )



