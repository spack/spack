##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from __future__ import absolute_import, print_function

import functools
import inspect
import re

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

import six


_IS_SPECIAL_PATTERN = re.compile('__[^_]+__')


def is_special(item):
    """Returns True if the item is a special function or method,
    False otherwise.

    Args:
        item: item to be inspected

    Returns:
        True or False
    """
    # TODO : this matches any __<name>__ not only special methods
    name = getattr(item, '__name__')
    if _IS_SPECIAL_PATTERN.match(name):
        return True
    return False


def is_private(item):
    """Returns True if the item is 'private', False otherwise.

    Args:
        item: item to be inspected

    Returns:
        True or False
    """
    name = getattr(item, '__name__')
    if name.startswith('_') and not is_special(item):
        return True
    return False


class _CompositeContainer(MutableSequence):
    """Container used for the composite implementation.

    This container is basically a list that permits to append items with a
    name, and retrieve them by name. It doesn't permit to set them by name.
    """

    def __init__(self):
        super(_CompositeContainer, self).__init__()
        self._items = []
        self._named_items = {}

    def append(self, value, name=None):
        """Append an item to the container. If it has a name store it to
        permit also a look-up by name.

        Args:
           value: value to be appended
           name (str): name to be associated with the value (optional)
        """
        if name is not None:
            self._named_items[name] = value
        super(_CompositeContainer, self).append(value)

    def __contains__(self, item):
        """Try to look-up by name first, delegate to list later."""
        if item in self._named_items:
            return self._named_items[item]

        return super(_CompositeContainer, self).__contains__(item)

    def __getitem__(self, item):
        # If item is a string, return whatever the lookup by name gives
        if isinstance(item, six.string_types):
            return self._named_items[item]

        # Otherwise delegate to list
        return self._items[item]

    def _cleanup_named_items(self):
        self._named_items = dict(
            [(k, v) for k, v in self._named_items.items() if v in self._items]
        )

    def __setitem__(self, key, value):
        # Delegate to list for setting
        self._items[key] = value

        # Cleanup the dictionary appropriately
        self._cleanup_named_items()

    def __delitem__(self, key):
        # Delegate to list for deletion
        del self._items[key]

        # Cleanup the dictionary appropriately
        self._cleanup_named_items()

    def __len__(self):
        return len(self._items)

    def insert(self, index, value):
        self._items.insert(index, value)


def composite(interface=None, method_list=None, reductions=None):
    """Class decorator that patches a class adding all the methods
    it needs to be a composite over a given interface.

    Args:
        interface (type): class exposing the interface to which the
            composite object must conform. Only non-private and
            non-special methods will be taken into account
        method_list (list of str): names of methods that should be part
            of the composite

        reductions (dict): dictionary that maps method names to reduction
            function

    Returns:
        class decorator
    """
    # Check if at least one of the 'interface' or the 'method_list'
    # arguments are defined
    if interface is None and method_list is None:
        raise TypeError("Either 'interface' or 'method_list' must be defined")

    if reductions is not None and not isinstance(reductions, dict):
        raise TypeError("'reduction' should be a dictionary")

    def cls_decorator(cls):
        # Retrieve the base class of the composite. Inspect its methods and
        # decide which ones will be overridden.
        def no_special_no_private(mthd):
            # Here we have a nasty difference between python 2 and python 3.
            # In python 2 x is considered to be an unbound method
            # when coming from a class
            # (ismethod(x) == True, isfunction(x) == False)
            # In python 3 x is considered just a function
            # when coming from a class
            # (ismethod(x) == False, isfunction(x) == True)
            return not is_special(mthd) and not is_private(mthd)

        # Patch the behavior of each of the methods in the previous list.
        # This is done associating an instance of the descriptor below to
        # any method that needs to be patched.
        class IterateOver(object):
            """Descriptor used to patch methods in a composite.

            It iterates over all the items in the instance containing the
            associated attribute and calls for each of them an attribute
            with the same name.
            """

            def __init__(self, name, func=None, reductions=reductions):
                self.name = name
                self.func = func
                self.reductions = reductions if reductions is not None else {}

            def __get__(self, instance, owner):
                reduction_function = self.reductions.get(self.name, None)

                def getter(*args, **kwargs):
                    for item in instance:
                        value = getattr(item, self.name)(*args, **kwargs)
                        if reduction_function is not None:
                            value = reduction_function(value)
                    return value

                # If we are using this descriptor to wrap a method from
                # an interface, then we must conditionally use the
                # `functools.wraps` decorator to set the appropriate fields.
                if self.func is not None:
                    getter = functools.wraps(self.func)(getter)
                return getter

        dictionary_for_type_call = {}
        # Construct a dictionary with the methods explicitly passed as names
        if method_list is not None:
            method_list_dict = {}
            for name in method_list:
                method_list_dict[name] = IterateOver(name)
            dictionary_for_type_call.update(method_list_dict)

        # Construct a dictionary with the methods inspected from the interface
        bases = (cls, _CompositeContainer)
        if interface is not None:
            # If an interface is passed, class methods and static methods
            # should not be inserted in the list of methods to be wrapped
            interface_methods = inspect.classify_class_attrs(interface)
            interface_methods = [
                x for x in interface_methods if x.kind == 'method'
            ]
            interface_methods = [
                x for x in interface_methods if no_special_no_private(x.object)
            ]

            interface_methods_dict = dict(
                (item.name, IterateOver(item.name, item.object))
                for item in interface_methods
            )
            dictionary_for_type_call.update(interface_methods_dict)
            bases = (cls, interface, _CompositeContainer)

        # Generate the new class on the fly and return it
        wrapper_class = type(cls.__name__, bases, dictionary_for_type_call)

        return wrapper_class

    return cls_decorator


class Bunch(object):
    """Carries a bunch of named attributes (from Alex Martelli bunch)"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Args(Bunch):
    """Subclass of Bunch to write argparse args more naturally."""
    def __init__(self, *flags, **kwargs):
        super(Args, self).__init__(flags=tuple(flags), kwargs=kwargs)
