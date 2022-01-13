# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyChartStudio(PythonPackage):
    """Utilities for interfacing with plotly's Chart Studio."""

    homepage = "https://pypi.org/project/chart-studio/"
    url = "https://files.pythonhosted.org/packages/d3/06/cfe81ee02b37eeacb3c74efd2a3280d68d97835c6d55419f89d5a3f63934/chart-studio-1.1.0.tar.gz"

    version('1.1.0', sha256='a17283b62470306d77060b200f13f9749c807dd15613c113d36f8d057f5c7019')

    depends_on('py-setuptools', type='build')

    depends_on('py-plotly', type=('run'))
    depends_on('py-requests', type=('run'))
    depends_on('py-retrying@1.3.3:', type=('run'))
    depends_on('py-six', type=('run'))
