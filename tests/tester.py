# Imports
import os, sys
import unittest

# Importing confidence planner module:

current = os.path.dirname(os.path.realpath(__file__))
# print(current)

parent = os.path.dirname(current)
# print(parent)

sys.path.append(parent)

from src.confidence_planner.confidence_planner import *

# print(clopper_pearson(100, 0.77, 0.77))

# # print(clopper_pearson(100, 77, -0.02))

# print(loose_langford_conf(0, 50))

# print(loose_langford_conf(1, 50))
print('per BM')
print(percentile_BM([56, 77, 98, 34, 87, 57], 0.89))