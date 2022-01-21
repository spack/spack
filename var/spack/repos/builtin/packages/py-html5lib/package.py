# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtml5lib(PythonPackage):
    """HTML parser based on the WHATWG HTML specification."""

    homepage = "https://github.com/html5lib/html5lib-python"
    pypi = "html5lib/html5lib-1.1.tar.gz"

    version('1.1', sha256='b2e5b40261e20f354d198eae92afc10d750afb487ed5e50f9c4eaf07c184146f',
            preferred=True)
    version('1.0.1', sha256='66cb0dcfdbbc4f9c3ba1a63fdb511ffdbd4f513b2b6d81b80cd26ce6b3fb3736')
    version('0.99', sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    version('099', sha256='2612a191a8d5842bfa057e41ba50bbb9dcb722419d2408c78cff4758d0754868',
            deprecated=True)

    depends_on('python@2.6:2.8,3.2:', when='@0.99', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@1.0.1:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@1.1:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-six@1.9:', type=('build', 'run'), when='@1.0.1:')
    depends_on('py-setuptools', type='build', when='@1.0.1:')
    depends_on('py-webencodings', type=('build', 'run'), when='@1.0.1:')
