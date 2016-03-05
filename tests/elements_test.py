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


    def test_subclassing_element(self):
        class FDiv(Div):
            def __init__(self, *args, **kwargs):
                kwargs.update({'_class': 'fdivclass'})
                super().__init__(*args, **kwargs)


        self.assertEqual(FDiv().render(), div(_class='container fdivclass').render())


    def test_ul_element(self):
        u = Ul('a','b','c')
        tv = ul(li('a'),li('b'),li('c'))
        self.assertEqual(u.render(), tv.render())

        u.add(li('d'))
        tv.add(li('d'))
        self.assertEqual(u.render(), tv.render())

    def test_glyphicon(self):
        g = Glyphicon()
        tv = span(_class='glyphicon glyphicon-home')
        self.assertEqual(g.render(), tv.render())

        g = Glyphicon(icon_name='user', href='#')
        tv = a(_class='glyphicon glyphicon-user', href='#')
        self.assertEqual(g.render(), tv.render())

    def test_dropdown_basic(self):
        d = Dropdown()
        tv = div(
            a(
                span(span(_class='caret')),
                _class='dropdown-toggle', 
                data_toggle='dropdown', 
                href='#'
            ),
            ul(_class='dropdown-menu'),
            _class='dropdown'
        )
        self.assertEqual(d.render(), tv.render())

    def test_dropdown_as_li(self):
        d = Dropdown(li=True)
        tv = li(
            a(
                span(span(_class='caret')),
                _class='dropdown-toggle', 
                data_toggle='dropdown', 
                href='#'
            ),
            ul(_class='dropdown-menu'),
            _class='dropdown'
        )
        self.assertEqual(d.render(), tv.render())

    def test_dropdown_button(self):
        d = DropdownButton('Home', glyph='home')
        tv = a(
            span('Home',
                span(_class='glyphicon glyphicon-home'),
                span(_class='caret')
            ),
            data_toggle='dropdown',
            href='#',
            _class='dropdown-toggle',
        )
        self.assertEqual(d.render(), tv.render())

    def test_dropdown_with_button(self):
        d = Dropdown(
            DropdownButton(glyph='home'),
            a('Menu1', href='#'),
            a('Menu2', href='#'),
        )

        tv = div(
            a(
                span(span(_class='glyphicon glyphicon-home'), span(_class='caret')),
                _class='dropdown-toggle',
                data_toggle='dropdown',
                href='#'
            ),
            ul(
                li(a('Menu1', href='#')),
                li(a('Menu2', href='#')),
                _class='dropdown-menu',
            ),
            _class='dropdown'
        )

        self.assertEqual(d.render(), tv.render())
        
