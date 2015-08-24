# Need this because of spack.util.string
from __future__ import absolute_import
import string
import itertools
import re

import spack

__all__ = ['mod_to_class', 'spack_module_to_python_module', 'valid_module_name',
           'validate_module_name', 'possible_spack_module_names']

# Valid module names can contain '-' but can't start with it.
_valid_module_re = r'^\w[\w-]*$'


def mod_to_class(mod_name):
    """Convert a name from module style to class name style.  Spack mostly
       follows `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_:

          * Module and package names use lowercase_with_underscores.
          * Class names use the CapWords convention.

       Regular source code follows these convetions.  Spack is a bit
       more liberal with its Package names nad Compiler names:

          * They can contain '-' as well as '_', but cannot start with '-'.
          * They can start with numbers, e.g. "3proxy".

       This function converts from the module convention to the class
       convention by removing _ and - and converting surrounding
       lowercase text to CapWords.  If mod_name starts with a number,
       the class name returned will be prepended with '_' to make a
       valid Python identifier.
    """
    validate_module_name(mod_name)

    class_name = re.sub(r'[-_]+', '-', mod_name)
    class_name = string.capwords(class_name, '-')
    class_name = class_name.replace('-', '')

    # If a class starts with a number, prefix it with Number_ to make it a valid
    # Python class name.
    if re.match(r'^[0-9]', class_name):
        class_name = "_%s" % class_name

    return class_name


def spack_module_to_python_module(mod_name):
    """Given a Spack module name, returns the name by which it can be
       imported in Python.
    """
    if re.match(r'[0-9]', mod_name):
        mod_name = 'num' + mod_name

    return mod_name.replace('-', '_')


def possible_spack_module_names(python_mod_name):
    """Given a Python module name, return a list of all possible spack module
       names that could correspond to it."""
    mod_name = re.sub(r'^num(\d)', r'\1', python_mod_name)

    parts = re.split(r'(_)', mod_name)
    options = [['_', '-']] * mod_name.count('_')

    results = []
    for subs in itertools.product(*options):
        s = list(parts)
        s[1::2] = subs
        results.append(''.join(s))

    return results


def valid_module_name(mod_name):
    """Return whether the mod_name is valid for use in Spack."""
    return bool(re.match(_valid_module_re, mod_name))


def validate_module_name(mod_name):
    """Raise an exception if mod_name is not valid."""
    if not valid_module_name(mod_name):
        raise InvalidModuleNameError(mod_name)


class InvalidModuleNameError(spack.error.SpackError):
    """Raised when we encounter a bad module name."""
    def __init__(self, name):
        super(InvalidModuleNameError, self).__init__(
            "Invalid module name: " + name)
        self.name = name
