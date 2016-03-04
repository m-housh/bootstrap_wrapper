"""
    v2.elements
    ~~~~~~~~~~~
"""
from markupsafe import Markup
from dominate.tags import html_tag, div

from .helpers import KClass, KwContainer

class ElementMeta(type):
    """ Adds tagname override to our elements. """
    tagname = None


class Element(html_tag, metaclass=ElementMeta):
    """ Our base class for all of our tags. """

    def render(self, *args, **kwargs):
        """ runs render through markupsafes Markup. """
        return Markup(super().render(*args, **kwargs))


class Div(Element, div):
    tagname = 'div'

    def __init__(self, *args, fluid=False, **kwargs):
        kclass_dep = KClass()
        if fluid is True:
            kclass_dep.append('container-fluid')
        else:
            kclass_dep.append('container')

        _class = kwargs.pop('_class', None) or kwargs.pop('cls', None)
        if _class is not None:
            kclass_dep.append(_class)

        kwargs.update(kclass_dep())

        super().__init__(*args, **kwargs)


