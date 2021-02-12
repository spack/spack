# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetifaces(PythonPackage):
    """Portable network interface information"""

    homepage = "https://bitbucket.org/al45tair/netifaces"
    pypi = "netifaces/netifaces-0.10.5.tar.gz"

    version('0.10.9', sha256='2dee9ffdd16292878336a58d04a20f0ffe95555465fee7c9bd23b3490ef2abf3')
    version('0.10.8', sha256='befc9800751991c005fcc24e75be90c5752e5c1907ed4fa4efa17adfcc09d490')
    version('0.10.7', sha256='bd590fcb75421537d4149825e1e63cca225fd47dad861710c46bd1cb329d8cbd')
    version('0.10.6', sha256='0c4da523f36d36f1ef92ee183f2512f3ceb9a9d2a45f7d19cda5a42c6689ebe0')
    version('0.10.5', sha256='59d8ad52dd3116fcb6635e175751b250dc783fb011adba539558bd764e5d628b')

    depends_on('py-setuptools', type='build')
