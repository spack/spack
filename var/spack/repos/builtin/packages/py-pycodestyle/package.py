# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    url      = "https://github.com/PyCQA/pycodestyle/archive/2.0.0.tar.gz"

    version('2.5.0', 'a603453c07e8d8e15a43cf062aa7174741b74b4a27b110f9ad03d74d519173b5')
    version('2.3.1', '4185319f6137833eec9057dbf3293629')
    version('2.3.0', '1b2019b3c39c20becadbb7fdec6dcb5a')
    version('2.2.0', '6e21aab2e038c3dd38dca585011a6f38')
    version('2.1.0', '1e606c687a6cf01d51305417d0e97824')
    version('2.0.0', '5c3e90001f538bf3b7896d60e92eb6f6')
    version('1.7.0', '31070a3a6391928893cbf5fa523eb8d9')
    version('1.6.2', '8df18246d82ddd3d19ffe7518f983955')
    version('1.6.1', '9d59bdc7c60f46f7cee86c732e28aa1a')
    version('1.6',   '340fa7e39bb44fb08db6eddf7cdc880a')
    version('1.5.7', '6d0f5fc7d95755999bc9275cad5cbf3e')
    version('1.5.6', 'c5c30e3d267b48bf3dfe7568e803a813')
    version('1.5.5', 'cfa12df9b86b3a1dfb13aced1927e12f')
    version('1.5.4', '3977a760829652543544074c684610ee')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
