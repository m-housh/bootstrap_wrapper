from markupsafe import Markup
from functools import reduce
from dominate.tags import *
from bootstrap_wrapper.helpers import KDep, KDefault, KClassDep, KwContainer

class Meta(type):
    tagname = None

class Element(html_tag, metaclass=Meta):

    def __init__(self, *args, **kwargs):
        print('element init')
        super().__init__(*args, **self.update_kwargs(kwargs))


    def _get_instances_of(self, kclass):
        # get instances from class
        instances = tuple(item for item in self.__class__.__dict__.values() \
                if isinstance(item, kclass))
        # get instances from instance
        instances += tuple(item for item in self.__dict__.values() \
                if isinstance(item, kclass))

        return instances
   
    def update_kwargs(self, kwargs):
        # defaults need to go first, because they don't get applied if there is a value
        # passed in kwargs
        defaults = self._get_instances_of(KDefault)
        for default in defaults:
            if not hasattr(kwargs, default.key): 
                kwargs = default(kwargs)
        
        deps = self._get_instances_of(KDep)
        for dep in deps:
            kwargs = dep(kwargs)
           
        
        return kwargs

class Tag(html_tag, metaclass=Meta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **self.kwargs(kwargs))
    
    def _get_kclasses(self):
        for item in self.__dict__.values():
            if isinstance(item, KwContainer):
                yield item
        for item in self.__class__.__dict__.values():
            if isinstance(item, KwContainer):
                yield item

    def kwargs(self, kwargs):
        return list(map(lambda x: x(kwargs), self._get_kclasses())).pop()


class Div(Element):
    tagname = 'div'

    kclass_dep = KClassDep('container')
    kstyle = KDefault('border:solid 1px grey;', key='style', sort=False)

class FDiv(Tag):
    tagname = 'div'
    kclass_dep = KClassDep('container-fluid')
    kdep = KDep('a', key='style')
    kstyle = KDefault('border:solid 1px grey;', key='style', sort=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    print('play.py\n\n\n')

    print(Div())
    print(Div(style='another'))
    print(FDiv())
    print(FDiv(style='b'))

