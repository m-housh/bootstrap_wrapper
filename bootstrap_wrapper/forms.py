"""
    v2.forms
    ~~~~~~~

        Holds form elements.
"""
from dominate.util import raw
from dominate.tags import br

from .helpers import KDep, KClassDep, KDefault, KClassDefault
from .elements import Tag


class BootstrapForm(Tag):
    """ Top level form element. """
    tagname = 'form'

    def __init__(self, *items, action=None, method='POST', **kwargs):
        self.kaction = KDefault(key='action')
        if action is not None:
            self.kaction.append(action)

        self.kmethod = KDefault(method, key='method')
        self.krole = KDep('form', key='role')

        super().__init__(*items, **self.update_kwargs(kwargs))
