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
"""Implementation of Spack imports that uses imp underneath.

``imp`` is deprecated in newer versions of Python, but is the only option
in Python 2.6.
"""
import imp
import tempfile
from contextlib import contextmanager


@contextmanager
def import_lock():
    imp.acquire_lock()
    yield
    imp.release_lock()


def load_source(full_name, path, prepend=None):
    """Import a Python module from source.

    Load the source file and add it to ``sys.modules``.

    Args:
        full_name (str): full name of the module to be loaded
        path (str): path to the file that should be loaded
        prepend (str, optional): some optional code to prepend to the
            loaded module; e.g., can be used to inject import statements

    Returns:
        (ModuleType): the loaded module
    """
    with import_lock():
        if prepend is None:
            return imp.load_source(full_name, path)
        else:
            with prepend_open(path, text=prepend) as f:
                return imp.load_source(full_name, path, f)


@contextmanager
def prepend_open(f, *args, **kwargs):
    """Open a file for reading, but prepend with some text prepended

    Arguments are same as for ``open()``, with one keyword argument,
    ``text``, specifying the text to prepend.

    We have to write and read a tempfile for the ``imp``-based importer,
    as the ``file`` argument to ``imp.load_source()`` requires a
    low-level file handle.

    See the ``importlib``-based importer for a faster way to do this in
    later versions of python.
    """
    text = kwargs.get('text', None)

    with open(f, *args) as f:
        with tempfile.NamedTemporaryFile(mode='w+') as tf:
            if text:
                tf.write(text + '\n')
            tf.write(f.read())
            tf.seek(0)
            yield tf.file
