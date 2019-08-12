# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NinjaFortran(Package):
    """A Fortran capable fork of ninja."""

    homepage = "https://github.com/Kitware/ninja"
    url      = "https://github.com/Kitware/ninja/archive/v1.9.0.g99df1.kitware.dyndep-1.jobserver-1.tar.gz"

    # Each version is a fork off of a specific commit of ninja
    # Hashes don't sort properly, so added "artificial" tweak-level version
    # number prior to the hashes for sorting puposes
    version('1.9.0.2.g99df1', 'f0892b1c8fd2984e8f47e9e1fcb9ce32')
    version('1.9.0.1.g5b44b', 'f7c2e718801c1fd097a728530559e0d4')
    version('1.9.0.0.gad558', 'cb93ffb5871225e2b813eb9c34b3096d')
    version('1.8.2.2.g81279', '0e29d0c441dcbd9b9ee9291c3a8dfbdd')
    version('1.8.2.1.g3bbbe', 'de6257118f2e3ac7fa1abca1e7c70afa')
    version('1.8.2.0.g972a7', '8ace90ad0c5657022d10ba063783a652')
    version('1.7.2.1.gaad58', 'eb51b042b9dbaf8ecd79a6fb24de1320')
    version('1.7.2.0.gcc0ea', '3982f508c415c0abaca34cb5e92e711a')
    version('1.7.1.0.g7ca7f', '187a8d15c1e20e5e9b00c5c3f227ca8a')

    depends_on('python', type='build')

    phases = ['configure', 'install']

    def url_for_version(self, version):
        # for some reason the hashes are being stripped from incomming
        # version, so find the incomming version in all package versions
        for ver in self.versions:
            if str(version) in str(ver):
                break

        # remove the "artificial" tweak-level
        split_ver = str(ver).split('.')
        url_version = ".".join(split_ver[:3]) + "." + split_ver[4]

        if version < spack.version.Version('1.8.2.1'):
            url = 'https://github.com/Kitware/ninja/archive/v{0}.kitware.dyndep-1.tar.gz'
        else:
            url = 'https://github.com/Kitware/ninja/archive/v{0}.kitware.dyndep-1.jobserver-1.tar.gz'
        return url.format(url_version)

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
