# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyIpywidgets(PythonPackage):
    """IPython widgets for the Jupyter Notebook"""

    homepage = "https://github.com/ipython/ipywidgets"
    pypi = "ipywidgets/ipywidgets-7.6.5.tar.gz"

    version('7.7.0', sha256='ab4a5596855a88b83761921c768707d65e5847068139bc1729ddfe834703542a')
    version('7.6.5', sha256='00974f7cb4d5f8d494c19810fedb9fa9b64bffd3cda7c2be23c133a1ad3c99c5')
    version('7.6.3', sha256='9f1a43e620530f9e570e4a493677d25f08310118d315b00e25a18f12913c41f0')
    version('7.5.1', sha256='e945f6e02854a74994c596d9db83444a1850c01648f1574adf144fbbabe05c97')
    version('7.4.2', sha256='a3e224f430163f767047ab9a042fc55adbcab0c24bbe6cf9f306c4f89fdf0ba3')
    version('5.2.2', sha256='baf6098f054dd5eacc2934b8ea3bef908b81ca8660d839f1f940255a72c660d2')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
    depends_on('py-ipython@4:', type=('build', 'run'))
    depends_on('py-ipython@4:5', type=('build', 'run'), when='^python@:3.2')
    depends_on('py-jupyterlab-widgets@1.0.0:', type=('build', 'run'),
               when='^python@3.6:')
    depends_on('py-ipykernel@4.2.2:', type=('build', 'run'))
    depends_on('py-ipykernel@4.5.1:', type=('build', 'run'), when='@6:')
    depends_on('py-ipython-genutils@0.2.0:0.2', type=('build', 'run'),
               when='@7.6.4:')
    depends_on('py-traitlets@4.2.1:', type=('build', 'run'))
    depends_on('py-traitlets@4.3.1:', type=('build', 'run'), when='@6:')
    depends_on('py-nbformat@4.2.0:', type=('build', 'run'), when='@6:')
    depends_on('py-widgetsnbextension@1.2.6:1.9', type=('build', 'run'),
               when='@5.2.2')
    depends_on('py-widgetsnbextension@3.4.0:3.4', type=('build', 'run'),
               when='@7.4.2')
    depends_on('py-widgetsnbextension@3.5.0:3.5', type=('build', 'run'),
               when='@7.5.1:7.6.5')
    depends_on('py-widgetsnbextension@3.6', type=('build', 'run'),
               when='@7.7:')
