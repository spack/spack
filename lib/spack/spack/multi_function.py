"""This module contains utilities for using multi-functions in spack.
You can think of multi-functions like overloaded functions -- they're
functions with the same name, and we need to select a version of the
function based on some criteria.  e.g., for overloaded functions, you
would select a version of the function to call based on the types of
its arguments.

For spack, we might want to select a version of the function based on
the platform we want to build a package for, or based on the versions
of the dependencies of the package.
"""
import sys
import functools

import spack.architecture
import spack.error as serr

class NoSuchVersionError(serr.SpackError):
    """Raised when we can't find a version of a function for a platform."""
    def __init__(self, fun_name, sys_type):
        super(NoSuchVersionError, self).__init__(
            "No version of %s found for %s!" % (fun_name, sys_type))


class PlatformMultiFunction(object):
    """This is a callable type for storing a collection of versions
       of an instance method.  The platform decorator (see docs below)
       creates PlatformMultiFunctions and registers function versions
       with them.

       To register a function, you can do something like this:
           pmf = PlatformMultiFunction()
           pmf.regsiter("chaos_5_x86_64_ib", some_function)

       When the pmf is actually called, it selects a version of
       the function to call based on the sys_type of the object
       it is called on.

       See the docs for the platform decorator for more details.
    """
    def __init__(self, default=None):
        self.function_map = {}
        self.default = default
        if default:
            self.__name__ = default.__name__

    def register(self, platform, function):
        """Register a version of a function for a particular sys_type."""
        self.function_map[platform] = function
        if not hasattr(self, '__name__'):
            self.__name__ = function.__name__
        else:
            assert(self.__name__ == function.__name__)

    def __get__(self, obj, objtype):
        """This makes __call__ support instance methods."""
        return functools.partial(self.__call__, obj)

    def __call__(self, package_self, *args, **kwargs):
        """Try to find a function that matches package_self.sys_type.
           If none is found, call the default function that this was
           initialized with.  If there is no default, raise an error.
        """
        # TODO: make this work with specs.
        sys_type = package_self.sys_type
        function = self.function_map.get(sys_type, self.default)
        if function:
            function(package_self, *args, **kwargs)
        else:
            raise NoSuchVersionError(self.__name__, sys_type)

    def __str__(self):
        return "<%s, %s>" % (self.default, self.function_map)


class platform(object):
    """This annotation lets packages declare platform-specific versions
       of functions like install().  For example:

       class SomePackage(Package):
           ...

           def install(self, prefix):
               # Do default install

           @platform('chaos_5_x86_64_ib')
           def install(self, prefix):
               # This will be executed instead of the default install if
               # the package's sys_type() is chaos_5_x86_64_ib.

           @platform('bgqos_0")
           def install(self, prefix):
               # This will be executed if the package's sys_type is bgqos_0

       This allows each package to have a default version of install() AND
       specialized versions for particular platforms.  The version that is
       called depends on the sys_type of SomePackage.

       Note that this works for functions other than install, as well.  So,
       if you only have part of the install that is platform specific, you
       could do this:

       class SomePackage(Package):
           ...

           def setup(self):
               # do nothing in the default case
               pass

           @platform('chaos_5_x86_64_ib')
           def setup(self):
               # do something for x86_64

           def install(self, prefix):
               # Do common install stuff
               self.setup()
               # Do more common install stuff

       If there is no specialized version for the package's sys_type, the
       default (un-decorated) version will be called.  If there is no default
       version and no specialized version, the call raises a
       NoSuchVersionError.

       Note that the default version of install() must *always* come first.
       Otherwise it will override all of the platform-specific versions.
       There's not much we can do to get around this because of the way
       decorators work.
    """
class platform(object):
    def __init__(self, sys_type):
        self.sys_type = sys_type

    def __call__(self, fun):
        # Record the sys_type as an attribute on this function
        fun.sys_type = self.sys_type

        # Get the first definition of the function in the calling scope
        calling_frame = sys._getframe(1).f_locals
        original_fun = calling_frame.get(fun.__name__)

        # Create a multifunction out of the original function if it
        # isn't one already.
        if not type(original_fun) == PlatformMultiFunction:
            original_fun = PlatformMultiFunction(original_fun)

        original_fun.register(self.sys_type, fun)
        return original_fun
