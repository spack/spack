# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyX21(PythonPackage):
    """FIXME: I think this is for unpacking this authors
    obfuscaded python libraries."""

    homepage = "https://pypi.org/project/x21/"
    list_url = "https://pypi.org/simple/x21/"

    def url_for_version(self, version):
        url = "https://pypi.io/packages/cp{1}/x/x21/x21-{0}-cp{1}-cp{1}{2}-{3}.whl"

        platform_string = {
            'linux': "manylinux_2_17_x86_64.manylinux2014_x86_64",
            'darwin': "macosx_10_9_x86_64"
        }

        return url.format(version,
                          self.spec['python'].version.up_to(2).joined,
                          'm' if self.spec.satisfies("^python@3.7.0:3.7") else '',
                          platform_string[self.spec.platform])

    # NOTE: Due to the this package having different packages for each
    # version of python and platform, checksums have not been provided.
    version('0.2.6', expand=False)

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-pynacl', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-tomli', type=('build', 'run'))
    depends_on('py-tomli-w', type=('build', 'run'))
    depends_on('py-pynacl', type=('build', 'run'))
