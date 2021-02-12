# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPydeps(PythonPackage):
    """Python module dependency visualization."""

    pypi = "pydeps/pydeps-1.7.1.tar.gz"

    version('1.9.13', sha256='4f1810814aefe9822db041696e3d845d3ac499574d19cdaa9cf933170248d143')
    version('1.9.11', sha256='05dde7194fcf1c2a52bd9b30a92749a98411f427b441be31c0fb2d082060ad16')
    version('1.9.10', sha256='479df4b98d5eeece1e996a2224d571cd2e13ab7caed460092698e31e9ee4b39d')
    version('1.9.9',  sha256='dceb972167db9cba4ee626f68783f3c25d13e903aef0eaa0ee278c856efb61cd')
    version('1.9.8',  sha256='36fa9c97440b2eca9b51521a195e00656363772a3bd972a330765dafa9d43e44')
    version('1.9.7',  sha256='df131ba72e5fea37603badb2a5013e9880cbfe859236c8baae7cf0310e9892ae')
    version('1.9.6',  sha256='b4314dca0e30057e05ad81c3a4c69c50414526901413b5e7a98efd865a74c33f')
    version('1.9.4',  sha256='ed0f887985af4924da55cd008140e8d47b67083149f372c81647f556f6d37b84')
    version('1.9.3',  sha256='a31c92b39a145ff46c2a1026d62952e051401895c69019af33506c751f8bd8a1')
    version('1.9.2',  sha256='5030dd541f4750157009118a176bb45806c2dfcc62fe13de55d962fe75960443')
    version('1.9.1',  sha256='5aebdf415d12c9708c2dd9e1aa8c7a90f3a3145ca9e0b72273a993c629d7cb73')
    version('1.9.0', sha256='ba9b8c7d72cb4dfd3f4dd6b8a250c240d15824850a415fd428f2660ed371361f')
    version('1.7.1', sha256='7eeb8d0ec2713befe81dd0d15eac540e843b1daae13613df1c572528552d6340')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-stdlib-list', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
