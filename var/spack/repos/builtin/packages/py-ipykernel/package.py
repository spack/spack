# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpykernel(PythonPackage):
    """IPython Kernel for Jupyter"""

    homepage = "https://pypi.python.org/pypi/ipykernel"
    url      = "https://github.com/ipython/ipykernel/archive/4.5.0.tar.gz"

    version('5.1.0',  sha256='30f01a2a1470d3fabbad03f5c43606c1bc2142850fc4ccedcf44281664ae9122')
    version('4.10.0', sha256='df2714fd0084085ed68876f75ab846202d261420b5f4069af6335b8df0475391')
    version('4.5.0',  sha256='c5ec5130f5f7eda71345b9ef638c9213c4c2f41610a9ad338a0f1d0819421adf')
    version('4.4.1',  sha256='62fe16252e40fb3d443fcf31fc52e5596965cf17620571c10ea64502a6d51db7')
    version('4.4.0',  sha256='a042bf202c5675da58dba66b9bd1e7aecc62d4f82058508b620a09e2f7baa0f2')
    version('4.3.1',  sha256='f38b366053567c36464ae6d04d72ed72d74f77e63d49a6fa38826278ed7848fd')
    version('4.3.0',  sha256='cf21ee03b258ee5d1fcef8189c5cecba017e22f3517ff8d49730102ff74d61af')
    version('4.2.2',  sha256='9cfa31b893a430ce0800a0780b6326a15658543651d2116849e0283ec39e67fc')
    version('4.2.1',  sha256='12c30f3d267068db4d31897d12653908cf543358faed5bad37d60eede6a909c4')
    version('4.2.0',  sha256='43f6847f816e4683842878e33c6c11d5311c2be9f1fe1f44c391f5abefd35e72')
    version('4.1.1',  sha256='59e7e1ca516b9ee109e9a51b942bda03ac8e214891956e787da997b252f5e736')
    version('4.1.0',  sha256='b72c3354ac12a219b9be928ff3b5125e5c861e9592fb4eb342f1d47592cb3740')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.4:', when='@5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@5:')
    depends_on('py-traitlets@4.1.0:', type=('build', 'run'))
    depends_on('py-tornado@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-tornado@4.2:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-ipython@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-ipython@5.0:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-pexpect', type=('build', 'run'))
