# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySh(PythonPackage):
    """Python subprocess interface"""

    homepage = "https://github.com/amoffat/sh"
    pypi = "sh/sh-1.12.9.tar.gz"

    version('1.14.1',  sha256='39aa9af22f6558a0c5d132881cf43e34828ca03e4ae11114852ca6a55c7c1d8e')
    version('1.14.0',  sha256='05c7e520cdf70f70a7228a03b589da9f96c6e0d06fc487ab21fc62b26a592e59')
    version('1.13.1',  sha256='97a3d2205e3c6a842d87ebbc9ae93acae5a352b1bc4609b428d0fd5bb9e286a3')
    version('1.13.0',  sha256='f00dfb38579ab661786daec7a7b9436facf77682f62160db5b66d58c8b2f270a')
    version('1.12.14', sha256='b52bf5833ed01c7b5c5fb73a7f71b3d98d48e9b9b8764236237bdc7ecae850fc')
    version('1.12.13', sha256='979928ca113cade663bb1a0ff710e3eb9147596cf28a7ee4c04f9d85804f7b9f')
    version('1.12.12', sha256='9b0d150639da53d5c9603cc9e4633aa0845759dd1645ce80ec166ae010ec3c0f')
    version('1.12.11', sha256='6c12be3df55eb2dcd1528fe56f81e52be5b985df42cb34a22171ab7fe986185a')
    version('1.12.10', sha256='599dc8c1678f6c3a905bdf6da7d5943cf4be542ed4ce4ee49e5e392983b1ff8b')
    version('1.12.9', sha256='579aa19bae7fe86b607df1afaf4e8537c453d2ce3d84e1d3957e099359a51677')
    version('1.11',   sha256='590fb9b84abf8b1f560df92d73d87965f1e85c6b8330f8a5f6b336b36f0559a4')

    depends_on('py-setuptools', type='build')
