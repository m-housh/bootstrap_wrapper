"""
    v2.forms
    ~~~~~~~

        Holds form elements.
"""
from dominate.util import raw
from dominate.tags import br, p, div
from wtforms.fields import SubmitField

from .helpers import KDep, KClassDep, KDefault, KClassDefault
from .elements import Tag, Div


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


class QuickForm(BootstrapForm):
    """ A helper to render a WTForms Form. """
    
    def __init__(self, form=None, pull_right=False, **kwargs):

        super().__init__(**kwargs)

        self.form = form
        self.pull_right = pull_right

        if self.form is not None:
            try:
                self.add(raw(form.hidden_tag()))
            except:
                pass

            for field in self.form:
                if field.widget.input_type is not 'hidden' and \
                        field.widget.input_type is not 'submit':
                    self.add(FormGroup(field=field))

                elif field.widget.input_type is 'submit':
                    button_class = 'btn btn-primary'
                    if self.pull_right is True:
                        button_class += ' pull-right'
                    self.add(raw(field(class_=button_class)))

class FormRow(Div):
    """ Allows the creation of row with form fields inline with labels above them. """

    def __init__(self, *fields, col_args=None, **kwargs):
        self.kclass_dep = KClassDep('row')
        super().__init__(**self.update_kwargs(kwargs))

        def _col(n):
            return 'col-sm-{}'.format(n)
        
        count = 0
        while count < len(fields):
            _kwargs = {}
            if count < len(col_args):
                _kwargs['_class'] = _col(col_args[count])

            _kwargs['style'] = 'float:left;'

            field = fields[count]
            if isinstance(field, SubmitField):
                _kwargs['style'] += 'padding-top:25px;'
                self.add(div(raw(field(class_='btn btn-primary')), **_kwargs))
            else:
                self.add(FormGroup(field=field, **_kwargs))
            count += 1

                
        


class FormGroup(Div):
    """ A Form Group holds a label, field, and any errors associated with a field.
        This is primarily used with a WTForm field.
    """

    def __init__(self, *args, field=None, **kwargs):
        self.kclass_dep = KClassDep('form-group')
        if field is not None:
            if field.errors:
                self.kclass_dep.append('has-error')
            if field.flags.required:
                self.kclass_dep.append('required')

        super().__init__(**self.update_kwargs(kwargs))

        if field is not None:
            self.add(
                raw(str(field.label)),
                br(),
                raw(field(class_='form-control')),
            )

            if field.errors:
                for error in field.errors:
                    self.add(p(error, _class='help-block'))

        # should check/do something with *args, but not sure what at the moment,
        # possibly just remove the possibility to pass args in, and make this
        # an element only responsible for WTForm field's.


class FormField(Tag):
    """ A basic form field. """
    tagname = 'input'
    is_single = True

    def __init__(self, type, id, place_holder=None, **kwargs):

        self.kclass_dep = KClassDep('form-control')
        self.ktype = KDep(type, key='type')
        self.kid = KDep(id, key='id')

        self.kplace_holder = KDefault(key='placeholder')
        if place_holder is not None:
            self.kplace_holder.append(place_holder)

        super().__init__(**self.update_kwargs(kwargs))
                    
