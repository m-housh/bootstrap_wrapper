from unittest import TestCase
from bootstrap_wrapper.helpers import *

class HelpersTestCase(TestCase):

    def test_unique_strings(self):
        u = UniqueStrings('a','b','c','a','b')
        self.assertEqual('a b c', u())

    def test_kclass_dep(self):
        k = KClassDep('a','b','a','b')
        self.assertEqual({'_class': 'a b'}, k())

        k.append('c','d','a','b')
        self.assertEqual({'_class': 'a b c d'}, k())

    def test_parse_into_single_tuple(self):
        tv = parse_into_single_tuple(('a', ['b', 'c'], ('d', 'e')))
        self.assertEqual(tv, ('a','b','c','d','e'))

    def test_kdep(self):
        k = KDep('a','b','c',key='_class')
        self.assertEqual({'_class': 'a b c d'}, k({'_class': 'd'}))

        k = KDep('a','b','c', key='_class')
        self.assertDictEqual({'_class': 'a b c', 'style': 'some'}, k({'style':'some'}))

    def test_kdefault(self):
        k = KDefault('a','b','c', key='_class')
        self.assertEqual({'_class': 'd'}, k({'_class':'d'}))

        k = KDefault('a','b', key='_class')
        self.assertEqual({'_class': 'a b', 'another': 'd'}, k({'another': 'd'}))

    def test_kclass_dep(self):
        k = KClassDep('a','b','c')
        self.assertEqual({'_class': 'a b c d'}, k({'cls':'d'}))
