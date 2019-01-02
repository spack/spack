# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
