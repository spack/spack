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
import inspect
import collections
import functools


def composite(interface=None, method_list=None, container=list):
    """Decorator implementing the GoF composite pattern.

    Args:
        interface (type): class exposing the interface to which the
            composite object must conform. Only non-private and
            non-special methods will be taken into account
        method_list (list of str): names of methods that should be part
            of the composite
        container (MutableSequence): container for the composite object
            (default = list).  Must fulfill the MutableSequence
            contract. The composite class will expose the container API
            to manage object composition

    Returns:
        a class decorator that patches a class adding all the methods
        it needs to be a composite for a given interface.

    """
    # Check if container fulfills the MutableSequence contract and raise an
    # exception if it doesn't. The patched class returned by the decorator will
    # inherit from the container class to expose the interface needed to manage
    # objects composition
    if not issubclass(container, collections.MutableSequence):
        raise TypeError("Container must fulfill the MutableSequence contract")

    # Check if at least one of the 'interface' or the 'method_list' arguments
    # are defined
    if interface is None and method_list is None:
        raise TypeError(
            "Either 'interface' or 'method_list' must be defined on a call "
            "to composite")

    def cls_decorator(cls):
        # Retrieve the base class of the composite. Inspect its methods and
        # decide which ones will be overridden
        def no_special_no_private(x):
            return callable(x) and not x.__name__.startswith('_')

        # Patch the behavior of each of the methods in the previous list.
        # This is done associating an instance of the descriptor below to
        # any method that needs to be patched.
        class IterateOver(object):
            """Decorator used to patch methods in a composite.

            It iterates over all the items in the instance containing the
            associated attribute and calls for each of them an attribute
            with the same name
            """

            def __init__(self, name, func=None):
                self.name = name
                self.func = func

            def __get__(self, instance, owner):
                def getter(*args, **kwargs):
                    for item in instance:
                        getattr(item, self.name)(*args, **kwargs)
                # If we are using this descriptor to wrap a method from an
                # interface, then we must conditionally use the
                # `functools.wraps` decorator to set the appropriate fields
                if self.func is not None:
                    getter = functools.wraps(self.func)(getter)
                return getter

        dictionary_for_type_call = {}

        # Construct a dictionary with the methods explicitly passed as name
        if method_list is not None:
            dictionary_for_type_call.update(
                (name, IterateOver(name)) for name in method_list)

        # Construct a dictionary with the methods inspected from the interface
        if interface is not None:
            dictionary_for_type_call.update(
                (name, IterateOver(name, method))
                for name, method in inspect.getmembers(
                    interface, predicate=no_special_no_private))

        # Get the methods that are defined in the scope of the composite
        # class and override any previous definition
        dictionary_for_type_call.update(
            (name, method) for name, method in inspect.getmembers(
                cls, predicate=inspect.ismethod))

        # Generate the new class on the fly and return it
        # FIXME : inherit from interface if we start to use ABC classes?
        wrapper_class = type(cls.__name__, (cls, container),
                             dictionary_for_type_call)
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
