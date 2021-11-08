# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Itk(CMakePackage):
    """The Insight Toolkit (ITK) is an open-source, cross-platform toolkit for
    N-dimensional scientific image processing, segmentation, and registration.

    The Insight Toolkit (ITK) is an open-source, cross-platform toolkit for
    N-dimensional scientific image processing, segmentation, and registration.
    Segmentation is the process of identifying and classifying data found in a
    digitally sampled representation. Typically the sampled representation is
    an image acquired from such medical instrumentation as CT or MRI scanners.
    Registration is the task of aligning or developing correspondences between
    data. For example, in the medical environment, a CT scan may be aligned
    with a MRI scan in order to combine the information contained in both."""

    homepage = "https://itk.org/"
    url      = "https://github.com/InsightSoftwareConsortium/ITK/releases/download/v5.1.1/InsightToolkit-5.1.1.tar.gz"

    maintainers = ['glennpj']

    version('5.2.1', sha256='192d41bcdd258273d88069094f98c61c38693553fd751b54f8cda308439555db')
    version('5.2.0', sha256='12c9cf543cbdd929330322f0a704ba6925a13d36d01fc721a74d131c0b82796e')
    version('5.1.2', sha256='f1e5a78e11125348f68f655c6b89b617c3a8b2c09f710081f621054811a70c98')
    version('5.1.1', sha256='39e2a63840054361b728878a35b21bbe38374682ffb4b5c4f8f8f7514dedb58e')

    variant('review', default=False, description='enable modules under review')
    variant('rtk', default=False,
            description='build the RTK (Reconstruction Toolkit module')

    # TODO: This will not work if the resource is pulled from a spack mirror.
    # The build process will checkout the appropriate commit but it needs to be
    # a git repository. The copy pulled from the mirror is not a git
    # repository.
    # NOTE: This problem is reflected in issues #8746 and #14344 and PR #9436.
    # resource(
    #     name='RTK',
    #     git='https://github.com/SimonRit/RTK.git',
    #     get_full_repo=True,
    #     destination='Modules/Remote',
    #     when='+rtk',
    # )

    depends_on('git', type='build')
    depends_on('perl', type='build')

    depends_on('eigen')
    depends_on('expat')
    depends_on('fftw-api')
    depends_on('googletest')
    depends_on('hdf5+cxx')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('zlib')

    def cmake_args(self):
        force = CMakePackage.define
        from_variant = self.define_from_variant
        use_mkl = '^mkl' in self.spec

        args = [
            force('BUILD_SHARED_LIBS', True),
            force('ITK_USE_SYSTEM_LIBRARIES', True),
            force('ITK_USE_MKL', use_mkl),
            from_variant('Module_ITKReview', 'review'),
            from_variant('Module_RTK', 'rtk'),
        ]

        if not use_mkl:
            args.extend([
                force('USE_FFTWD', True),
                force('USE_FFTWF', True),
                force('USE_SYSTEM_FFTW', True),
            ])

        return args
