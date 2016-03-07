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
        self.assertEqual(d.render(), div(_class='some').render())


    def test_subclassing_element(self):
        class FDiv(Div):
            def __init__(self, *args, **kwargs):
                kwargs.update({'_class': 'fdivclass'})
                super().__init__(*args, **kwargs)


        self.assertEqual(FDiv().render(), div(_class='fdivclass').render())


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

    def test_table_header(self):
        t = TableHeader('Column1', 'Column2')
        tv = thead(tr(th('Column1'),th('Column2')))
        self.assertEqual(t.render(), tv.render())
        
        t.add('Column3')
        tv.children[0].add(th('Column3'))
        self.assertEqual(t.render(), tv.render())

    def test_table_row(self):
        t = TableRow('Item1', 'Item2')
        tv = tr(td('Item1'), td('Item2'))
        self.assertEqual(t.render(), tv.render())

        t = TableRow(info=True)
        tv = tr(_class='info')
        self.assertEqual(t.render(), tv.render())

        t = TableRow(success=True)
        tv = tr(_class='success')
        self.assertEqual(t.render(), tv.render())

        t = TableRow(warning=True)
        tv = tr(_class='warning')
        self.assertEqual(t.render(), tv.render())

        t = TableRow(danger=True)
        tv = tr(_class='danger')
        self.assertEqual(t.render(), tv.render())

    def test_table_body(self):
        t = TableBody(TableRow('Item1', 'Item2'), tr(td('Item3'), td('Item4')))
        tv = tbody(tr(td('Item1'), td('Item2')), tr(td('Item3'), td('Item4')))
        self.assertEqual(t.render(), tv.render())

    def test_table(self):
        t = Table(
            TableHeader('Column1', 'Column2'),
            TableRow('Item1', 'Item2'),
        )
        tv = table(
            thead(tr(th('Column1'), th('Column2'))),
            _class='table'
        )
        _tbody = tv.add(tbody(tr(td('Item1'), td('Item2'))))
        self.assertEqual(t.render(), tv.render())

        t.add(TableRow('Item3', 'Item4'))
        _tbody.add(tr(td('Item3'), td('Item4')))
        self.assertEqual(t.render(), tv.render())

        t = Table(TableBody(), bordered=True, striped=True)
        tv = table(tbody(), _class='table table-bordered table-striped')
        self.assertEqual(t.render(), tv.render())



    def test_responsive_table(self):
        t = ResponsiveTable(Table())
        tv = div(table(tbody(), _class='table'), _class='table-responsive')
        print(t)
        print(tv)
        self.assertEqual(t.render(), tv.render())


    def test_button(self):
        b = Button()
        tv = button(type='button', _class='btn btn-default')
        self.assertEqual(b.render(), tv.render())

        b = Button(anchor=True, link=True)
        tv = a(type='button', _class='btn btn-link')
        self.assertEqual(b.render(), tv.render())

        b = Button(primary=True)
        tv = button(type='button', _class='btn btn-primary')
        self.assertEqual(b.render(), tv.render())

        b = Button(success=True)
        tv = button(type='button', _class='btn btn-success')
        self.assertEqual(b.render(), tv.render())

        b = Button(info=True)
        tv = button(type='button', _class='btn btn-info')
        self.assertEqual(b.render(), tv.render())

        b = Button(danger=True, pull_right=True)
        tv = button(type='button', _class='btn btn-danger pull-right')
        self.assertEqual(b.render(), tv.render())
