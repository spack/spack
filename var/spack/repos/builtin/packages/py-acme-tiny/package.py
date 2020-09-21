# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAcmeTiny(PythonPackage):
    """A tiny script to issue and renew TLS certs from Let's Encrypt."""

    homepage = "https://github.com/diafygi/acme-tiny"
    git      = "https://github.com/diafygi/acme-tiny.git"

    version('master', branch='master')

    depends_on('py-setuptools-scm', type=('build', 'run'))
