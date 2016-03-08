from unittest import TestCase
from dominate.tags import *

from bootstrap_wrapper.navigation import *
from bootstrap_wrapper.elements import DropdownButton

class NavigationTestCase(TestCase):
    
    def test_tabbar_basic(self):
        t = Tabbar()
        tv = div(
            ul(_class='nav nav-tabs'),
            div(_class='tab-content'),
            _class='container-fluid'
        )
        self.assertEqual(t.render(), tv.render())

    def test_tabbar(self):
        t = Tabbar(
            Tab('Home', (h1('Home Content')), active=True),
            Tab('Menu1', (h1('Menu1 Content'))),
            'Invalid Item'
        )
        tv = div(
            ul(
                li(
                    a('Home', href='#home', _class='btn btn-link', data_toggle='tab', type='button'),
                    _class='active'
                ),
                li(
                    a('Menu1', href='#menu1', _class='btn btn-link', data_toggle='tab', type='button'),
                ),
                _class='nav nav-tabs'
            ),
            div(
                div(h1('Home Content'), _class='tab-pane fade in active', id='home', \
                        style='border:solid 1px lightgrey;'),
                div(h1('Menu1 Content'), _class='tab-pane fade', id='menu1', \
                        style='border:solid 1px lightgrey;'),
                comment('These items are not of the correct class to add to the tabbar: Invalid Item'),
                _class='tab-content'
            ),
            _class='container-fluid'
        )

        self.assertEqual(t.render(), tv.render())

    def test_tab_content(self):
        t = TabContent()
        tv = div(_class='tab-content')
        self.assertEqual(t.render(), tv.render())

    def test_tabbar_tab(self):
        t = TabbarTab('Home', 'home')
        tv = a('Home', href='#home', _class='btn btn-link', data_toggle='tab', type='button')
        self.assertEqual(t.render(), tv.render())

        t = TabbarTab('Home', 'home', pills=True)
        tv = a('Home', href='#home', _class='btn btn-link', data_toggle='pill', type='button')
        self.assertEqual(t.render(), tv.render())


    def test_tab(self):
        t = Tab('Home', (h1('Tab Content')), active=True)
        tv_tab = a('Home', href='#home', _class='btn btn-link', data_toggle='tab', type='button')
        tv_content = div(h1('Tab Content'), _class='tab-pane fade in active', \
                style='border:solid 1px lightgrey;', id='home')
        
        self.assertEqual(t.tab.render(), tv_tab.render())
        self.assertEqual(t.content.render(), tv_content.render())

    def test_tab_pane(self):
        t = TabPane(h1('Tab Content'), id='home', fade=False, style='border:solid 3px black;')
        tv = div(h1('Tab Content'), _class='tab-pane', style='border:solid 3px black;', \
                id='home')
        self.assertEqual(t.render(), tv.render())

    def test_tabbar_ul(self):
        t = TabbarUl()
        tv = ul(_class='nav nav-tabs')
        self.assertEqual(t.render(), tv.render())

        t = TabbarUl(pills=True)
        tv = ul(_class='nav nav-pills')
        self.assertEqual(t.render(), tv.render())

        t.add(TabbarTab('Home', 'home'), active=True)
        tv.add(li(
            a('Home', href='#home', _class='btn btn-link', data_toggle='tab', type='button'),
            _class='active')
        )
        self.assertEqual(t.render(), tv.render())

        t.add('Home', 'home')
        tv.add(li(comment('These items could not be added to TabbarUl because they are not of class TabbarTab: Home home')))
        self.assertEqual(t.render(), tv.render())

    def test_navbar_brand(self):
        n = NavbarBrand('HHE')
        tv = div('HHE', _class='navbar-header navbar-brand')
        self.assertEqual(n.render(), tv.render())

        n = NavbarBrand('HHE', href='#')
        tv = div(a('HHE', href='#', _class='navbar-brand'), _class='navbar-header')
        self.assertEqual(n.render(), tv.render())

    def test_navbar_items(self):
        n = NavbarItems(a('HHE', href='#'))
        tv = ul(li(a('HHE', href='#')), _class='nav navbar-nav')
        self.assertEqual(n.render(), tv.render())

        n = NavbarItems(right=True)
        tv = ul(_class='nav navbar-nav navbar-right')
        self.assertEqual(n.render(), tv.render())

    def test_navbar_dropdown(self):
        n = NavbarDropdown(
            DropdownButton(glyph='home')
        )

        tv = li(
            a(
                span(
                    span(_class='glyphicon glyphicon-home'),
                    span(_class='caret'),
                ),
                data_toggle='dropdown',
                href='#',
                _class='dropdown-toggle',
            ),
            ul(_class='dropdown-menu'),
            _class='dropdown'
        )
        self.assertEqual(n.render(), tv.render())

    def test_navbar_basic(self):
        n = Navbar()
        tv = nav(_class='navbar navbar-default')
        _div = tv.add(div(_class='container-fluid'))
        self.assertEqual(n.render(), tv.render())

        n = Navbar(inverse=True)
        tv = nav(_class='navbar navbar-inverse')
        _div = tv.add(div(_class='container-fluid'))
        self.assertEqual(n.render(), tv.render())

        # test that brand get's added correctly
        n.add(NavbarBrand('HHE', href='#'))
        _div.add(div(a('HHE', href='#', _class='navbar-brand'), _class='navbar-header'))
        self.assertEqual(n.render(), tv.render())

        n = Navbar(a('Menu1', href='#'), right_only=True)
        tv = nav(_class='navbar navbar-default')
        _div = tv.add(div(_class='container-fluid'))
        _div.add(ul(li(a('Menu1', href='#')), _class='nav navbar-nav navbar-right'))
        self.assertEqual(n.render(), tv.render())

    def test_navbar(self):
        n = Navbar(
            NavbarDropdown(
                DropdownButton(glyph='home')
            ),
            brand=NavbarBrand('HHE', href='#'),
            right_items=(
                NavbarDropdown(
                    DropdownButton(glyph='user')
                ),
            ),
        )


        tv = nav(
            div(
                div(
                    a('HHE', href='#', _class='navbar-brand'),
                    _class='navbar-header',
                ),
                ul(
                    li(
                        a(
                            span(
                                span(_class='glyphicon glyphicon-home'),
                                span(_class='caret'),
                            ),
                            data_toggle='dropdown',
                            href='#',
                            _class='dropdown-toggle'
                        ),
                        ul(_class='dropdown-menu'),
                        _class='dropdown',
                    ),
                    _class='nav navbar-nav',
                ),
                ul(
                    li(
                        a(
                            span(
                                span(_class='glyphicon glyphicon-user'),
                                span(_class='caret'),
                            ),
                            data_toggle='dropdown',
                            href='#',
                            _class='dropdown-toggle'
                        ),
                        ul(_class='dropdown-menu'),
                        _class='dropdown',
                    ),
                    _class='nav navbar-nav navbar-right',
                ),
                _class='container-fluid'
            ),
            _class='navbar navbar-default'
        )

        self.assertEqual(n.render(inline=True), tv.render(inline=True))
        
        
