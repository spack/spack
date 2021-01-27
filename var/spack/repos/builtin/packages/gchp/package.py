# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gchp
#
# You can edit this file again by typing:
#
#     spack edit gchp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import shutil
import inspect


class Gchp(CMakePackage):
    """GEOS-Chem High Performance model of atmospheric chemistry"""

    homepage = "https://gchp.readthedocs.io/"
    url      = "https://github.com/geoschem/GCHP/archive/13.0.0-rc.0.tar.gz"

    maintainers = ['williamdowns']

    version('13.0.0-rc.0', git='https://github.com/geoschem/GCHP.git',
            commit='4bd15316faf4e5f06517d3a6b1df1986b1126d90',  submodules=True)
    # NOTE: Post-13.0.0-rc.0 versions will have fix that
    # allows these ESMF variants to be enabled
    depends_on('esmf@8.0.1: -lapack -pio -pnetcdf -xerces')
    depends_on('mpi@3')
    depends_on('netcdf-fortran')
    depends_on('cmake@3.13:')

    variant('omp',        default=False, description="OpenMP parallelization")
    variant('real8',      default=True,  description="REAL*8 precision")
    variant('apm',        default=False, description="APM Microphysics (Experimental)")
    variant('rrtmg',      default=False, description="RRTMG radiative transfer model")
    variant('luo_wetdep', default=False, description="Luo et al 2019 wet deposition scheme")
    variant('tomas',      default=False, description="TOMAS Microphysics (Experimental)")

    def cmake_args(self):
        args = ["-DRUNDIR=" + self.prefix,
                self.define_from_variant('OMP', 'omp'),
                self.define_from_variant('USE_REAL8', 'real8'),
                self.define_from_variant('APM', 'apm'),
                self.define_from_variant('RRTMG', 'rrtmg'),
                self.define_from_variant('LUO_WETDEP', 'luo_wetdep'),
                self.define_from_variant('TOMAS', 'tomas')]
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)
        # preserve source code structure for run directory creation
        # can be shortened later
        shutil.move(self.stage.source_path,
                    join_path(prefix, 'source_code'))
