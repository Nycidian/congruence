#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
__author__ = 'Nycidian'

from six import iteritems
from collections import Counter


class Congruence(object):
    # TODO Docstring

    def __init__(self, alpha_iterable=None, reflect=True, cyclic=False):
        self.alpha_iterable = alpha_iterable
        self.reflect = reflect
        self.cyclic = cyclic
        self.congruence_set = None

        if alpha_iterable is not None:
            self._mutable_error(alpha_iterable)
            self._unordered_error(alpha_iterable)
            self.congruence_set = self.make_congruence_set(alpha_iterable)

    def __call__(self, beta_iterable=None, omega_iterable=None):

        if beta_iterable is None:
            self.reset(reflect=self.reflect, cyclic=self.cyclic)

        elif self.alpha_iterable is None:
            if omega_iterable is None:
                # Store β as α if non-mutable, else raises error
                print(beta_iterable)
                self._mutable_error(beta_iterable)
                self._unordered_error(beta_iterable)
                self.alpha_iterable = beta_iterable
                self.congruence_set = self.make_congruence_set(beta_iterable)
            else:
                # Test: β ≅ ω (accepts mutables)
                return self.make_congruence_set(beta_iterable) == self.make_congruence_set(omega_iterable)

        else:
            if omega_iterable is None:
                # Test: α ≅ β
                return self.congruence_set == self.make_congruence_set(beta_iterable)
            else:
                # Test: α ≅ β ≅ ω
                self._unordered_error(omega_iterable)
                return self.congruence_set == self.make_congruence_set(beta_iterable) \
                    == self.make_congruence_set(omega_iterable)

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
            for _ in iterable_object:
                break
        except TypeError as e:
            for arg in e.args:
                if "is not iterable" in arg:
                    error = True
        try:
            for (_, _) in iteritems(iterable_object):
                error = True
                break
        except AttributeError:
            pass

        if error:
            raise TypeError('Requires an ordered iterable')

    def reset(self, alpha_iterable=None, reflect=True, cyclic=False):
        self.alpha_iterable = alpha_iterable
        self.reflect = reflect
        self.cyclic = cyclic
        self.congruence_set = None

        if alpha_iterable is not None:
            self._mutable_error(alpha_iterable)
            self._unordered_error(alpha_iterable)
            self.congruence_set = self.make_congruence_set(alpha_iterable)

    def set_reflect(self, reflect=False):
        self.reset(self.alpha_iterable, reflect=reflect, cyclic=self.cyclic)

    def set_cyclic(self, cyclic=True):
        self.reset(self.alpha_iterable, reflect=self.reflect, cyclic=cyclic)

    def make_congruence_set(self, iterable, cyclic=None, reflect=None):
        if cyclic is None:
            cyclic = self.cyclic

        if reflect is None:
            reflect = self.reflect

        iterable_rev = iterable[::-1]

        if cyclic:
            index_rev = self._unique_shape_index_(iterable_rev)
            index = self._unique_shape_index_(iterable)

            if reflect:
                return frozenset(['make_congruence_set_cyclic', self._unique_shape_(iterable, index),
                                  self._unique_shape_(iterable_rev, index_rev)])
            else:
                return frozenset(['make_congruence_set_cyclic', self._unique_shape_(iterable, index)])
        else:
            if reflect:
                return frozenset(['make_congruence_set_linear', iterable, iterable_rev])
            else:
                return frozenset(['make_congruence_set_linear', iterable])

    @staticmethod
    def _unique_shape_(iterable, index):

        length = len(iterable)
        this = []

        for n in range(length):
            this.append(iterable[((index + n) % length)])

        return tuple(this)

    @staticmethod
    def _unique_shape_index_(iterable_object):
        """
        :param iterable_object: an ordered iterable object
        :return: An index in the above iterable that is a unique identifier in relation to shape.
        """
        length = len(iterable_object)
        if len(set(iterable_object)) == 1:
            # Uniform List
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

                place_list = [i for i in new_object_dict[least_o][1]]
                if least_value == last_least:
                    # if break check is true and the list is no longer being reduced,
                    #   then the list is irreducible due to a repeat pattern which does not need to be reduced further
                    if break_check:
                        return new_object_dict[least_o][1][0]
                return find_unique_place(place_list, level+1, least_value)
            else:
                return new_object_dict[least_o][1][0]

        return find_unique_place(range(len(iterable_object)))

    def __hash__(self):
        return hash(self.congruence_set)

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except TypeError:
            return False

        return False

    def __str__(self):
        return '<{} Object: {}>'.format(self.__class__.__name__, hash(self))

    def __repr__(self):
        return '<{} Object: {}>'.format(self.__class__.__name__, hash(self))