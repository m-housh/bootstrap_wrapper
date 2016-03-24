"""
    v2.elements
    ~~~~~~~~~~~
"""
import sys
from itertools import chain
from markupsafe import Markup
from dominate.tags import html_tag, div, li, span, th, td, tr

from .helpers import KDep, KClassDep, KClassDefault, KDefault, KwContainer, parse_into_single_tuple

class ElementMeta(type):
    """ Adds tagname override to our elements. """
    tagname = None


class Element(html_tag, metaclass=ElementMeta):
    """ Our base class for all of our tags. """

    def render(self, *args, **kwargs):
        """ runs render through markupsafes Markup. """
        return Markup(super().render(*args, **kwargs))

class Tag(Element):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **self.update_kwargs(kwargs))
    
    def _get_from_instance(self):
        return (item for item in self.__dict__.values() \
                if isinstance(item, KwContainer))

    def _get_from_class(self):
        return (item for item in self.__class__.__dict__.values() \
                if isinstance(item, KwContainer))

    def _get_kclasses(self):
        return chain(self._get_from_class(), self._get_from_instance())
    
    @staticmethod
    def _kwargs(kwargs, lst):
        # do defaults first:
        defaults = list(filter(lambda x: isinstance(x, KDefault), lst))
        if len(defaults) > 0:
            kwargs = defaults[0](kwargs)
            lst.remove(defaults[0])
            return (kwargs, lst)

        kwargs = lst[0](kwargs)
        return (kwargs, lst[1:])

    def update_kwargs(self, kwargs):
        lst = list(self._get_kclasses())
        while len(lst) > 0:
            kwargs, lst = self._kwargs(kwargs, lst)

        return kwargs



class Div(Tag):
    """ A <div> tag.  Default class is `container`. """
    tagname = 'div'

    def __init__(self, *args, fluid=False, **kwargs):
        self.kclass_default = KClassDefault('container')
        if fluid is True:
            self.kclass_default.set('container-fluid')

        super().__init__(*args, **self.update_kwargs(kwargs))

class Ul(Tag):
    """ A <ul> tag.  Makes sure all elements added are wrapped in <li> tag. """
    tagname = 'ul'

    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        self.add(*items)


    def add(self, *items, active=False):
        added = []
        _items = parse_into_single_tuple(items)
        for item in _items:
            _type = getattr(type(item), 'tagname', None)
            if _type is 'li' or isinstance(item, li):
                super().add(item)
                added.append(item)
            else:
                if active is True:
                    element = super().add(li(item, _class='active', style='float:left;'))
                else:
                    element = super().add(li(item, style='float:left;'))
                added.append(element)

        if len(added) == 1:
            return added[0]
        else:
            return tuple(added)
        
class Glyphicon(Tag):
    """ A glyphicon element.

            If this element is called with an href then it returns and <a> tag with
            the appropriate class's, else it defaults to a <span> tag.
    """
    tagname = 'span'


    def __init__(self, *args, icon_name='home', href=None, **kwargs):
        if href is not None:
            self.__class__.tagname = 'a'
            kwargs.update({'href': href})
        else:
            self.__class__.tagname = 'span'
        
        self.kclass_dep = KClassDep('glyphicon')
        self.kclass_default = KClassDefault('glyphicon-{}'.format(icon_name))

        super().__init__(*args, **self.update_kwargs(kwargs))

class DropdownButton(Tag):
    tagname = 'a'

    def __init__(self, text=None, glyph=None, caret=True, **kwargs):
        self.kclass_dep = KClassDep('dropdown-toggle')
        self.kdata_toggle = KDep('dropdown', key='data-toggle')
        self.khref = KDep('#', key='href')
        
        items = span()
        if text is not None:
            items.add(text)
        if glyph is not None:
            if isinstance(glyph, Glyphicon):
                items.add(glyph)
            else:
                items.add(Glyphicon(icon_name=glyph))
        if caret is True:
            items.add(span(_class='caret'))

        super().__init__(items, **self.update_kwargs(kwargs))

class Dropdown(Tag):
    """ A dropdown element. """
    tagname = 'div'

    def __init__(self, *items, li=False, **kwargs):
        # set the tagname for this element
        # li is used when the dropdown menu is in a Navbar.
        if li is True:
             type(self).tagname = 'li'
        else:
            type(self).tagname  = 'div'

        self.kclass_dep = KClassDep('dropdown')

        super().__init__(**self.update_kwargs(kwargs))
        
        # list of the menu items for the dropdown
        # all elements except for the dropdown button, get added to this menu.
        self.menu = super().add(Ul(_class='dropdown-menu'))

        # set up the button
        self.button = None
        # check if a button was passed in at instantiation
        buttons = [button for button in items if isinstance(button, DropdownButton)]
        if len(buttons) == 1:
            # if it was insert it before the menu
            #TODO:  this should be moved so that there to a class method, to aid in adding a
            #       button after instantiation
            self.button = self.children.insert(0, buttons[0])
            # set the items to everything but the button
            items = [item for item in items if item is not buttons[0]]

        #elif len(buttons) > 1:
            # do raise an error or something.
            #pass
        else:
            # add a button if one was not passed in, because what's a dropdown if yout can't
            # open it.
            self.button = self.children.insert(0, DropdownButton())

        # add the rest of the items
        self.add(items)

    def add(self, *items):
        """ Adds items to the menu. """
        return self.menu.add(items)

class TableHeader(Tag):
    """ A table header element. """
    tagname = 'thead'

    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        self.row = super().add(TableRow(items, header=True))

    def add(self, *items):
        """ Adds items to the row.  
            Makes sure items are wrapped in <th> tag.
        """
        return self.row.add(items)

class TableRow(Tag):
    """ A row in a TableHeader or TableBody element. """
    tagname = 'tr'

    def __init__(self, *items, header=False, info=False, success=False, warning=False, \
            danger=False, **kwargs):
        
        # if true then this row is part of a TableHeader element.
        self.header = header

        # sets class args, the success, info... adds highlighed color to the row.
        self.kclass_dep = KClassDep()
        if info is True:
            self.kclass_dep.append('info')
        elif success is True:
            self.kclass_dep.append('success')
        elif warning is True:
            self.kclass_dep.append('warning')
        elif danger is True:
            self.kclass_dep.append('danger')

        super().__init__(**self.update_kwargs(kwargs))
        self.add(items)

    def add(self, *items):
        """ Adds items to the table row, items are wrapped in a <td> tag if self.header is
            False, else they are wrapped in a <th> tag.
        """
        added = []
        items = parse_into_single_tuple(items)
        for item in items:
            if isinstance(item, th) or isinstance(item, td):
                added.append(super().add(item))
            elif self.header is True:
                added.append(super().add(th(item)))
            else:
                added.append(super().add(td(item)))

        if len(added) == 1:
            return added[0]
        else:
            return added
                


class TableBody(Tag):
    """ The body of a table element. """
    tagname = 'tbody'
    
    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        self.add(items)

    def add(self, *items):
        """ Make's sure all items are a TableRow or tr tag. """
        items = parse_into_single_tuple(items)
        error_items = [item for item in items  if not isinstance(item, TableRow)]
        error_items = [item for item in error_items if not isinstance(item, tr)]
        if len(error_items) > 0:
            print('ERROR in table body', error_items, file=sys.stderr)
            # do something with error_items
            items = tuple((item for item in items if item not in error_items))
        return super().add(*items)

class Table(Tag):
    """ The top level table element. """
    tagname = 'table'

    def __init__(self, *items, bordered=False, striped=False, **kwargs):
        self.kclass_deps = KClassDep('table')
        if bordered is True:
            self.kclass_deps.append('table-bordered')
        if striped is True:
            self.kclass_deps.append('table-striped')

        self.body = None
        self.header = None

        super().__init__(**self.update_kwargs(kwargs))
        self.add(items)

    def add(self, *items):
        """ Adds items to the table body. """

        items_lst = list(parse_into_single_tuple(items))

        header_lst = [item for item in items_lst if isinstance(item, TableHeader)]
        #:TODO   maybe move adding header to a class method to make it easier to add a header
        #        after instantiation
        if len(header_lst) == 1:
            self.header = header_lst[0]
            self.children.insert(0, self.header)
            items_lst.remove(header_lst[0])

        body_lst = [body for body in items_lst if isinstance(body, TableBody)]
        if len(body_lst) == 1:
            self.body = super().add(body_lst[0])
            items_lst.remove(body_lst[0])

        if self.body is None:
            self.body = super().add(TableBody())

        return self.body.add(tuple(items_lst))

class ResponsiveTable(Div):
    """ A wrapper to make a table responsive. """
    #:TODO: make an table element that can have responsive as a param.
    
    tagname = 'div'

    def __init__(self, *items, **kwargs):
        self.kclass_dep = KClassDep('table-responsive')
        # when subclassing an element you must call self.update_kwargs or it will not 
        # gaurantee the right kwargs being sent the html_tag instantiation.
        super().__init__(*items, **self.update_kwargs(kwargs))
           

class Button(Tag):
    """ A button element. """
    tagname = 'button'

    def __init__(self, *items, anchor=False, primary=False, success=False, info=False, \
            danger=False, link=False, pull_right=False, **kwargs):

        if anchor is True:
            type(self).tagname = 'a'
        else:
            type(self).tagname = 'button'

        self.kclass_dep = KClassDep('btn')
        self.ktype = KDep('button', key='type')
        self.kclass_default = KClassDefault('btn-default')

        if primary is True:
            self.kclass_default.set('btn-primary')
        elif success is True:
            self.kclass_default.set('btn-success')
        elif info is True:
            self.kclass_default.set('btn-info')
        elif danger is True:
            self.kclass_default.set('btn-danger')
        elif link is True:
            self.kclass_default.set('btn-link')

        if pull_right is True:
            self.kclass_default.append('pull-right')

        super().__init__(*items, **self.update_kwargs(kwargs))


class Small(Tag):
    tagname = 'small'
