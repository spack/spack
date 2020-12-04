# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Edm4hep(CMakePackage):
    """Event data model of Key4hep."""

    homepage = "https://github.com/key4hep/EDM4hep"
    url = "https://github.com/key4hep/EDM4hep/archive/v00-01.tar.gz"
    git = "https://github.com/key4hep/EDM4hep.git"

    maintainers = ['vvolkl']

    tags = ["hep", "key4hep"]

    version('master', branch='master')
    version('0.3', sha256='d0ad8a486c3ed1659ea97d47b268fe56718fdb389b5935f23ba93804e4d5fbc5')

    variant('cxxstd',
            default='17',
            values=('17',),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.3:', type='build')
    depends_on('python', type='build')

    depends_on('root@6.08:')
    depends_on('podio@0.13:')

    depends_on('hepmc@:2.99.99', type='test')
    depends_on('heppdt', type='test')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append(self.define('CMAKE_CXX_STANDARD',
                    self.spec.variants['cxxstd'].value))
        return args

    def url_for_version(self, version):
        # edm4hep releases are dashed and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        base_url = self.url.rsplit('/', 1)[0]
        major = str(version[0]).zfill(2)
        minor = str(version[1]).zfill(2)
        # handle the different cases for the patch version:
        # first case, no patch version is given in spack, i.e 0.1
        if len(version) == 2:
            url = base_url + "/v%s-%s.tar.gz" % (major, minor)
        # a patch version is specified in spack, i.e. 0.1.x ...
        elif len(version) == 3:
            patch = str(version[2]).zfill(2)
            # ... but it is zero, and not part of the ilc release url
            if version[2] == 0:
                url = base_url + "/v%s-%s.tar.gz" % (major, minor)
            # ... if it is non-zero, it is part  of the release url
            else:
                url = base_url + "/v%s-%s-%s.tar.gz" % (major, minor, patch)
        else:
            print('Error - Wrong version format provided')
            return
        return url
