"""
    v2.navigation
    ~~~~~~~~~~~~

        Holds elements for our navigation classes. (Tabbar and Navbar)
"""
from dominate.tags import comment

from .helpers import KClassDep, KClassDefault, KDep, KDefault, KStyle, \
        parse_into_single_tuple
from .elements import Tag, Ul, Dropdown, Div, Button

class Tabbar(Div):
    """ Our top level tabbar element. """

    def __init__(self, *items, pills=False, **kwargs):
        super().__init__(fluid=True, **kwargs)
        self.tabs = super().add(TabbarUl(pills=pills))
        self.content = super().add(TabContent())
        if len(items) > 0:
            self.add(items)

    def add(self, *items):
        items = parse_into_single_tuple(items)

        # store tabs and content that's been added
        tabs_added = []
        content_added = []

        # seperate :class: Tab, which is the preferred way to add content.
        tabs = tuple(item for item in items if isinstance(item, Tab))
        # seperate :class: TabbarTab (only has content relevent to the tab button, no content)
        tabbar_tabs = tuple(item for item in items if isinstance(item, TabbarTab))
        # this is what's left over
        panes = tuple(item for item in items if isinstance(item, TabPane))
        # catchall for everything left-over
        items = tuple(item for item in items if item not in tabs \
                and item not in tabbar_tabs and item not in panes)

        # add loosely passed tabbar_tabs and items that are :class: TabPane
        if len(tabbar_tabs) > 0:
            tabs_added = list(self.tabs.add(tabbar_tabs))
        if len(panes) > 0:
            content_added = list(self.content.add(panes))

        if len(tabs) > 0:
            for item in tabs:
                tabs_added.append(self.tabs.add(item.tab, active=item.active))
                content_added.append(self.content.add(item.content))

        if len(items) > 0:
            string = ' '.join(items)
            self.content.add(comment('These items are not of the correct class to add to the tabbar: ' + string))

        if len(tabs_added) > 0 and len(content_added) > 0:
            return (tuple(tabs_added), tuple(content_added))
        elif len(tabs_added) > 0:
            return (tuple(tabs_added), None)
        elif len(content_added) > 0:
            return (None, tuple(content_added))
        return


class Tab:
    """ A convenience object to instantiate a tab with it's content together. """
    
    def __init__(self, text, content=None, content_kwargs={}, href=None, \
            pills=False, active=False, **kwargs):

        self.active = active
        if href is None:
            href = text.lower()

        self.tab = TabbarTab(text, href, pills, **kwargs)
        self.content = TabPane(content, id=href, active=active, **content_kwargs)


class TabbarTab(Button):
    """ The tabs/pills of a tabbar.
        This item will probably not be used directly too often, you should use one of 
        the convenience method to create a tab with it's content.
    """
    def __init__(self, text, href, pills=False, **kwargs):
        self.kdata_toggle = KDep('tab', key='data_toggle')
        if pills is True:
            self.kdata_toggle.set('pill')

        self.khref = KDep('#{}'.format(href.lower()), key='href')

        super().__init__(text, anchor=True, link=True, **self.update_kwargs(kwargs))

class TabContent(Div):
    """ Container that holds all the content for all the tabs of the tabbar. Each tab
        should have a TabPane that gets added to the class, where the TabPane is the actual
        content for a particular tab.
    """

    def __init__(self, *items, **kwargs):
        self.kclass_dep = KClassDep('tab-content')
        super().__init__(*items, **self.update_kwargs(kwargs))

class TabPane(Div):
    """ The actual content for a particular tab. """

    def __init__(self, *items, id='', active=False, fade=True, **kwargs):
        self.kclass_dep = KClassDep('tab-pane')
        self.kstyle = KStyle('border:solid 1px grey;')
        self.kclass_default = KClassDefault('fade')
        if fade is False:
            self.kclass_default.clear()
        elif active is True:
            self.kclass_default.append('in', 'active')

        self.kid = KDep(id, key='id')

        super().__init__(*items, **self.update_kwargs(kwargs))

class TabbarUl(Ul):
    """ A <ul> element that holds the tabs for our tabbar.
        This element will not be used directly too often, you should
        use one of the convience methods to add items to the tabbar.
    """
    def __init__(self, *items, pills=False, **kwargs):
        self.kclass_dep = KClassDep('nav')
        self.kclass_default = KClassDefault('nav-tabs')
        if pills is True:
            self.kclass_default.set('nav-pills')

        super().__init__(**self.update_kwargs(kwargs))
        self.add(items)

    def add(self, *items, active=False):
        added = []
        items = parse_into_single_tuple(items)

        # seperate any tab elements from non-tab elements
        # hopefully all items are tab elements.
        tabs = tuple(item for item in items if isinstance(item, TabbarTab))
        items = tuple(item for item in items if item not in tabs)
        
        if len(items) > 0:
            string = ' '.join(items)
            super().add(comment('These items could not be added to TabbarUl because they are not of class TabbarTab: ' + string))
            
        # super().add() takes care of wrapping the element in an <li> tag
        _tabs = tuple(super().add(tabs, active=active))
        # combine all element we've added
        _tabs += tuple(added)
        if len(_tabs) == 1:
            return _tabs[0]
        elif len(tabs) > 1:
            return _tabs
        return
