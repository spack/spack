# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class Edm4hep(CMakePackage):
    """Event data model of Key4hep."""

    homepage = "https://github.com/key4hep/EDM4hep"
    url = "https://github.com/key4hep/EDM4hep/archive/v00-01.tar.gz"
    git = "https://github.com/key4hep/EDM4hep.git"

    maintainers = ['vvolkl']

    tags = ["hep", "key4hep"]

    version('master', branch='master')
    version('0.4.1', sha256='122987fd5969b0f1639afa9668ac5181203746d00617ddb3bf8a2a9842758a63')
    version('0.4', sha256='bcb729cd4a6f5917b8f073364fc950788111e178dd16b7e5218361f459c92a24')
    version('0.3.2', sha256='b6a28649a4ba9ec1c4423bd1397b0a810ca97374305c4856186b506e4c00f769')
    version('0.3.1', sha256='eeec38fe7d72d2a72f07a63dca0a34ca7203727f67869c0abf6bef014b8b319b')
    version('0.3', sha256='d0ad8a486c3ed1659ea97d47b268fe56718fdb389b5935f23ba93804e4d5fbc5')

    patch('test-deps.patch', when='@:0.3.2')

    variant('cxxstd',
            default='17',
            values=('17',),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.3:', type='build')
    depends_on('python', type='build')

    depends_on('root@6.08:')
    depends_on('podio@0.14.1:', when='@0.4.1:')
    depends_on('podio@0.14', when='@0.4')
    depends_on('podio@0.13.0:0.13', when='@:0.3')
    depends_on('py-jinja2', type='build')
    depends_on('py-pyyaml', type='build')

    depends_on('hepmc@:2', type='test', when='@:0.4.0')
    depends_on('hepmc3', type='test', when='@0.4.1:')
    depends_on('heppdt', type='test')
    depends_on('catch2@3.0.1:', type='test')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append(self.define('CMAKE_CXX_STANDARD',
                    self.spec.variants['cxxstd'].value))
        args.append(self.define("BUILD_TESTING", self.run_tests))
        return args

    def url_for_version(self, version):
        """Translate version numbers to ilcsoft conventions.
        in spack, the convention is: 0.1 (or 0.1.0) 0.1.1, 0.2, 0.2.1 ...
        in ilcsoft, releases are dashed and padded with a leading zero
        the patch version is omitted when 0
        so for example v01-12-01, v01-12 ...
        :param self: spack package class that has a url
        :type self: class: `spack.PackageBase`
        :param version: version
        :type param: str
        """
        base_url = self.url.rsplit('/', 1)[0]

        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version

        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = 'v%02d-%02d.tar.gz' % (major, minor)
        else:
            version_str = 'v%02d-%02d-%02d.tar.gz' % (major, minor, patch)

        return base_url + '/' + version_str
