# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDatabricksCli(PythonPackage):
    """A command line interface for Databricks."""

    homepage = "https://pypi.org/project/databricks-cli/"
    url = "https://files.pythonhosted.org/packages/bc/af/631375abc29e59cedfa4467a5f7755503ba19898890751e1f2636ef02f92/databricks-cli-0.14.3.tar.gz"

    version('0.14.3', sha256='bdf89a3917a3f8f8b99163e38d40e66dc478c7408954747f145cd09816b05e2c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-click@6.7:', type=('run'))
    depends_on('py-requests@2.17.3:', type=('run'))
    depends_on('py-tabulate@0.7.7:', type=('run'))
    depends_on('py-six@1.10.0:', type=('run'))
