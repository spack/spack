# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Libseccomp(AutotoolsPackage):
    """The main libseccomp repository"""

    homepage = "https://github.com/seccomp/libseccomp"
    url      = 'https://github.com/seccomp/libseccomp/releases/download/v2.5.3/libseccomp-2.5.3.tar.gz'

    version('2.5.3', sha256='59065c8733364725e9721ba48c3a99bbc52af921daf48df4b1e012fbc7b10a76')
    version('2.3.3', sha256='7fc28f4294cc72e61c529bedf97e705c3acf9c479a8f1a3028d4cd2ca9f3b155')

    variant('python', default=True, description="Build Python bindings")

    depends_on('gperf',     type='build', when='@2.5:')
    depends_on("py-cython", type="build", when="+python")

    def configure_args(self):
        args = []
        if "+python" in self.spec:
            args.append("--enable-python")
        return args
