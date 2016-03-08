from unittest import TestCase
from dominate.tags import *
from wtforms import Form as _WForm
from wtforms.fields import *

from bootstrap_wrapper.forms import *

class FormsTestCase(TestCase):

    def test_form_group_tag(self): #{{{
        class F(_WForm):
            name = StringField('Name')

        for field in F():
            f = FormGroup(field=field)
            tv = div(raw(str(field.label)), br(), raw(str(field(class_='form-control'))), _class='form-group')

        self.assertEqual(f.render(), tv.render())
#}}}
    def test_quick_form(self): #{{{
        class F(_WForm):
            name = StringField('Name')
            email = StringField('Email')
            submit = SubmitField()

        f = QuickForm(F())

        tv = form(
                div(
                    label('Name', _for='name'),
                    br(),
                    input(type='text',_class='form-control', id='name', name='name', value=''),
                    _class='form-group',
                ),
                div(
                    label('Email', _for='email'),
                    br(),
                    input(type='text', _class='form-control', id='email', name='email', value=''),
                    _class='form-group'
                ),
                input(
                    _class="btn btn-primary",
                    id="submit",
                    name="submit",
                    type="submit",
                    value="Submit"
                ),
                method='POST',
                role='form'
        )
        
        # must be rendered inline for tests because of adding field's as raw tags inside
        # our WTForm tag doesn't add the same newlines and tabs
        self.assertEqual(f.render(inline=True), tv.render(inline=True))

        f = QuickForm(F(), pull_right=True)
        tv = form(
                div(
                    label('Name', _for='name'),
                    br(),
                    input(type='text',_class='form-control', id='name', name='name', value=''),
                    _class='form-group',
                ),
                div(
                    label('Email', _for='email'),
                    br(),
                    input(type='text', _class='form-control', id='email', name='email', value=''),
                    _class='form-group'
                ),
                input(
                    _class="btn btn-primary pull-right",
                    id="submit",
                    name="submit",
                    type="submit",
                    value="Submit"
                ),
                method='POST',
                role='form'
        )
#}}}
    def test_form_field(self): #{{{
        f = FormField('text', 'name', place_holder='Enter Your Name')
        tv = input(type='text', id='name', placeholder='Enter Your Name', _class='form-control')
        self.assertEqual(f.render(), tv.render())
#}}}
    def test_bootstrap_form_tag(self): #{{{
        f = BootstrapForm()
        tv = form(method='POST', role='form')
        self.assertEqual(f.render(), tv.render())
#}}}


