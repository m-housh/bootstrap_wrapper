"""
    v2.helpers
    ~~~~~~~~~~

"""
class UniqueStrings(list):
    """ Class that stores unique strings in a list. """

    def __init__(self, *items, sort=False):
        self._items = []
        self.append(items)
        self.sort = sort
        
    def clear(self):
        self._items = []
        return self._items

    def append(self, *items):
        def parse_string(string):
            strings = (s for s in string.split() if s not in self._items)
            for string in strings:
                self._items.append(string)

        def parse_iterables(items):
            for item in items:
                if isinstance(item, str):
                    parse_string(item)
                if isinstance(item, tuple) or isinstance(item, list):
                    parse_iterables(item)

        parse_iterables(items)
        return self._items

    def set(self, *items):
        self.clear()
        return self.append(items)

    def __str__(self):
        if self.sort is True:
            return ' '.join(sorted(self._items))
        return ' '.join(self._items)

    def __call__(self):
        return str(self)

class KwContainer:

    def __init__(self, *items, key='', sort=False):
        self.key = key
        self.value = UniqueStrings(*items, sort)

    def append(self, *items):
        return self.value.append(*items)

    def clear(self):
        return self.value.clear()

    def set(self, *items):
        return self.value.set(items)

    def __call__(self):
        if self.value() is not '':
            return {self.key: self.value()}
        return {}

class KDep(KwContainer):

    def __call__(self, kwargs={}):
        try:
            attr = kwargs[self.key]
            self.append(attr)
            kwargs[self.key] = self.value()
            return kwargs
        except:
            s_call = super().__call__()
            kwargs.update(s_call)
            return kwargs


class KDefault(KwContainer):

    def __call__(self, kwargs={}):
        # this seems like a hack, but for some reason using hasattr(kwargs, self.key) does
        # not ever return True
        try:
            attr = kwargs[self.key]
            return kwargs
        except: 
            s_call = super().__call__()
            kwargs.update(s_call)
            return kwargs

class KClassDep(KDep):

    def __init__(self, *items):
        super().__init__(*items, key='_class')

    def __call__(self, kwargs={}):
        try:
            attr = kwargs['cls']
            self.append(attr)
            del kwargs['cls']
            kwargs[self.key] = self.value()
            return kwargs
        except:
            return super().__call__(kwargs)

class KClassDefault(KDefault):

    def __init__(self, *items):
        super().__init__(*items, key='_class')

    def __call__(self, kwargs={}):
        try:
            attr = kwargs['cls']
            self.append(attr)
            del kwargs['cls']
            kwargs[self.key] = self.value()
            return kwargs
        except:
            return super().__call__(kwargs)

class KStyle(KDefault): # styling should never be a dependency

    def __init__(self, *items):
        super().__init__(*items, key='style', sort=False)

def parse_into_single_tuple(items, retval=None):
    """ Parse lists/tuples of lists/tuples into one tuple with all the values. """
    if retval is None:
        retval = []
    for item in items:
        if isinstance(item, list) or isinstance(item, tuple):
            retval = list(parse_into_single_tuple(item, retval))
        else:
            retval.append(item)
    return tuple(retval)
