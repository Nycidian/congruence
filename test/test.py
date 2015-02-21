__author__ = 'Nycidian'

import unittest
from congruence import Congruence
from string import ascii_letters as letters
from random import choice, randint

'''
calls different sequences
test errors
'''

class TestNone(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.test_1 = 'bcdea'
        cls.test_2 = 'abcde'
        cls.test_3 = 'edcba'

        cls.test_4 = 'aaaaa'

        cls.test_5 = 1, 2, 3, 4, 5, 6
        cls.test_6 = 3, 4, 5, 6, 1, 2
        cls.test_7 = 6, 5, 4, 3, 2, 1

    def test_none(self):

        class_1 = Congruence()
        self.assertEqual(class_1.alpha_sequence, None)
        class_1(self.test_1)
        self.assertEqual(class_1.alpha_sequence, self.test_1)
        class_1()
        self.assertEqual(class_1.alpha_sequence, None)


class TestLinear(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.test_1 = 'bcdea'
        cls.test_2 = ('b', 'c', 'd', 'e', 'a')
        cls.test_3 = 'aedcb'
        cls.test_4 = ('a', 'e', 'd', 'c', 'b')

        cls.test_5 = ['a', 'e', 'd', 'c', 'b']

    def test(self):

        class_1 = Congruence(self.test_1)
        class_2 = Congruence(self.test_2)
        class_3 = Congruence(self.test_3)
        class_4 = Congruence(self.test_4)

        class_5 = Congruence(self.test_1, reflect=False)

        self.assertEqual(class_1, class_2)
        self.assertEqual(class_2, class_3)
        self.assertTrue(class_4(self.test_5))
        self.assertFalse(class_5(self.test_5))


class TestCyclic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        let = list(letters)
        numbers = list(range(0, 100, 1))
        cls.alpha_numeric = let + numbers

    def test(self):

        for _ in self.alpha_numeric:

            length_int = randint(5, 100)
            length_range = range(0, length_int, 1)
            rotate = randint(1, length_int-1)

            list_1 = [choice(self.alpha_numeric) for _ in length_range]
            list_2 = list_1[rotate:] + list_1[:rotate]

            class_1 = Congruence(tuple(list_1), cyclic=True)
            class_2 = Congruence(tuple(list_2), cyclic=True)

            self.assertEqual(class_1, class_2)

