#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
__author__ = 'Nycidian'

from six import iteritems
from collections import Counter


class Congruence(object):
    """
    Takes
    """

    def __init__(self, alpha_iterable=None):
        if alpha_iterable is not None:
            self._mutable_error(alpha_iterable)
            self._unordered_error(alpha_iterable)
            self.congruence_hash_alpha = self.congruence_hash(alpha_iterable)

        self.alpha_iterable = alpha_iterable


    def __call__(self, beta_iterable, omega_iterable=None):
        self._unordered_error(beta_iterable)
        if self.alpha_iterable is None:
            if omega_iterable is None:
                print('store β as α if non-mutable, else raise error')
                print(beta_iterable)
                self._mutable_error(beta_iterable)
                self._unordered_error(beta_iterable)
                self.alpha_iterable = beta_iterable
                self.congruence_hash_alpha = self.congruence_hash(beta_iterable)
            else:
                print('Test: β ≅ ω (Accepts Mutables)')
                return self.congruence_hash(beta_iterable) == self.congruence_hash(omega_iterable)
        else:
            if omega_iterable is None:
                print('Test: α ≅ β')
                return self.congruence_hash_alpha == self.congruence_hash(beta_iterable)
            else:
                self._unordered_error(omega_iterable)
                print('Test: α ≅ β ≅ ω')
                return self.congruence_hash_alpha == self.congruence_hash(beta_iterable) \
                       == self.congruence_hash(omega_iterable)

    @staticmethod
    def _mutable_error(iterable_object):
        error = False
        try:
            hash(iterable_object)
        except TypeError as e:
            for arg in e.args:
                if "unhashable type" in arg:
                    error = True

        if error:
            raise TypeError('The ordered iterable being stored in Congruence must be immutable')

    @staticmethod
    def _unordered_error(iterable_object):
        error = False
        try:
            for i in iterable_object:
                pass
        except TypeError as e:
            for arg in e.args:
                if "is not iterable" in arg:
                    error = True
        try:
            for (k, v) in iteritems(iterable_object):
                error = True
                break
        except AttributeError:
            pass

        if error:
            raise TypeError('Requires an ordered iterable')

    def congruence_hash(self, iterable):
        index = self.unique_shape_index(iterable)
        return hash(('congruence_hash', self.unique_shape(iterable, index)))

    @staticmethod
    def unique_shape(iterable, index):

        length = len(iterable)
        this = []

        for n in range(length):
            this.append(iterable[((index + n) % length)])

        return tuple(this)


    @staticmethod
    def unique_shape_index(iterable_object):
        """
        :param iterable_object: an ordered iterable object
        :return: An index in the above iterable that is a unique identifier in relation to shape.
        """
        length = len(iterable_object)
        if len(set(iterable_object)) == 1:
            print('Uniform List')
            return 0

        def find_unique_place(place_list, level=0, last_least=10000000):
            new_object_dict = {}
            least = Counter()

            for index in place_list:
                this = [iterable_object[index]]

                for i in range(level):
                    # Modular access adding one to the tuple every level
                    this = this + [iterable_object[((index+1+i) % length)]]
                this = tuple(this)
                least[this] += 1
                try:
                    occurrence, indexes = new_object_dict[this]
                    occurrence += 1
                    new_object_dict[this] = occurrence, indexes + [index]

                except KeyError:
                    occurrence = 1
                    new_object_dict[this] = occurrence, [index]

            least_value = None
            item_list = []
            for item in reversed(least.most_common()):
                if least_value is None:
                    least_value = item[1]

                if least_value == item[1]:
                    item_list = item_list + [item[0]]
                else:
                    break
            # Checks if all entries are split in equal amounts indicating a possible repeat pattern
            break_check = len(least) == len(item_list)

            least_o = max(item_list)
            if least_value > 1:
                print('least_value > 1 @level {}'.format(level))
                place_list = [i for i in new_object_dict[least_o][1]]
                if least_value == last_least:
                    # if break check is true and the list is no longer being reduced,
                    #   then the list is irreducible due to a repeat pattern which does not need to be reduced further
                    if break_check:
                        return new_object_dict[least_o][1][0]
                return find_unique_place(place_list, level+1, least_value)
            else:
                print('Returns @level {}'.format(level))
                return new_object_dict[least_o][1][0]

        return find_unique_place(range(len(iterable_object)))

