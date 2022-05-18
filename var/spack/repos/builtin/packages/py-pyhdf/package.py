# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyhdf(PythonPackage):
    """pyhdf is a python wrapper around the NCSA HDF version 4 library.
    The SD (Scientific Dataset), VS (Vdata) and V (Vgroup) API’s are
    currently implemented. NetCDF files can also be read and modified."""

    homepage = "https://github.com/fhs/pyhdf"
    pypi     = "pyhdf/pyhdf-0.10.4.tar.gz"
    git      = "https://github.com/fhs/pyhdf.git"
    #maintainers = []

    version('master', branch='master')
    version('0.10.4', sha256='ea09b2bdafc9be0f7f43d72ff122d8efbde61881f4da3a659b33be5e29215f93')

    # Python versions
    depends_on('python@3.2:', type=('build', 'run'))

    # Dependencies
    depends_on('zlib', type=('build', 'run'))
    depends_on('hdf', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('jpeg', type=('build', 'run'))

    def setup_build_environment(self, env):
        inc_dirs = []
        lib_dirs = []
        # Strip -I and -L from spec include_flags / search_flags
        inc_dirs.append(self.spec['hdf'].headers.include_flags.lstrip('-I'))
        inc_dirs.append(self.spec['jpeg'].headers.include_flags.lstrip('-I'))
        lib_dirs.append(self.spec['hdf'].libs.search_flags.lstrip('-L'))
        lib_dirs.append(self.spec['jpeg'].libs.search_flags.lstrip('-L'))
        env.set('INCLUDE_DIRS', ':'.join(inc_dirs))
        env.set('LIBRARY_DIRS', ':'.join(lib_dirs))
        if self.spec['hdf'].satisfies('@:4.1'):
            env.set('NO_COMPRESS', '1')
