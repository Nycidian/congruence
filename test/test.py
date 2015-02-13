__author__ = 'Nycidian'

import unittest
from congruence import Congruence

class TestGem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_1 = 0, 'd', (1, 2)
        cls.test_2 = 1, 'a', (2, 3)
        cls.class_1 = Gem(*cls.test_1)
        cls.class_2 = Gem(*cls.test_2)
        cls.class_3 = Gem(*cls.test_1)
        cls.class_4 = Ring(*cls.test_1)

    def test_get(self):
        self.assertEqual(self.class_1[1], 'd')


