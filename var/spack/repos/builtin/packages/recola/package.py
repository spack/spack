# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class Recola(CMakePackage):
    """REcursive Computation of One-Loop Amplitudes:
    a fortran library for the perturbative computation of
    next-to-leading-order transition amplitudes in the
    Standard Model of particle physics."""

    tags = ['hep']

    homepage = "https://recola.hepforge.org"
    url      = "https://recola.hepforge.org/downloads/?f=recola2-2.2.3.tar.gz"

    maintainers = ['vvolkl']

    variant('python', default=True,
            description="Build py-recola python bindings.")

    version('2.2.4', sha256='16bdefb633d51842b4d32c39a43118d7052302cd63be456a473557e9b7e0316e')
    version('2.2.3', sha256='db0f5e448ed603ac4073d4bbf36fd74f401a22876ad390c0d02c815a78106c5f')
    version('1.4.3', url='https://recola.hepforge.org/downloads/?f=recola-1.4.3.tar.gz',
            sha256='f6a7dce6e1f09821ba919524f786557984f216c001ab63e7793e8aa9a8560ceb')

    depends_on('collier')
    depends_on('recola-sm')
    depends_on('python@3:', when='+python')

    def cmake_args(self):
        args = [
            self.define('static', True),
            self.define('collier_path', self.spec['collier'].prefix.lib.cmake),
            self.define('modelfile_path', self.spec['recola-sm'].prefix.lib.cmake),
            self.define_from_variant("with_python3", 'python'),
        ]
        return args
