# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRjags(RPackage):
    """Interface to the JAGS MCMC library.
       Usage: $ spack load r-rjags """

    homepage = "https://cran.r-project.org/web/packages/rjags/index.html"
    url      = "https://cran.r-project.org/src/contrib/rjags_4-6.tar.gz"

    version('4-6', 'c26b7cc8e8ddcdb55e14cba28df39f4c')

    depends_on('jags', type=('link'))
    depends_on('r-coda', type=('build', 'run'))

    def configure_args(self):
        args = ['--with-jags-lib=%s' % self.spec['jags'].prefix.lib,
                '--with-jags-include=%s' % self.spec['jags'].prefix.include,
                '--with-jags-modules=%s/JAGS/modules-4'
                % self.spec['jags'].prefix.lib]
        return args
