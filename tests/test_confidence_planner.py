# Imports
import os, sys
import unittest

# Importing confidence planner module:

current = os.path.dirname(os.path.realpath(__file__))
print(current)

parent = os.path.dirname(current)
print(parent)

sys.path.append(parent)

from src.confidence_planner.confidence_planner import *

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)


class TestConfidencePlannerMethods(unittest.TestCase):

    def test_min_max(self):
        pass

    def test_min_max_conf(self):
        pass


    def test_clopper_pearson(self):

        with self.assertRaises(Exception):
            clopper_pearson(n=0, acc=78, conf=0.9)

        with self.assertRaises(Exception):
            clopper_pearson(n=100, acc=100.0034, conf=0.9)
        with self.assertRaises(Exception):
            clopper_pearson(n=57, acc=-0.000432, conf=0.9)
        
        with self.assertRaises(Exception):
            clopper_pearson(n=79, acc=88, conf=0)
        with self.assertRaises(Exception):
            clopper_pearson(n=79, acc=88, conf=1)
        


    def test_cv_interval(self):
        pass


    def test_loose_langford_conf(self):
        pass


    def test_loose_langford_reverse(self):
        pass


    def test_loose_langford(self):
        pass


    def test_percentile_BM(self):
        pass


    def test_prog_val(self):
        pass


    def test_reverse_ttest_pr_conf(self):
        pass


    def test_reverse_ztest_pr_conf(self):
        pass


    def test_reverse_ztest_pr(self):
        pass


    def test_ttest_pr(self):
        pass


    def test_wilson(self):
        pass


    def test_ztest_pr(self):
        pass


# if __name__ == '__main__':
    # unittest.main()

