# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Openmc(CMakePackage):
    """The OpenMC project aims to provide a fully-featured Monte Carlo particle
       transport code based on modern methods. It is a constructive solid
       geometry, continuous-energy transport code that uses ACE format cross
       sections. The project started under the Computational Reactor Physics
       Group at MIT."""

    homepage = "http://openmc.readthedocs.io/"
    url = "https://github.com/openmc-dev/openmc/tarball/v0.10.0"
    git = "https://github.com/openmc-dev/openmc.git"

    version('0.10.0', 'abb57bd1b226eb96909dafeec31369b0')
    version('develop')

    depends_on("hdf5+hl")

    def cmake_args(self):
        options = ['-DHDF5_ROOT:PATH=%s' % self.spec['hdf5'].prefix]

        return options
