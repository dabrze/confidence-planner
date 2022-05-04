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

print(clopper_pearson(100, 77, 0))

print(clopper_pearson(100, 77, -0.02))