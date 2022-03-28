# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Implementation of Spack imports that uses imp underneath.

``imp`` is deprecated in newer versions of Python, but is the only option
in Python 2.6.
"""
import imp
import tempfile
from contextlib import contextmanager


@contextmanager
def import_lock():
    try:
        imp.acquire_lock()
        yield
    finally:
        imp.release_lock()


def load_source(full_name, path, prepend=None):
    """Import a Python module from source.

    Load the source file and add it to ``sys.modules``.

    Args:
        full_name (str): full name of the module to be loaded
        path (str): path to the file that should be loaded
        prepend (str or None): some optional code to prepend to the
            loaded module; e.g., can be used to inject import statements

    Returns:
        the loaded module
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
