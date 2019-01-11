# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Percept(CMakePackage):
    """Parallel mesh refinement and adaptivity tools for the finite
    element method.
    """

    homepage = "https://github.com/PerceptTools/percept"
    git      = "https://github.com/PerceptTools/percept.git"

    # This package file was created at percept
    # commit dc1c8ec0175213146ac139946beca185a84c22e8
    version('develop', branch='master')

    depends_on('googletest~shared')
    depends_on('opennurbs@percept')
    depends_on('boost+graph+mpi')
    depends_on('yaml-cpp+pic~shared@0.5.3:')
    # Percept was initially tested against Trilinos 12.12.1
    depends_on('trilinos~shared+exodus+tpetra+epetra+muelu+belos+ifpack2+amesos2+zoltan+stk+boost~superlu-dist+superlu+hdf5+zlib+pnetcdf+aztec+sacado~openmp+shards+intrepid+cgns@master,12.12.1:')

    patch('fix_cmakelists.patch')
    patch('fix_header.patch')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DSTK_PERCEPT_LITE:BOOL=OFF',
            '-DSTK_ADAPT_HAVE_YAML_CPP:BOOL=ON',
            '-DTrilinos_DIR:PATH=%s' %
            spec['trilinos'].prefix,
            '-DYAML_DIR:PATH=%s' %
            spec['yaml-cpp'].prefix,
            '-DBOOST_DIR:PATH=%s' %
            spec['boost'].prefix,
            '-DOPENNURBS_DIR:PATH=%s' %
            spec['opennurbs'].prefix,
            '-DOPENNURBS_INCLUDE_DIR:PATH=%s' %
            spec['opennurbs'].prefix.include,
            '-DOPENNURBS_LIBRARY_DIR:PATH=%s' %
            spec['opennurbs'].prefix.lib,
            '-DPERCEPT_TPLS_INSTALL_DIR:PATH=%s' %
            spec['googletest'].prefix,
            '-DENABLE_INSTALL:BOOL=ON'
        ])

        return options
