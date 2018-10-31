# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRjags(RPackage):
    """Interface to the JAGS MCMC library.
       Usage: $ spack load r-rjags """

    homepage = "https://cran.r-project.org/web/packages/rjags/index.html"
    url      = "https://cran.r-project.org/src/contrib/rjags_4-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rjags/"

    version('4-8', sha256='1529827ab11493fb5f05552e239d700ae2f818995d86d3c9e4c92523f594b59f')
    version('4-6', 'c26b7cc8e8ddcdb55e14cba28df39f4c')

    depends_on('jags', type=('link'))
    depends_on('r-coda', type=('build', 'run'))

    def configure_args(self):
        args = ['--with-jags-lib=%s' % self.spec['jags'].prefix.lib,
                '--with-jags-include=%s' % self.spec['jags'].prefix.include,
                '--with-jags-modules=%s/JAGS/modules-4'
                % self.spec['jags'].prefix.lib]
        return args
