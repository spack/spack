# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyX21(PythonPackage):

    list_url = "https://pypi.org/simple/x21/"

    def url_for_version(self, version):
        url = "https://pypi.io/packages/cp{1}/x/x21/x21-{0}-cp{1}-cp{1}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
        return url.format(version, self.spec['python'].version.up_to(2).joined)
        
    #version('0.2.6', sha256='7c5c58ff6dc81caac6815578f78cf545e719beb0bf4017f77120d38025d2bc7d', expand=False)
    #version('0.2.4', sha256='83a7f3bb904a2564ff24da3d8b24bc3871fadc0db53e88aa1ee0a63a52af3c38', expand=False)
    version('0.2.6', expand=False)

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-pynacl', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-tomli', type=('build', 'run'))
# Requires-Dist: PyNaCl
# Requires-Dist: setuptools
# Requires-Dist: tomli
# Requires-Dist: tomli-w
