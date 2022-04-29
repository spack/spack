# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class PyTypeguard(PythonPackage):
    """
    Run-time type checker for Python
    """

    homepage = "https://github.com/agronholm/typeguard"
    pypi     = "typeguard/typeguard-2.12.1.tar.gz"

    version('2.12.1', sha256='c2af8b9bdd7657f4bd27b45336e7930171aead796711bc4cfc99b4731bb9d051')

    depends_on('python@3.5.3:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools-scm@3.4:+toml', type='build')
