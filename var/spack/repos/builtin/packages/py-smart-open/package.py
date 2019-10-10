# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySmartOpen(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "https://files.pythonhosted.org/packages/37/c0/25d19badc495428dec6a4bf7782de617ee0246a9211af75b302a2681dea7/smart_open-1.8.4.tar.gz"

    version('1.8.4', sha256='788e07f035defcbb62e3c1e313329a70b0976f4f65406ee767db73ad5d2d04f9')

    depends_on('py-setuptools', type='build')
    depends_on('py-boto3', type=('build', 'run'))
