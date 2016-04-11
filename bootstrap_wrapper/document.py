"""
    v2.document
    ~~~~~~~~~~~

        Holds our base document template for a bootstrap document. 
"""
from dominate.document import document
from dominate.tags import meta, script, link, div, comment
from markupsafe import Markup

from .navigation import Navbar
from .elements import Div

class Document(document):
    ''' Just passes render through Markup. '''
    def render(self, *args, **kwargs):
        return Markup(super().render(*args, **kwargs))

class BootstrapDocument(Document):
    """ BootstrapDocument.

        Adds bootstrap and jquery to a document, with the option to specify a local
        file system path to load it from or a cdn path.

        The following tags are available to add items to.

        :head:          The head tag of the document.
        :meta:          Stores meta tags inside of the head tag.
        :content:       A <div class='container' id='content'> tag.
                        Calling the add method of a document adds items inside
                        of this tag.
        :body:          The body of the document.
        :scripts:       A <div> below the content, to add <script> tags to.

        :param bootstrap_url:   A cdn url or path to a static folder.
        :param jquery_url:      A cdn url or path to a static folder.
        :param static_folder:   A path in the file system to load from.
    """

    def __init__(self, *args, \
            bootstrap_url='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6', \
            jquery_url='https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js',
            static_folder=None,
            **kwargs):

        super().__init__(**kwargs)
        self.navbar = None

        self.meta = self.head.add(
            meta(
                name='viewport',
                content='width=device-width, initial-scale=1.0'
            )
        )
        self.head.add(comment('Latest compiled and minified CSS'))
        if static_folder is not None:
            bootstrap_url = static_folder

        self.head.add(
            link(
                rel='stylesheet',
                href=bootstrap_url + '/css/bootstrap.min.css'
            ),
        )
        self.content = self.body.add(Div(id='content'))
        self.scripts = self.body.add(Div(id='scripts'))
        self.scripts.add(comment('jQuery library'))

        if static_folder is not None:
            jquery_url = static_folder + '/js/jquery.min.js'

        self.scripts.add(
            script(src=jquery_url)
        )
        self.scripts.add(comment('Latest compiled JavaScript'))
        self.scripts.add(
            script(src=bootstrap_url + '/js/bootstrap.min.js')
        )

        self.add(*args)

    def add(self, *items):
        """ Adds items to the content div by default. """
        # get any navbar items so they can be added before the content
        top_nav = next((item for item in items if isinstance(item, Navbar) \
                and item.top is True), None)

        if top_nav is not None:
            self.body.children.insert(0, top_nav)
            self.navbar = top_nav
            items = list(items)
            items.remove(top_nav)

        return self.content.add(items)

