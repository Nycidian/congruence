__author__ = 'Nycidian'

import unittest
from congruence import Congruence

'''
init and call with no arguments
init with diffretn types of iterables
calls diffretn itterables
test errors
test __equality__
'''

class TestOne(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.test_1 = 'bcdea'
        cls.test_2 = 'abcde'
        cls.test_3 = 'edcba'

        cls.test_4 = 'aaaaa'

        cls.test_5 = 1, 2, 3, 4, 5, 6
        cls.test_6 = 3, 4, 5, 6, 1, 2
        cls.test_7 = 6, 5, 4, 3, 2, 1

    def test_get(self):

        class_1 = Congruence(self.test_1)

        self.assertEqual(self.class_1[1], 'd')


