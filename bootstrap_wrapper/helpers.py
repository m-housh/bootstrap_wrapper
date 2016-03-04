"""
    v2.helpers
    ~~~~~~~~~~

"""
class UniqueStrings(list):
    """ Class that stores unique strings in a list. """

    def __init__(self, *items):
        self._items = []
        self.append(items)
        
   
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

    def __str__(self):
        return ' '.join(sorted(self._items))

    def __call__(self):
        return str(self)

class KwContainer:

    def __init__(self, *items, key=''):
        self.key = key
        self.value = UniqueStrings(*items)

    def append(self, *items):
        return self.value.append(*items)

    def __call__(self):
        return {self.key: self.value()}

class KClass(KwContainer):

    def __init__(self, *items):
        super().__init__(*items, key='_class')
