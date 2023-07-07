# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Itk(CMakePackage, PythonExtension):
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
    url = "https://github.com/InsightSoftwareConsortium/ITK/releases/download/v5.1.1/InsightToolkit-5.1.1.tar.gz"

    version("5.3.0", sha256="57a4471133dc8f76bde3d6eb45285c440bd40d113428884a1487472b7b71e383")
    version(
        "5.3rc02",
        sha256="163aaf4a6cecd5b70ff718c1a986c746581797212fd1b629fa81f12ae4756d14",
        deprecated=True,
    )
    version("5.2.1", sha256="192d41bcdd258273d88069094f98c61c38693553fd751b54f8cda308439555db")
    version("5.2.0", sha256="12c9cf543cbdd929330322f0a704ba6925a13d36d01fc721a74d131c0b82796e")
    version("5.1.2", sha256="f1e5a78e11125348f68f655c6b89b617c3a8b2c09f710081f621054811a70c98")
    version("5.1.1", sha256="39e2a63840054361b728878a35b21bbe38374682ffb4b5c4f8f8f7514dedb58e")

    variant("review", default=False, description="enable modules under review")
    variant("rtk", default=False, description="build the RTK (Reconstruction Toolkit module")
    variant("minc", default=False, description="enable support for MINC files")
    variant("antspy", default=False, description="enable support features for antspy")
    variant("python", default=False, description="enable Python bindings")

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

    depends_on("git", type="build")
    depends_on("perl", type="build")

    depends_on("eigen")
    depends_on("expat")
    depends_on("fftw-api")
    depends_on("googletest")
    depends_on("hdf5+cxx+hl")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("mpi")
    depends_on("zlib")
    depends_on("py-numpy", when="+python")
    extends("python", when="+python")

    conflicts("+minc", when="+python")

    # The np.bool alias was removed in numpy-1.24.0. Patch to use np.bool_
    # instead.
    patch("bool_5.1.patch", when="@5.1 ^py-numpy@1.24:")
    patch("bool_5.2.patch", when="@5.2 ^py-numpy@1.24:")
    # Version 5.3 uses np.bool8 but that is deprecated as of numpy-1.24.0 so
    # patch this as well. Versions after 5.3 will use np.bool_ so patches will
    # not be needed for this after 5.3.
    patch("bool_5.3.patch", when="@5.3 ^py-numpy@1.24:")

    def cmake_args(self):
        use_mkl = "^mkl" in self.spec
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("ITK_USE_SYSTEM_LIBRARIES", True),
            self.define("ITK_USE_MKL", use_mkl),
            self.define_from_variant("Module_ITKReview", "review"),
            self.define_from_variant("Module_RTK", "rtk"),
            self.define_from_variant("Module_ITKIOMINC", "minc"),
            self.define_from_variant("Module_ITKIOTransformMINC", "minc"),
            self.define_from_variant("Module_MGHIO", "antspy"),
            self.define_from_variant("Module_GenericLabelInterpolator", "antspy"),
            self.define_from_variant("Module_AdaptiveDenoising", "antspy"),
        ]

        if not use_mkl:
            args.extend(
                [
                    self.define("USE_FFTWD", True),
                    self.define("USE_FFTWF", True),
                    self.define("USE_SYSTEM_FFTW", True),
                ]
            )

        if "+python" in self.spec:
            args.extend(
                [
                    self.define("ITK_WRAP_PYTHON", True),
                    self.define("PY_SITE_PACKAGES_PATH", python_platlib),
                ]
            )

        return args
