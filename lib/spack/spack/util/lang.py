##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import sys
import functools
import inspect
from spack.util.filesystem import new_path

# Ignore emacs backups when listing modules
ignore_modules = [r'^\.#', '~$']


def caller_locals():
    """This will return the locals of the *parent* of the caller.
       This allows a fucntion to insert variables into its caller's
       scope.  Yes, this is some black magic, and yes it's useful
       for implementing things like depends_on and provides.
    """
    stack = inspect.stack()
    try:
        return stack[2][0].f_locals
    finally:
        del stack


def get_calling_package_name():
    """Make sure that the caller is a class definition, and return
       the module's name.  This is useful for getting the name of
       spack packages from inside a relation function.
    """
    stack = inspect.stack()
    try:
        # get calling function name (the relation)
        relation = stack[1][3]

        # Make sure locals contain __module__
        caller_locals = stack[2][0].f_locals
    finally:
        del stack

    if not '__module__' in caller_locals:
        raise ScopeError(relation)

    module_name = caller_locals['__module__']
    base_name = module_name.split('.')[-1]
    return base_name


def attr_required(obj, attr_name):
    """Ensure that a class has a required attribute."""
    if not hasattr(obj, attr_name):
        tty.die("No required attribute '%s' in class '%s'"
                % (attr_name, obj.__class__.__name__))


def attr_setdefault(obj, name, value):
    """Like dict.setdefault, but for objects."""
    if not hasattr(obj, name):
        setattr(obj, name, value)
    return getattr(obj, name)


def has_method(cls, name):
    for base in inspect.getmro(cls):
        if base is object:
            continue
        if name in base.__dict__:
            return True
    return False


def memoized(obj):
    """Decorator that caches the results of a function, storing them
       in an attribute of that function."""
    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


def list_modules(directory, **kwargs):
    """Lists all of the modules, excluding __init__.py, in
       a particular directory."""
    list_directories = kwargs.setdefault('directories', True)

    for name in os.listdir(directory):
        if name == '__init__.py':
            continue

        path = new_path(directory, name)
        if list_directories and os.path.isdir(path):
            init_py = new_path(path, '__init__.py')
            if os.path.isfile(init_py):
                yield name

        elif name.endswith('.py'):
            if not any(re.search(pattern, name) for pattern in ignore_modules):
                yield re.sub('.py$', '', name)


def key_ordering(cls):
    """Decorates a class with extra methods that implement rich comparison
       operations and __hash__.  The decorator assumes that the class
       implements a function called _cmp_key().  The rich comparison operations
       will compare objects using this key, and the __hash__ function will
       return the hash of this key.

       If a class already has __eq__, __ne__, __lt__, __le__, __gt__, or __ge__
       defined, this decorator will overwrite them.  If the class does not
       have a _cmp_key method, then this will raise a TypeError.
    """
    def setter(name, value):
        value.__name__ = name
        setattr(cls, name, value)

    if not has_method(cls, '_cmp_key'):
        raise TypeError("'%s' doesn't define _cmp_key()." % cls.__name__)

    setter('__eq__', lambda s,o: o is not None and s._cmp_key() == o._cmp_key())
    setter('__lt__', lambda s,o: o is not None and s._cmp_key() <  o._cmp_key())
    setter('__le__', lambda s,o: o is not None and s._cmp_key() <= o._cmp_key())

    setter('__ne__', lambda s,o: o is None or s._cmp_key() != o._cmp_key())
    setter('__gt__', lambda s,o: o is None or s._cmp_key() >  o._cmp_key())
    setter('__ge__', lambda s,o: o is None or s._cmp_key() >= o._cmp_key())

    setter('__hash__', lambda self: hash(self._cmp_key()))

    return cls


@key_ordering
class HashableMap(dict):
    """This is a hashable, comparable dictionary.  Hash is performed on
       a tuple of the values in the dictionary."""
    def _cmp_key(self):
        return tuple(sorted(self.values()))


    def copy(self):
        """Type-agnostic clone method.  Preserves subclass type."""
        # Construct a new dict of my type
        T = type(self)
        clone = T()

        # Copy everything from this dict into it.
        for key in self:
            clone[key] = self[key].copy()
        return clone


def in_function(function_name):
    """True if the caller was called from some function with
       the supplied Name, False otherwise."""
    stack = inspect.stack()
    try:
        for elt in stack[2:]:
            if elt[3] == function_name:
                return True
        return False
    finally:
        del stack
