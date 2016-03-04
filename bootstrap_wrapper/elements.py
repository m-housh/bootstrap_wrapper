"""
    v2.elements
    ~~~~~~~~~~~
"""
from markupsafe import Markup
from dominate.tags import html_tag, div, li

from .helpers import KClassDep, parse_into_single_tuple

class ElementMeta(type):
    """ Adds tagname override to our elements. """
    tagname = None


class Element(html_tag, metaclass=ElementMeta):
    """ Our base class for all of our tags. """

    def render(self, *args, **kwargs):
        """ runs render through markupsafes Markup. """
        return Markup(super().render(*args, **kwargs))


class Div(Element):
    """ A <div> tag.  Default class is `container`. """
    tagname = 'div'

    def __init__(self, *args, fluid=False, **kwargs):
        print('Div init')
        print('kwargs', kwargs)
        kclass_dep = KClassDep()
        if fluid is True:
            kclass_dep.append('container-fluid')
        else:
            kclass_dep.append('container')

        super().__init__(*args, **kclass_dep(kwargs))

class Ul(Element):
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
                print('item is li')
                super().add(item)
                added.append(item)
            else:
                print('item is not li')
                if active is True:
                    element = super().add(li(item, _class='active'))
                else:
                    element = super().add(li(item))
                added.append(element)

        if len(added) == 1:
            return added[0]
        else:
            return tuple(added)
        
class Glyphicon(Element):
    """ A glyphicon element.

            If this element is called with an href then it returns and <a> tag with
            the appropriate class's, else it defaults to a <span> tag.
    """
    tagname = 'span'

    def __init__(self, *args, icon_name='home', href=None, **kwargs):
        if href is not None:
            self.__class__.tagname = 'a'
            kwargs.update({'href': href})

        kclass = KClassDep('glyphicon', 'glyphicon-{}'.format(icon_name))
        super().__init__(*args, **kclass(kwargs))

