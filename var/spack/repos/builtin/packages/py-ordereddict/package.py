# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOrdereddict(PythonPackage):
    """A drop-in substitute for Py2.7's new collections.
    OrderedDict that works in Python 2.4-2.6."""

    homepage = "https://pypi.python.org/pypi/ordereddict"
    url      = "https://pypi.io/packages/source/o/ordereddict/ordereddict-1.1.tar.gz"

    import_modules = ['ordereddict']

    version('1.1', 'a0ed854ee442051b249bfad0f638bbec')
