from markupsafe import Markup
from dominate.tags import *
from bootstrap_wrapper.helpers import KDep, KDefault, KClassDep

class Meta(type):
    tagname = None

class Element(html_tag, metaclass=Meta):


    def _get_instances_of(self, kclass):
        # get instances from class
        instances = tuple(item for item in self.__class__.__dict__.values() \
                if isinstance(item, kclass))
        # get instances from instance
        instances += tuple(item for item in self.__dict__.values() \
                if isinstance(item, kclass))

        return instances

    def _clean_key_and_value_for(self, kclass):
        # returns a cleaned key and the value of self.attributes for that key
        key = html_tag.clean_attribute(kclass.key)
        return (key, getattr(self, key, None))

    
    def update_attributes(self):

        defaults = self._get_instances_of(KDefault)
        for default in defaults:
            key, value = self._clean_key_and_value_for(default)
            if value is None:
                self.attributes[key] = default.value()

        deps = self._get_instances_of(KDep)
        for dep in deps:
            key, value = self._clean_key_and_value_for(dep)
            if value is not None:
                dep.append(value)

            self.attributes[key] = dep.value()


        

    def render(self, *args, **kwargs):
        """ Responsible for updating attributes on an instance before we call, super().render. """
        # call defaults first, as they are skipped if there is a value for the key.
        self.update_attributes()
        return super().render(*args, **kwargs)




if __name__ == '__main__':
    print('play.py\n\n\n')


