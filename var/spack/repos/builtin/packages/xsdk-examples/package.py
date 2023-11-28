# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class XsdkExamples(CMakePackage, CudaPackage, ROCmPackage):
    """xSDK Examples show usage of libraries in the xSDK package."""

    homepage = "http://xsdk.info"
    url = "https://github.com/xsdk-project/xsdk-examples/archive/v0.1.0.tar.gz"
    git = "https://github.com/xsdk-project/xsdk-examples"

    maintainers("balay", "luszczek", "balos1", "shuds13", "v-dobrev")

    version("develop", branch="master")
    version("0.4.0", sha256="de54e02e0222420976a2f4cf0a6230e4bb625b443c66500fa1441032db206df9")
    version(
        "0.3.0",
        sha256="e7444a403c0a69eeeb34a4068be4d6f4e5b54cbfd275629019b9236a538a739e",
        deprecated=True,
    )

    depends_on("xsdk+cuda", when="+cuda")
    depends_on("xsdk~cuda", when="~cuda")
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on("xsdk+cuda cuda_arch={0}".format(sm_), when="+cuda cuda_arch={0}".format(sm_))
    depends_on("xsdk+rocm", when="+rocm")
    depends_on("xsdk~rocm", when="~rocm")
    for ac_ in ROCmPackage.amdgpu_targets:
        depends_on(
            "xsdk+rocm amdgpu_target={0}".format(ac_), when="+rocm amdgpu_target={0}".format(ac_)
        )

    depends_on("xsdk@develop", when="@develop")
    # Use ^dealii~hdf5 because of HDF5 linking issue in deal.II 9.4.0.
    # Disable 'arborx' to remove the 'kokkos' dependency which conflicts with
    # the internal Kokkos used by 'trilinos':
    depends_on("xsdk@0.8.0 ~arborx ^mfem+pumi ^dealii~hdf5", when="@0.4.0")
    depends_on("xsdk@0.8.0 ^mfem+strumpack", when="@0.4.0 ^xsdk+strumpack")
    depends_on("xsdk@0.8.0 ^mfem+ginkgo", when="@0.4.0 ^xsdk+ginkgo")
    depends_on("xsdk@0.8.0 ^mfem+hiop", when="@0.4.0 ^xsdk+hiop")
    depends_on("xsdk@0.8.0 ^sundials+magma", when="@0.4.0 +cuda")
    depends_on("xsdk@0.7.0", when="@0.3.0")
    depends_on("xsdk@0.7.0 ^mfem+strumpack", when="@0.3.0 ^xsdk+strumpack")
    depends_on("xsdk@0.7.0 ^sundials+magma", when="@0.3.0 +cuda")
    depends_on("mpi")
    depends_on("cmake@3.21:", type="build", when="@0.3.0:")

    def cmake_args(self):
        spec = self.spec

        def enabled(pkg):
            if type(pkg) is not list:
                return "ON" if "^" + pkg in spec else "OFF"
            else:
                return "ON" if all([("^" + p in spec) for p in pkg]) else "OFF"

        # Note: paths to the enabled packages are automatically added by Spack
        # to the variable CMAKE_PREFIX_PATH.
        args = [
            # Using the MPI wrappers for C and C++ may cause linking issues
            # when CUDA is enabled.
            # "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            # "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            # Use the Fortran MPI wrapper as a workaround for a linking issue
            # with some versions of apple-clang on Mac.
            "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            "-DENABLE_AMREX=" + enabled("amrex"),
            "-DENABLE_DEAL_II=" + enabled("dealii"),
            "-DENABLE_GINKGO=" + enabled("ginkgo"),
            "-DENABLE_HEFFTE=" + enabled("heffte"),
            "-DENABLE_HIOP=" + enabled("hiop"),
            "-DENABLE_HYPRE=ON",
            "-DENABLE_MAGMA=" + enabled("magma"),
            "-DENABLE_MFEM=ON",
            "-DENABLE_PETSC=ON",
            # ENABLE_PLASMA also needs Slate:
            "-DENABLE_PLASMA=" + enabled(["plasma", "slate"]),
            "-DENABLE_PRECICE=" + enabled("precice"),
            "-DENABLE_PUMI=ON",
            "-DENABLE_STRUMPACK=" + enabled("strumpack"),
            "-DENABLE_SUNDIALS=ON",
            "-DENABLE_SUPERLU=ON",
            "-DENABLE_TASMANIAN=" + enabled("tasmanian"),
            "-DENABLE_TRILINOS=" + enabled("trilinos"),
        ]

        if "+cuda" in spec:
            archs = ";".join(spec.variants["cuda_arch"].value)
            args.extend(["-DENABLE_CUDA=ON", "-DCMAKE_CUDA_ARCHITECTURES=%s" % archs])

        if "+rocm" in spec:
            archs = ";".join(spec.variants["amdgpu_target"].value)
            args.extend(["-DENABLE_HIP=ON", "-DCMAKE_HIP_ARCHITECTURES=%s" % archs])

        return args

    def check(self):
        with working_dir(self.builder.build_directory):
            ctest("--output-on-failure")
