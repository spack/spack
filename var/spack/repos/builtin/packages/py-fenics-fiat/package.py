# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsFiat(PythonPackage):
    """The FInite element Automatic Tabulator FIAT supports generation of
    arbitrary order instances of the Lagrange elements on lines, triangles,
    and tetrahedra."""

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/fiat.git"

    # Use this url for version >= 2017.1.0
    url      = "https://bitbucket.org/fenics-project/fiat/get/2018.1.0.tar.gz"

    version('2018.1.0',       sha256='b21ae8c040eb0c129629569110cc1426f458aa237c4f590e7f5a781dce3238ef')
    version('2017.2.0',       sha256='44524aaefe938d448eee07e4398c5f26b3ea15e4b1be3a2bcb248ef239d747ed')
    version('2017.1.0.post1', sha256='9c82daabc5271abfe42ef1960db4b2d34cae5d78d8f104f1e9b83a3ab390ef75')
    version('2017.1.0',       sha256='d1242540206f748843aeed6cf72e4cece9f5063b025737c858d46cb7ce98ae3b')

    # FIXME: Older versions prepend name to version in url
    # url      = "https://bitbucket.org/fenics-project/fiat/get/fiat-2016.2.0.tar.gz"

    # version('2016.2.0',       sha256='9bb6d9337029f7ba895694e1361d6301a902486e5cb057d49c6c8d3d2145c54c')
    # version('2016.1.0',       sha256='dc590dc528b3f564d6ec6ae0e0250aa0e68b3eb8cb66889fe4db4c35aad73b50')
    # version('1.6.0',          sha256='0174d7a095d9103c67997e931e3a5a67943b236fd807ae6363c16808ef1af57f')
    # version('1.5.0',          sha256='0729f12d3cc2533a773f5a41569b3db4645dddadbf3521e23f75aec2cce1bffc')
    # version('1.4.0',          sha256='a8b5d2af534599230622dfc319239a0aa2d27854f5a6fecd495137f6a86eb4c0')
    # version('1.3.0',          sha256='286dc0f688edcc7bd8524907509412698bf88a425377719d6f24d6e48d461647')

    depends_on('python@3:', type=('build', 'run'))

    depends_on('py-sympy@1.1:')
