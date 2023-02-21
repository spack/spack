# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import inspect
import sys

import llnl.util.tty as tty

#: at what level we should write stack traces or short error messages
#: this is module-scoped because it needs to be set very early
debug = 0


class SpackError(Exception):
    """This is the superclass for all Spack errors.
    Subclasses can be found in the modules they have to do with.
    """

    def __init__(self, message, long_message=None):
        super(SpackError, self).__init__()
        self.message = message
        self._long_message = long_message

        # for exceptions raised from child build processes, we save the
        # traceback as a string and print it in the parent.
        self.traceback = None

        # we allow exceptions to print debug info via print_context()
        # before they are caught at the top level. If they *haven't*
        # printed context early, we do it by default when die() is
        # called, so we need to remember whether it's been called.
        self.printed = False

    @property
    def long_message(self):
        return self._long_message

    def print_context(self):
        """Print extended debug information about this exception.

        This is usually printed when the top-level Spack error handler
        calls ``die()``, but it can be called separately beforehand if a
        lower-level error handler needs to print error context and
        continue without raising the exception to the top level.
        """
        if self.printed:
            return

        # basic debug message
        tty.error(self.message)
        if self.long_message:
            sys.stderr.write(self.long_message)
            sys.stderr.write("\n")

        # stack trace, etc. in debug mode.
        if debug:
            if self.traceback:
                # exception came from a build child, already got
                # traceback in child, so print it.
                sys.stderr.write(self.traceback)
            else:
                # run parent exception hook.
                sys.excepthook(*sys.exc_info())

        sys.stderr.flush()
        self.printed = True

    def die(self):
        self.print_context()
        sys.exit(1)

    def __str__(self):
        msg = self.message
        if self._long_message:
            msg += "\n    %s" % self._long_message
        return msg

    def __repr__(self):
        args = [repr(self.message), repr(self.long_message)]
        args = ",".join(args)
        qualified_name = inspect.getmodule(self).__name__ + "." + type(self).__name__
        return qualified_name + "(" + args + ")"

    def __reduce__(self):
        return type(self), (self.message, self.long_message)


class UnsupportedPlatformError(SpackError):
    """Raised by packages when a platform is not supported"""

    def __init__(self, message):
        super(UnsupportedPlatformError, self).__init__(message)


class NoLibrariesError(SpackError):
    """Raised when package libraries are requested but cannot be found"""

    def __init__(self, message_or_name, prefix=None):
        super(NoLibrariesError, self).__init__(
            message_or_name
            if prefix is None
            else "Unable to locate {0} libraries in {1}".format(message_or_name, prefix)
        )


class NoHeadersError(SpackError):
    """Raised when package headers are requested but cannot be found"""


class SpecError(SpackError):
    """Superclass for all errors that occur while constructing specs."""


class UnsatisfiableSpecError(SpecError):
    """
    Raised when a spec conflicts with package constraints.

    For original concretizer, provide the requirement that was violated when
    raising.
    """

    def __init__(self, provided, required, constraint_type):
        # This is only the entrypoint for old concretizer errors
        super(UnsatisfiableSpecError, self).__init__(
            "%s does not satisfy %s" % (provided, required)
        )

        self.provided = provided
        self.required = required
        self.constraint_type = constraint_type
