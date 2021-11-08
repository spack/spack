# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpDataVisSdk(BundlePackage, CudaPackage):
    """ECP Data & Vis SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"

    tags = ['ecp']
    maintainers = ['chuckatkins']

    version('1.0')

    ############################################################
    # Variants
    ############################################################

    # I/O
    variant('adios2', default=False, description="Enable ADIOS2")
    variant('darshan', default=False, description="Enable Darshan")
    variant('faodel', default=False, description="Enable FAODEL")
    variant('hdf5', default=False, description="Enable HDF5")
    variant('pnetcdf', default=False, description="Enable PNetCDF")
    variant('unifyfs', default=False, description="Enable UnifyFS")
    variant('veloc', default=False, description="Enable VeloC")

    # Vis
    variant('ascent', default=False, description="Enable Ascent")
    variant('paraview', default=False, description="Enable ParaView")
    variant('sz', default=False, description="Enable SZ")
    variant('vtkm', default=False, description="Enable VTK-m")
    variant('zfp', default=False, description="Enable ZFP")

    # Cinema
    variant('cinema', default=False, description="Enable Cinema")

    # Outstanding build issues
    variant('catalyst', default=False, description="Enable Catalyst")
    conflicts('+catalyst')
    variant('visit', default=False, description="Enable VisIt")
    conflicts('+visit')

    # Wrapper around depends_on to propagate dependency variants
    def dav_sdk_depends_on(spec, when=None, propagate=None):
        # Do the basic depends_on
        depends_on(spec, when=when)

        # Skip if there is nothing to propagate
        if not propagate:
            return

        # Map the propagated variants to the dependency variant
        if not type(propagate) is dict:
            propagate = dict([(v, v) for v in propagate])

        # Strip spec string to just the base spec name
        # ie. A +c ~b -> A
        spec = Spec(spec).name

        # Determine the base variant
        base_variant = ''
        if when:
            base_variant = when

        def is_boolean(variant):
            return '=' not in variant

        # Propagate variants to dependecy
        for v_when, v_then in propagate.items():
            if is_boolean(v_when):
                depends_on('{0} +{1}'.format(spec, v_then),
                           when='{0} +{1}'.format(base_variant, v_when))
                depends_on('{0} ~{1}'.format(spec, v_then),
                           when='{0} ~{1}'.format(base_variant, v_when))
            else:
                depends_on('{0} {1}'.format(spec, v_then),
                           when='{0} {1}'.format(base_variant, v_when))

    def exclude_variants(variants, exclude):
        return [variant for variant in variants if variant not in exclude]

    ############################################################
    # Dependencies
    ############################################################
    cuda_arch_variants = ['cuda_arch={0}'.format(x)
                          for x in CudaPackage.cuda_arch_values]

    dav_sdk_depends_on('adios2+shared+mpi+fortran+python+blosc+sst+ssc+dataman',
                       when='+adios2',
                       propagate=['hdf5', 'sz', 'zfp'])

    dav_sdk_depends_on('darshan-runtime+mpi', when='+darshan')
    dav_sdk_depends_on('darshan-util', when='+darshan')

    dav_sdk_depends_on('faodel+shared+mpi network=libfabric',
                       when='+faodel',
                       propagate=['hdf5'])

    dav_sdk_depends_on('hdf5 +shared+mpi+fortran', when='+hdf5')

    dav_sdk_depends_on('parallel-netcdf+shared+fortran', when='+pnetcdf')

    dav_sdk_depends_on('unifyfs', when='+unifyfs ')

    dav_sdk_depends_on('veloc', when='+veloc')

    dav_sdk_depends_on('ascent+shared+mpi+fortran+openmp+python+vtkh+dray',
                       when='+ascent')

    dav_sdk_depends_on('catalyst', when='+catalyst')

    depends_on('py-cinemasci', when='+cinema')

    # +adios2 is not yet enabled in the paraview package
    paraview_base_spec = 'paraview+mpi+python3+kits'
    # Want +shared when not using cuda
    dav_sdk_depends_on(paraview_base_spec + '+shared ~cuda',
                       when='+paraview ~cuda',
                       propagate=['hdf5'])
    # Can't have +shared when using cuda, propagate cuda_arch_variants
    dav_sdk_depends_on(paraview_base_spec + '~shared +cuda',
                       when='+paraview +cuda',
                       propagate=cuda_arch_variants)

    dav_sdk_depends_on('visit', when='+visit')

    dav_sdk_depends_on('vtk-m+shared+mpi+openmp+rendering',
                       when='+vtkm',
                       propagate=['cuda'] + cuda_arch_variants)

    # +python is currently broken in sz
    # dav_sdk_depends_on('sz+shared+fortran+python+random_access',
    dav_sdk_depends_on('sz+shared+fortran+random_access',
                       when='+sz',
                       propagate=['hdf5'])

    dav_sdk_depends_on('zfp',
                       when='+zfp',
                       propagate=['cuda'] + cuda_arch_variants)
