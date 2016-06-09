from unittest import TestCase
from dominate.tags import *
from dominate.document import document

from bootstrap_wrapper.document import *


def bootstrapDoc(): #{{{
    doc = document(title='My Title')
    doc.head.add(meta(name="viewport", content="width=device-width, initial-scale=1.0"))
    doc.head.add(comment('Latest compiled and minified CSS'))
    doc.head.add(link(rel="stylesheet", href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"))
    content = doc.body.add(div(_class="container", id="content"))
    scripts = doc.body.add(div(_class='container', id="scripts"))
    scripts.add(comment('jQuery library'))
    scripts.add(script(src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js'))
    scripts.add(comment('Latest compiled JavaScript'))
    scripts.add(script(src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js'))


    return doc
#}}}

class BootstrapDocumentTestCase(TestCase):

    def test_bootstrap_document_should_have_correct_elements(self):
        b = BootstrapDocument(title='My Title')
        tv = bootstrapDoc()
        self.assertEqual(b.render(), tv.render())

    def test_items_get_added_to_body_content_container(self):
        b = BootstrapDocument(title='My Title')
        b.add(h1('My Header'))

        tv = bootstrapDoc()
        content = tv.get(tag='div', id='content')[0]
        content.add(h1('My Header'))

        self.assertEqual(b.render(), tv.render())

    def test_navbar_gets_added_above_body_content_tag(self):
        b = BootstrapDocument(title='My Title')
        b.add(Navbar(top=True))

        tv = bootstrapDoc()
        tv.body.children.insert(0, nav(div(_class='container-fluid'), _class='navbar navbar-default'))
        self.assertEqual(b.render(), tv.render())

    def test_static_paths(self):
        b = BootstrapDocument(static_folder='/static')
        scripts = div(_class='container', id='scripts')
        scripts.add(comment('jQuery library'))
        scripts.add(script(src='/static/js/jquery.min.js'))
        scripts.add(comment('Latest compiled JavaScript'))
        scripts.add(script(src='/static/js/bootstrap.min.js'))

        self.assertEqual(b.scripts.render(), scripts.render())
