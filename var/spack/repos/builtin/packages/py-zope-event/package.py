# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZopeEvent(PythonPackage):
    """Very basic event publishing system."""

    homepage = "http://github.com/zopefoundation/zope.event"
    url      = "https://pypi.io/packages/source/z/zope.event/zope.event-4.3.0.tar.gz"

    # FIXME: No idea why this import test fails.
    # Maybe some kind of namespace issue?
    # import_modules = ['zope.event']

    version('4.3.0', sha256='e0ecea24247a837c71c106b0341a7a997e3653da820d21ef6c08b32548f733e7')

    depends_on('py-setuptools', type='build')
