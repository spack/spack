# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWand(PythonPackage):
    """Wand is a ctypes-based simple ImageMagick binding for Python.
    """

    homepage = "http://docs.wand-py.org"
    pypi = "Wand/Wand-0.5.6.tar.gz"

    version('0.6.5', sha256='ec981b4f07f7582fc564aba8b57763a549392e9ef8b6a338e9da54cdd229cf95')
    version('0.6.4', sha256='6aeb0183d94762b37a8cdee97174f38ae21e626d44f62f1e2f0ab48a35026e98')
    version('0.6.3', sha256='d21429288fe0de63d829dbbfb26736ebaed9fd0792c2a0dc5943c5cab803a708')
    version('0.6.2', sha256='65440e478b595aaa18483e25091adacf6d4458c49c2fd8d59e0fd44a7393a14a')
    version('0.6.1', sha256='df0780b1b54938a43d29279a6588fde11e349550c8958a673d57c26a3e6de7f1')
    version('0.6.0', sha256='de45b6252db4f10d2babdde8581e3c39603b1d93124a14a31bf4bd4df6ba0521')
    version('0.5.9', sha256='6eaca78e53fbe329b163f0f0b28f104de98edbd69a847268cc5d6a6e392b9b28')
    version('0.5.8', sha256='6d0925190a846e28412814ea50fa8b3d7969859bac8a93ebc5b2f1c0a1a34d6a')
    version('0.5.7', sha256='13a96818a2f89e7684704ba3bfc20bdb21a15e08736c3fdf74035eeaeefd7873')
    version('0.5.6', sha256='d06b59f36454024ce952488956319eb542d5dc65f1e1b00fead71df94dbfcf88')
    version('0.4.2', sha256='a0ded99a9824ddd82617a4b449164e2c5c93853aaff96f9e0bab8b405d62ca7c')

    variant('docs', default=False, description='Build docs')

    depends_on('py-setuptools', type='build')
    # provides libmagickwand
    depends_on('imagemagick')
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))

    depends_on('py-sphinx@1:', type='build', when='+docs')
