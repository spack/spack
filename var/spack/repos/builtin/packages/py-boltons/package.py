# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBoltons(PythonPackage):
    """When they're not builtins, they're boltons.

    Functionality that should be in the standard library. Like builtins,
    but Boltons.

    Otherwise known as, "everyone's util.py," but cleaned up and tested.
    """
    homepage = "https://boltons.readthedocs.io/"
    pypi = "boltons/boltons-16.5.1.tar.gz"

    version('20.2.1', sha256='dd362291a460cc1e0c2e91cc6a60da3036ced77099b623112e8f833e6734bdc5')
    version('20.2.0', sha256='d367506c0b32042bb1ee3bf7899f2dcc8492dceb42ce3727b89e174d85bffe6e')
    version('20.1.0', sha256='6e890b173c5f2dcb4ec62320b3799342ecb1a6a0b2253014455387665d62c213')
    version('20.0.0', sha256='e44ddbd10af0904147c194d2c9bd2affa6a3e5b2ebfb9d5547900d8931203953')
    version('19.3.0', sha256='7b3344098aa0d593e1a04cd290f61310d5aefc66aeb1e07262d5afdabdb88a67')
    version('19.2.0', sha256='249def4ff32e0dbdeb92aa768118e9c68983f50e69147fcadf9752543eabeddf')
    version('19.1.0', sha256='c32b2d121331a9bc7c220050d4273f3aa359b7569cb4794188e71524603113dc')
    version('19.0.1', sha256='1bc30bd881028ee8d058c1b5f706f241367abba5c288bad469bfb00a9a27a8ba')
    version('19.0.0', sha256='194346ba090dd7cbe5bb2cd59246eb043ce088128cca69902aebe30dcd96efc6')
    version('18.0.1', sha256='1b7dd3892e949e7979f9ec4696b29e47e5b8f5ec0c231719bfb5e467202d04d1')
    version('18.0.0', sha256='a11e113cf3f0915a21ee2c8c69c315b02f46546ad61d3640e1037b7603f6e16f')
    version('17.2.0', sha256='c7496b4b0edfff7e5f27d61da4393fc27fee09c64fa66a423f1e64fa16458a20')
    version('17.1.0', sha256='b349ad10ec233ecd5e8e4c66b1654a5cffa7b70c2b8164b648c41bf2e266f4e8')
    version('17.0.0', sha256='e8fb9e90eee94e8b1ddd20038a22312b6699faa2edc089f9e7bf13533800d5fe')
    version('16.5.1', sha256='fcded58596fa79bd1ada4488178e79fd11c7cb449f29ff9a6532411fb2db19b7')

    depends_on('py-setuptools', type='build')
