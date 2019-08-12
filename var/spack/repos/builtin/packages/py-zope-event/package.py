# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('4.3.0', '8ca737960741c6fd112972f3313303bd')

    depends_on('py-setuptools', type='build')
