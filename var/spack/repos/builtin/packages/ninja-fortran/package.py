##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class NinjaFortran(Package):
    """A Fortran capable fork of ninja."""

    homepage = "https://github.com/Kitware/ninja"
    url      = "https://github.com/Kitware/ninja/archive/v1.7.2.gaad58.kitware.dyndep-1.tar.gz"

    # Each version is a fork off of a specific commit of ninja
    # Hashes don't sort properly, so manually set newest version
    version('1.7.2.gaad58', 'eb51b042b9dbaf8ecd79a6fb24de1320', preferred=True)
    version('1.7.2.gcc0ea', '3982f508c415c0abaca34cb5e92e711a')
    version('1.7.1.g7ca7f', '187a8d15c1e20e5e9b00c5c3f227ca8a')

    depends_on('python', type=('build', 'run'))

    phases = ['configure', 'install']

    def url_for_version(self, version):
        url = 'https://github.com/Kitware/ninja/archive/v{0}.kitware.dyndep-1.tar.gz'
        return url.format(version)

    def configure(self, spec, prefix):
        python('configure.py', '--bootstrap')

    @run_after('configure')
    @on_package_attributes(run_tests=True)
    def test(self):
        ninja = Executable('./ninja')
        ninja('-j{0}'.format(make_jobs), 'ninja_test')
        ninja_test = Executable('./ninja_test')
        ninja_test()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('ninja', prefix.bin)
        install_tree('misc', prefix.misc)

        # Some distros like Fedora install a 'ninja-build' executable
        # instead of 'ninja'. Install both for uniformity.
        with working_dir(prefix.bin):
            symlink('ninja', 'ninja-build')
