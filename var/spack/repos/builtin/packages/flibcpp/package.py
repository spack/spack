# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flibcpp(CMakePackage):
    """Fortran bindings to the C++ Standard Library.
    """

    homepage = "https://flibcpp.readthedocs.io/en/latest"
    git = "https://github.com/swig-fortran/flibcpp.git"
    url = "https://github.com/swig-fortran/flibcpp/archive/v0.3.0.tar.gz"

    version('master', branch='master')
    version('0.3.0', sha256='2e68a3c8fcfa4fad9f6d5e1cafa5bd44ee6b878cc5a4ee3d69a98f1950c0547b')

    variant('doc', default=False, description='Build and install documentation')
    variant('shared', default=True, description='Build shared libraries')
    variant('swig', default=False,
            description='Regenerate source files using SWIG')
    variant('fstd', default='03', values=('none', '03', '08', '15', '18'),
            multi=False, description='Build with this Fortran standard')

    depends_on('swig@fortran', type='build', when="+swig")
    depends_on('py-sphinx', type='build', when="+doc")

    def cmake_args(self):
        spec = self.spec
        def hasopt(key):
            return "ON" if ("+" + key) in spec else "OFF"

        testopt = "ON" if self.run_tests else "OFF"
        opts = [('BUILD_SHARED_LIBS', hasopt('shared')),
                ('BUILD_TESTING', testopt),
                ('FLIBCPP_BUILD_DOCS', hasopt('doc')),
                ('FLIBCPP_BUILD_EXAMPLES', testopt)]
        fstd = spec.variants['fstd'].value
        opts.append(('FLIBCPP_FORTRAN_STD', fstd))

        return ['-D{0}={1}'.format(k,v) for (k,v) in opts]
