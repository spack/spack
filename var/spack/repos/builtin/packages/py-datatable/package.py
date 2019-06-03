# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyDatatable(PythonPackage):
    """This is a Python package for manipulating 2-dimensional tabular data
structures (aka data frames). It is close in spirit to pandas or SFrame; 
however we put specific emphasis on speed and big data support. As the name
 suggests, the package is closely related to R's data.table and attempts to 
mimic its core algorithms and API.
"""

    homepage = "https://github.com/h2oai/datatable"
    url      = "https://github.com/h2oai/datatable/archive/v0.8.0.tar.gz"

    version('0.8.0', sha256='42ecf2ca4f256c8e4c015af865cce5fec9566ceb3ed5c601de24697dd38642a6')

    depends_on('python@3.5.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-llvmlite',   type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-psutil',     type=('build', 'run'))
    depends_on('py-xlrd',       type=('build', 'run'))
    # depends_on('py-blessed',    type=('build', 'run'))
    # depends_on('py-typesentry', type=('build', 'run'))
