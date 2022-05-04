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


# class TestConfidencePlannerMethods(unittest.TestCase):

#     def



# if __name__ == '__main__':
    # unittest.main()

