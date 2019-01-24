# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyPycairo(PythonPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    url      = "https://github.com/pygobject/pycairo/releases/download/v1.17.1/pycairo-1.17.1.tar.gz"
    url      = "https://files.pythonhosted.org/packages/68/76/340ff847897296b2c8174dfa5a5ec3406e3ed783a2abac918cf326abad86/pycairo-1.17.1.tar.gz"

    version('1.17.1', '34c1ee106655b450c4bd57e29371a4a7')

    depends_on('cairo@1.2.0:')
    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')

    @run_after('install')
    def post_install(self):
        src = self.prefix.lib + '/pkgconfig/py3cairo.pc'
        dst = self.prefix.lib + '/pkgconfig/pycairo.pc'
        if os.path.exists(src) and not os.path.exists(dst):
            copy(src, dst)
