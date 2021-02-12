# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyquaternion(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://kieranwynn.github.io/pyquaternion/"
    pypi = "pyquaternion/pyquaternion-0.9.5.tar.gz"

    version('0.9.9', sha256='b1f61af219cb2fe966b5fb79a192124f2e63a3f7a777ac3cadf2957b1a81bea8')
    version('0.9.8', sha256='17b389149adbe2273162d97f91d923ddc0d7e8fc387682e1564d6c0022be582f')
    version('0.9.5', sha256='2d89d19259d62a8fbd25219eee7dacc1f6bb570becb70e1e883f622597c7d81d')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy', type='run')
