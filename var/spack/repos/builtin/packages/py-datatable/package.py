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
    git      = "https://github.com/h2oai/datatable.git"

    # Use the version of the package as of the following git commit
    # since v0.8.0 yields a run time error. See the following ticket:
    # https://github.com/h2oai/datatable/issues/1875#issuecomment-504695182
    # the below commit was pushed on 2019 June 21
    version('master', git=git, commit='b533b487e26519e586a0231641d82576f322a683')

    depends_on('python@3.5.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-llvmlite',   type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-psutil',     type=('build', 'run'))
    depends_on('py-xlrd',       type=('build', 'run'))
    depends_on('py-blessed',    type=('build', 'run'))
    depends_on('py-typesentry', type=('build', 'run'))

    def setup_py(self, *args, **kwargs):
        setup = self.setup_file()

        with working_dir(self.build_directory):
            self.python('-s', setup, *args, **kwargs)
