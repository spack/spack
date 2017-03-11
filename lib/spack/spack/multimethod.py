##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""This module contains utilities for using multi-methods in
spack. You can think of multi-methods like overloaded methods --
they're methods with the same name, and we need to select a version
of the method based on some criteria.  e.g., for overloaded
methods, you would select a version of the method to call based on
the types of its arguments.

In spack, multi-methods are used to ease the life of package
authors.  They allow methods like install() (or other methods
called by install()) to declare multiple versions to be called when
the package is instantiated with different specs.  e.g., if the
package is built with OpenMPI on x86_64,, you might want to call a
different install method than if it was built for mpich2 on
BlueGene/Q.  Likewise, you might want to do a different type of
install for different versions of the package.

Multi-methods provide a simple decorator-based syntax for this that
avoids overly complicated rat nests of if statements.  Obviously,
depending on the scenario, regular old conditionals might be clearer,
so package authors should use their judgement.
"""
import functools

from llnl.util.lang import *

import spack.architecture
import spack.error
from spack.spec import parse_anonymous_spec


class SpecMultiMethod(object):
    """This implements a multi-method for Spack specs.  Packages are
       instantiated with a particular spec, and you may want to
       execute different versions of methods based on what the spec
       looks like.  For example, you might want to call a different
       version of install() for one platform than you call on another.

       The SpecMultiMethod class implements a callable object that
       handles method dispatch.  When it is called, it looks through
       registered methods and their associated specs, and it tries
       to find one that matches the package's spec.  If it finds one
       (and only one), it will call that method.

       The package author is responsible for ensuring that only one
       condition on multi-methods ever evaluates to true.  If
       multiple methods evaluate to true, this will raise an
       exception.

       This is intended for use with decorators (see below).  The
       decorator (see docs below) creates SpecMultiMethods and
       registers method versions with them.

       To register a method, you can do something like this:
           mm = SpecMultiMethod()
           mm.register("^chaos_5_x86_64_ib", some_method)

       The object registered needs to be a Spec or some string that
       will parse to be a valid spec.

       When the mm is actually called, it selects a version of the
       method to call based on the sys_type of the object it is
       called on.

       See the docs for decorators below for more details.
    """

    def __init__(self, default=None):
        self.method_list = []
        self.default = default
        if default:
            functools.update_wrapper(self, default)

    def register(self, spec, method):
        """Register a version of a method for a particular sys_type."""
        self.method_list.append((spec, method))

        if not hasattr(self, '__name__'):
            functools.update_wrapper(self, method)
        else:
            assert(self.__name__ == method.__name__)

    def __get__(self, obj, objtype):
        """This makes __call__ support instance methods."""
        # Method_list is a list of tuples (constraint, method)
        # Here we are going to assume that we have at least one
        # element in the list. The first registered function
        # will be the one 'wrapped'.
        wrapped_method = self.method_list[0][1]
        # Call functools.wraps manually to get all the attributes
        # we need to be disguised as the wrapped_method
        func = functools.wraps(wrapped_method)(
            functools.partial(self.__call__, obj)
        )
        return func

    def __call__(self, package_self, *args, **kwargs):
        """Find the first method with a spec that matches the
           package's spec.  If none is found, call the default
           or if there is none, then raise a NoSuchMethodError.
        """
        for spec, method in self.method_list:
            if package_self.spec.satisfies(spec):
                return method(package_self, *args, **kwargs)

        if self.default:
            return self.default(package_self, *args, **kwargs)

        else:
            superclass = super(package_self.__class__, package_self)
            superclass_fn = getattr(superclass, self.__name__, None)
            if callable(superclass_fn):
                return superclass_fn(*args, **kwargs)
            else:
                raise NoSuchMethodError(
                    type(package_self), self.__name__, spec,
                    [m[0] for m in self.method_list])

    def __str__(self):
        return "SpecMultiMethod {\n\tdefault: %s,\n\tspecs: %s\n}" % (
            self.default, self.method_list)


class when(object):
    """This annotation lets packages declare multiple versions of
       methods like install() that depend on the package's spec.
       For example:

       .. code-block:: python

          class SomePackage(Package):
              ...

              def install(self, prefix):
                  # Do default install

              @when('arch=chaos_5_x86_64_ib')
              def install(self, prefix):
                  # This will be executed instead of the default install if
                  # the package's platform() is chaos_5_x86_64_ib.

              @when('arch=bgqos_0")
              def install(self, prefix):
                  # This will be executed if the package's sys_type is bgqos_0

       This allows each package to have a default version of install() AND
       specialized versions for particular platforms.  The version that is
       called depends on the architecutre of the instantiated package.

       Note that this works for methods other than install, as well.  So,
       if you only have part of the install that is platform specific, you
       could do this:

       .. code-block:: python

          class SomePackage(Package):
              ...
              # virtual dependence on MPI.
              # could resolve to mpich, mpich2, OpenMPI
              depends_on('mpi')

              def setup(self):
                  # do nothing in the default case
                  pass

              @when('^openmpi')
              def setup(self):
                  # do something special when this is built with OpenMPI for
                  # its MPI implementations.


              def install(self, prefix):
                  # Do common install stuff
                  self.setup()
                  # Do more common install stuff

       There must be one (and only one) @when clause that matches the
       package's spec.  If there is more than one, or if none match,
       then the method will raise an exception when it's called.

       Note that the default version of decorated methods must
       *always* come first.  Otherwise it will override all of the
       platform-specific versions.  There's not much we can do to get
       around this because of the way decorators work.
    """

    def __init__(self, spec):
        pkg = get_calling_module_name()
        if spec is True:
            spec = pkg
        self.spec = (parse_anonymous_spec(spec, pkg)
                     if spec is not False else None)

    def __call__(self, method):
        # Get the first definition of the method in the calling scope
        original_method = caller_locals().get(method.__name__)

        # Create a multimethod out of the original method if it
        # isn't one already.
        if not type(original_method) == SpecMultiMethod:
            original_method = SpecMultiMethod(original_method)

        if self.spec is not None:
            original_method.register(self.spec, method)

        return original_method


class MultiMethodError(spack.error.SpackError):
    """Superclass for multimethod dispatch errors"""

    def __init__(self, message):
        super(MultiMethodError, self).__init__(message)


class NoSuchMethodError(spack.error.SpackError):
    """Raised when we can't find a version of a multi-method."""

    def __init__(self, cls, method_name, spec, possible_specs):
        super(NoSuchMethodError, self).__init__(
            "Package %s does not support %s called with %s.  Options are: %s"
            % (cls.__name__, method_name, spec,
               ", ".join(str(s) for s in possible_specs)))
