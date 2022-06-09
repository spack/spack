# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    pypi     = "pycodestyle/pycodestyle-2.8.0.tar.gz"

    version('2.8.0', sha256='eddd5847ef438ea1c7870ca7eb78a9d47ce0cdb4851a5523949f2601d0cbbe7f')
    version('2.7.0', sha256='c389c1d06bf7904078ca03399a4816f974a1d590090fecea0c63ec26ebaf1cef')
    version('2.6.0', sha256='c58a7d2815e0e8d7972bf1803331fb0152f867bd89adf8a01dfd55085434192e')
    version('2.5.0', sha256='a603453c07e8d8e15a43cf062aa7174741b74b4a27b110f9ad03d74d519173b5')
    version('2.3.1', sha256='682256a5b318149ca0d2a9185d365d8864a768a28db66a84a2ea946bcc426766')
    version('2.3.0', sha256='a5910db118cf7e66ff92fb281a203c19ca2b5134620dd2538a794e636253863b')
    version('2.2.0', sha256='df81dc3293e0123e2e8d1f2aaf819600e4ae287d8b3af8b72181af50257e5d9a')
    version('2.1.0', sha256='5b540e4f19b4938c082cfd13f5d778d1ad2308b337abbc687ab9335233f5f3e2')
    version('2.0.0', sha256='37f0420b14630b0eaaf452978f3a6ea4816d787c3e6dcbba6fb255030adae2e7')
    # Versions below 2.0.0 are not on pypi
    version('1.7.0', sha256='3f62d19b5cbcbdcb7810f967dcc2fbdd090256e090c32b457e2580a841d118ef',
            url='https://github.com/PyCQA/pycodestyle/archive/1.7.0.tar.gz', deprecated=True)
    version('1.6.2', sha256='508bfd7d457046891bf4b8fbfc95ccac7995c37cdfdb3daf97bfeb7a13fa4c9c',
            url='https://github.com/PyCQA/pycodestyle/archive/1.6.2.tar.gz', deprecated=True)
    version('1.6.1', sha256='3a910a0d0d998d4c3c2b8152a4816b98938b27cc73a4433c61202449706a73c8',
            url='https://github.com/PyCQA/pycodestyle/archive/1.6.1.tar.gz', deprecated=True)
    version('1.6',   sha256='5e7bb5156af311079345b5e81f8154c3e1420d723150a6cba5a70245eb0d515a',
            url='https://github.com/PyCQA/pycodestyle/archive/1.6.tar.gz',   deprecated=True)
    version('1.5.7', sha256='9bf020638986f2e254823aee62cfd97e55ba08ad51503cd5ae26172c47f48401',
            url='https://github.com/PyCQA/pycodestyle/archive/1.5.7.tar.gz', deprecated=True)
    version('1.5.6', sha256='9f164c1211854678b2cb269954bc8aac2dcfa142d40c99f7bab08f9344cf3241',
            url='https://github.com/PyCQA/pycodestyle/archive/1.5.6.tar.gz', deprecated=True)
    version('1.5.5', sha256='e55204c5477a29eb094835ad6e83be292aa3e06be12e51f5b4cc67f38d0d61ba',
            url='https://github.com/PyCQA/pycodestyle/archive/1.5.5.tar.gz', deprecated=True)
    version('1.5.4', sha256='bc234f7935a350c79c953421b01163db01010f39caeddfa8602ff54f76a6fd9e',
            url='https://github.com/PyCQA/pycodestyle/archive/1.5.4.tar.gz', deprecated=True)

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@2.7.0:')
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@2.8.0:')
