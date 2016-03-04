from unittest import TestCase
from bootstrap_wrapper.helpers import *

class HelpersTestCase(TestCase):

    def test_unique_strings(self):
        u = UniqueStrings('a','b','c','a','b')
        self.assertEqual('a b c', u())

    def test_kclass(self):
        k = KClass('a','b','a','b')
        self.assertEqual({'_class': 'a b'}, k())

        k.append('c','d','a','b')
        self.assertEqual({'_class': 'a b c d'}, k())
