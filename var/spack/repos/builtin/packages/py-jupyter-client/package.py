# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyJupyterClient(PythonPackage):
    """Jupyter protocol client APIs"""

    homepage = "https://github.com/jupyter/jupyter_client"
    pypi = "jupyter-client/jupyter_client-6.1.7.tar.gz"

    version('7.1.2', sha256='4ea61033726c8e579edb55626d8ee2e6bf0a83158ddf3751b8dd46b2c5cd1e96')
    version('7.0.6', sha256='8b6e06000eb9399775e0a55c52df6c1be4766666209c22f90c2691ded0e338dc')
    version('6.1.12', sha256='c4bca1d0846186ca8be97f4d2fa6d2bae889cce4892a167ffa1ba6bd1f73e782')
    version('6.1.7', sha256='49e390b36fe4b4226724704ea28d9fb903f1a3601b6882ce3105221cd09377a1')
    version('5.3.4', sha256='60e6faec1031d63df57f1cc671ed673dced0ed420f4377ea33db37b1c188b910')
    version('5.2.4', sha256='b5f9cb06105c1d2d30719db5ffb3ea67da60919fb68deaefa583deccd8813551')
    version('4.4.0', sha256='c99a52fac2e5b7a3b714e9252ebf72cbf97536d556ae2b5082baccc3e5cd52ee')
    version('4.3.0', sha256='70b2e88403835a1d54b83858783d9e5e5771fa4bb6f6904e0b5bb8cfde4b99dd')
    version('4.2.2', sha256='3ffc530eff0518fd9bfe3662423a2bec15d0628b9ca159921dd72f34ae004a14')
    version('4.2.1', sha256='ffc4c11db26b099e4a6c9e51337ee12ba8025e01cd8f977ec08d7826d28ed3b8')
    version('4.2.0', sha256='3026cda12d76356f2f3fb5c082811826aecc492e762b69c706ee166dd68ffccf')
    version('4.1.1', sha256='ff1ef5c6c3031a62db46ec6329867b4cb1595e6102a7819b3b5252b0c524bdb8')
    version('4.1.0', sha256='b1786dbf4752907292afed4a5a192572280a8794be0c499d1f530ae8e1550d57')
    version('4.0.0', sha256='a39a4181ea2021daf6e821acae836999ef6e0fefe603813a7a7d4658d2ffa2ac')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@5:')
    depends_on('python@3.5:', type=('build', 'run'), when='@6:')
    depends_on('python@3.6.1:', type=('build', 'run'), when='@6.2:')
    depends_on('py-setuptools', type=('build', 'run'), when='@5:')

    depends_on('py-entrypoints', type=('build', 'run'), when='@7:')
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-jupyter-core@4.6.0:', type=('build', 'run'), when='@6:')
    depends_on('py-nest-asyncio@1.5:', type=('build', 'run'), when='@6.1.13:')
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'), when='@5:')
    depends_on('py-pyzmq@13:', type=('build', 'run'))
    depends_on('py-tornado@4.1:', type=('build', 'run'), when='@5:')
    depends_on('py-traitlets', type=('build', 'run'))
