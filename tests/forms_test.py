from unittest import TestCase

from dominate.tags import *

from bootstrap_wrapper.forms import *

class FormsTestCase(TestCase):

    def test_bootstrap_form(self):
        f = BootstrapForm(action='/test')
        tv = form(role='form', action='/test', method='POST')
        self.assertEqual(f.render(), tv.render())
