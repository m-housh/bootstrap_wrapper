from markupsafe import Markup
from itertools import chain
from functools import reduce
from dominate.tags import *
from bootstrap_wrapper.helpers import KDep, KDefault, KClassDep, KClassDefault, KwContainer

class Meta(type):
    tagname = None

class Tag(html_tag, metaclass=Meta):

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
    tagname = 'div'


    def __init__(self, *args, **kwargs):
        self.kclass_default = KClassDefault('container')
        self.kdep = KDep('a', key='style')
        super().__init__(*args, **kwargs)

class FDiv(Div):
    def __init__(self, *args, **kwargs):
        self.kclass_default = KClassDefault('container-fluid')
        super().__init__(*args, **self.update_kwargs(kwargs))

class A(Tag):
    tagname = 'a'


if __name__ == '__main__':
    print('play.py\n\n\n')

    print(Div())
    #print(Div(style='another'))
    print(FDiv())
    print(FDiv(style='b'))
    #print(A())

