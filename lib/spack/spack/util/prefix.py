# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains utilities for managing the installation prefix of a package.
"""
import os


class Prefix(str):
    """This class represents an installation prefix, but provides useful
    attributes for referring to directories inside the prefix.

    Attributes of this object are created on the fly when you request them,
    so any of the following is valid:

    >>> prefix = Prefix('/usr')
    >>> prefix.bin
    /usr/bin
    >>> prefix.lib64
    /usr/lib64
    >>> prefix.share.man
    /usr/share/man
    >>> prefix.foo.bar.baz
    /usr/foo/bar/baz
    >>> prefix.join('dashed-directory').bin64
    /usr/dashed-directory/bin64

    Prefix objects behave identically to strings. In fact, they
    subclass ``str``. So operators like ``+`` are legal::

        print('foobar ' + prefix)

    This prints ``foobar /usr``. All of this is meant to make custom
    installs easy.
    """
    def __getattr__(self, attr):
        return Prefix(os.path.join(self, attr))

    def join(self, string):
        """Concatenates a string to a prefix.

        Parameters:
            string (str): the string to append to the prefix

        Returns:
            Prefix: the newly created installation prefix
        """
        return Prefix(os.path.join(self, string))

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)
