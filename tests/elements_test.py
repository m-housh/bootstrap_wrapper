from unittest import TestCase
from bootstrap_wrapper.elements import *
from dominate.tags import *

class ElementsTestCase(TestCase):

    def test_div(self):
        d = Div()
        self.assertEqual(d.render(), div(_class='container').render())

        d = Div(fluid=True)
        self.assertEqual(d.render(), div(_class='container-fluid').render())

        d = Div(_class='some')
        self.assertEqual(d.render(), div(_class='container some').render())
