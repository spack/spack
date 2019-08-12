# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUrwid(PythonPackage):
    """A full-featured console UI library"""
    homepage = "http://urwid.org/"
    url      = "https://pypi.io/packages/source/u/urwid/urwid-1.3.0.tar.gz"

    version('1.3.0', 'a989acd54f4ff1a554add464803a9175')

    depends_on('py-setuptools', type='build')
