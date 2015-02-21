#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
__author__ = 'Nycidian'

from six import iteritems
from collections import Counter


class Congruence(object):
    # TODO Docstring

    def __init__(self, alpha_sequence=None, reflect=True, cyclic=False):
        self.alpha_sequence = alpha_sequence
        self.reflect = reflect
        self.cyclic = cyclic
        self.congruence_set = None

        if alpha_sequence is not None:
            self._mutable_error(alpha_sequence)
            self._unordered_error(alpha_sequence)
            self.congruence_set = self.make_congruence_set(alpha_sequence)

    def __call__(self, beta_sequence=None, omega_sequence=None):

        if beta_sequence is None:
            self.reset(reflect=self.reflect, cyclic=self.cyclic)

        elif self.alpha_sequence is None:
            if omega_sequence is None:
                # Store β as α if non-mutable, else raises error
                self._mutable_error(beta_sequence)
                self._unordered_error(beta_sequence)
                self.alpha_sequence = beta_sequence
                self.congruence_set = self.make_congruence_set(beta_sequence)
            else:
                # Test: β ≅ ω (accepts mutables)
                return self.make_congruence_set(beta_sequence) == self.make_congruence_set(omega_sequence)

        else:
            if omega_sequence is None:
                # Test: α ≅ β
                return self.congruence_set == self.make_congruence_set(beta_sequence)
            else:
                # Test: α ≅ β ≅ ω
                self._unordered_error(omega_sequence)
                return self.congruence_set == self.make_congruence_set(beta_sequence) \
                    == self.make_congruence_set(omega_sequence)

    @staticmethod
    def _mutable_error(sequence_object):
        error = False
        try:
            hash(sequence_object)
        except TypeError as e:
            for arg in e.args:
                if "unhashable type" in arg:
                    error = True

        if error:
            raise TypeError('The sequence being stored in Congruence must be immutable')

    @staticmethod
    def _unordered_error(sequence_object):
        error = False
        try:
            for _ in sequence_object:
                break
        except TypeError as e:
            for arg in e.args:
                if "is not sequence" in arg:
                    error = True
        try:
            for (_, _) in iteritems(sequence_object):
                error = True
                break
        except AttributeError:
            pass

        if error:
            raise TypeError('Requires a sequence')

    def reset(self, alpha_sequence=None, reflect=True, cyclic=False):
        self.alpha_sequence = alpha_sequence
        self.reflect = reflect
        self.cyclic = cyclic
        self.congruence_set = None

        if alpha_sequence is not None:
            self._mutable_error(alpha_sequence)
            self._unordered_error(alpha_sequence)
            self.congruence_set = self.make_congruence_set(alpha_sequence)

    def set_reflect(self, reflect=False):
        self.reset(self.alpha_sequence, reflect=reflect, cyclic=self.cyclic)

    def set_cyclic(self, cyclic=True):
        self.reset(self.alpha_sequence, reflect=self.reflect, cyclic=cyclic)

    def make_congruence_set(self, sequence, cyclic=None, reflect=None):

        sequence = tuple(sequence)

        if cyclic is None:
            cyclic = self.cyclic

        if reflect is None:
            reflect = self.reflect

        sequence_rev = sequence[::-1]


        if cyclic:
            index_rev = self._unique_shape_index_(sequence_rev)
            index = self._unique_shape_index_(sequence)

            if reflect:
                return frozenset(['make_congruence_set_cyclic', self._unique_shape_(sequence, index),
                                  self._unique_shape_(sequence_rev, index_rev)])
            else:
                return frozenset(['make_congruence_set_cyclic', self._unique_shape_(sequence, index)])
        else:
            if reflect:
                return frozenset(['make_congruence_set_linear', sequence, sequence_rev])
            else:
                return frozenset(['make_congruence_set_linear', sequence])

    @staticmethod
    def _unique_shape_(sequence, index):

        length = len(sequence)
        this = []

        for n in range(length):
            this.append(sequence[((index + n) % length)])

        return tuple(this)

    @staticmethod
    def _unique_shape_index_(sequence_object):
        """
        :param sequence_object: an ordered sequence object
        :return: An index in the above sequence that is a unique identifier in relation to shape.
        """
        length = len(sequence_object)
        if len(set(sequence_object)) == 1:
            # Uniform List
            return 0

        def find_unique_place(place_list, level=0, last_least=10000000):
            new_object_dict = {}
            least = Counter()

            for index in place_list:
                this = [sequence_object[index]]

                for i in range(level):
                    # Modular access adding one to the tuple every level
                    this = this + [sequence_object[((index+1+i) % length)]]
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

        return find_unique_place(range(len(sequence_object)))

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