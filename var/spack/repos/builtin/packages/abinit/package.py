# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Abinit(AutotoolsPackage):
    """ABINIT is a package whose main program allows one to find the total
    energy, charge density and electronic structure of systems made of
    electrons and nuclei (molecules and periodic solids) within
    Density Functional Theory (DFT), using pseudopotentials and a planewave
    or wavelet basis.

    ABINIT also includes options to optimize the geometry according to the
    DFT forces and stresses, or to perform molecular dynamics
    simulations using these forces, or to generate dynamical matrices,
    Born effective charges, and dielectric tensors, based on Density-Functional
    Perturbation Theory, and many more properties. Excited states can be
    computed within the Many-Body Perturbation Theory (the GW approximation and
    the Bethe-Salpeter equation), and Time-Dependent Density Functional Theory
    (for molecules). In addition to the main ABINIT code, different utility
    programs are provided.
    """

    homepage = "https://www.abinit.org/"
    url = "https://www.abinit.org/sites/default/files/packages/abinit-8.6.3.tar.gz"

    maintainers("downloadico")
    version("9.10.3", sha256="3f2a9aebbf1fee9855a09dd687f88d2317b8b8e04f97b2628ab96fb898dce49b")
    version("9.8.4", sha256="a086d5045f0093b432e6a044d5f71f7edf5a41a62d67b3677cb0751d330c564a")
    version("9.8.3", sha256="de823878aea2c20098f177524fbb4b60de9b1b5971b2e835ec244dfa3724589b")
    version("9.6.1", sha256="b6a12760fd728eb4aacca431ae12150609565bedbaa89763f219fcd869f79ac6")
    version("9.4.2", sha256="d40886f5c8b138bb4aa1ca05da23388eb70a682790cfe5020ecce4db1b1a76bc")
    version("8.10.3", sha256="ed626424b4472b93256622fbb9c7645fa3ffb693d4b444b07d488771ea7eaa75")
    version("8.10.2", sha256="4ee2e0329497bf16a9b2719fe0536cc50c5d5a07c65e18edaf15ba02251cbb73")
    version("8.8.2", sha256="15216703bd56a799a249a112b336d07d733627d3756487a4b1cb48ebb625c3e7")
    version("8.6.3", sha256="82e8d071088ab8dc1b3a24380e30b68c544685678314df1213180b449c84ca65")
    version("8.2.2", sha256="e43544a178d758b0deff3011c51ef7c957d7f2df2ce8543366d68016af9f3ea1")
    # Versions before 8.0.8b are not supported.
    version("8.0.8b", sha256="37ad5f0f215d2a36e596383cb6e54de3313842a0390ce8d6b48a423d3ee25af2")

    variant("mpi", default=True, description="Builds with MPI support. Requires MPI2+")
    variant("openmp", default=False, description="Enables OpenMP threads. Use threaded FFTW3")
    variant("scalapack", default=False, description="Enables scalapack support. Requires MPI")

    variant("wannier90", default=False, description="Enables the Wannier90 library")
    variant("libxml2", default=False, description="Enable libxml2 support, used by multibinit")

    variant(
        "optimization-flavor",
        default="standard",
        multi=False,
        values=("safe", "standard", "aggressive"),
        description="Select the optimization flavor to use.",
    )

    variant("install-tests", default=False, description="Install test cases")

    # Add dependencies
    depends_on("atompaw")
    depends_on("blas")
    depends_on("lapack")

    # Require MPI2+
    depends_on("mpi@2:", when="+mpi")

    depends_on("scalapack", when="+scalapack+mpi")

    depends_on("fftw-api")

    depends_on("netcdf-fortran")
    depends_on("netcdf-c+mpi", when="+mpi")
    depends_on("netcdf-c~mpi", when="~mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("hdf5~mpi", when="~mpi")
    # constrain version of hdf5
    depends_on("hdf5@:1.8", when="@9:")
    depends_on("wannier90+shared", when="+wannier90+mpi")

    # constrain libxc version
    depends_on("libxc")
    depends_on("libxc@:2", when="@:8")
    depends_on("libxc@:5", when="@9.8:")

    # libxml2
    depends_on("libxml2", when="@9:+libxml2")

    # If the Intel suite is used for Lapack, it must be used for fftw and vice-versa
    for _intel_pkg in INTEL_MATH_LIBRARIES:
        requires(f"^[virtuals=fftw-api] {_intel_pkg}", when=f"^[virtuals=lapack]   {_intel_pkg}")
        requires(f"^[virtuals=lapack]   {_intel_pkg}", when=f"^[virtuals=fftw-api] {_intel_pkg}")

    # Cannot ask for +scalapack if it does not depend on MPI
    conflicts("+scalapack", when="~mpi")

    # Cannot ask for +wannier90 if it does not depend on MPI
    conflicts("+wannier90", when="~mpi")

    # libxml2 needs version 9 and above
    conflicts("+libxml2", when="@:8")

    conflicts("%gcc@7:", when="@:8.8")
    conflicts("%gcc@9:", when="@:8.10")

    # need openmp threading for abinit+openmp
    # TODO: The logic here can be reversed with the new concretizer. Instead of
    # using `conflicts`, `depends_on` could be used instead.
    for fftw in ["amdfftw", "cray-fftw", "fujitsu-fftw", "fftw"]:
        conflicts("+openmp", when=f"^{fftw}~openmp", msg=f"Need to request {fftw} +openmp")

    mkl_message = "Need to set dependent variant to threads=openmp"
    conflicts("+openmp", when="^intel-mkl threads=none", msg=mkl_message)
    conflicts("+openmp", when="^intel-mkl threads=tbb", msg=mkl_message)
    conflicts("+openmp", when="^intel-parallel-studio +mkl threads=none", msg=mkl_message)

    conflicts(
        "+openmp", when="^fujitsu-ssl2 ~parallel", msg="Need to request fujitsu-ssl2 +parallel"
    )

    conflicts(
        "~openmp", when="^fujitsu-ssl2 +parallel", msg="Need to request fujitsu-ssl2 ~parallel"
    )

    patch("rm_march_settings.patch", when="@:8")
    patch("rm_march_settings_v9.patch", when="@9:")

    # Fix detection of Fujitsu compiler
    # Fix configure not to collect the option that causes an error
    # Fix intent(out) and unnecessary rewind to avoid compile error
    patch("fix_for_fujitsu.patch", when="@:8 %fj")
    patch("fix_for_fujitsu.v9.patch", when="@9: %fj")

    def configure_args(self):
        spec = self.spec

        options = []
        options += self.with_or_without("libxml2")

        oapp = options.append
        if "@:8" in spec:
            oapp(f"--enable-optim={self.spec.variants['optimization-flavor'].value}")
        else:
            oapp(f"--with-optim-flavor={self.spec.variants['optimization-flavor'].value}")

        if "+wannier90" in spec:
            if spec.satisfies("@:8"):
                oapp(f"--with-wannier90-libs=-L{spec['wannier90'].prefix.lib} -lwannier -lm")
                oapp(f"--with-wannier90-incs=-I{spec['wannier90'].prefix.modules}")
                oapp(f"--with-wannier90-bins={spec['wannier90'].prefix.bin}")
                oapp("--enable-connectors")
                oapp("--with-dft-flavor=atompaw+libxc+wannier90")
            elif spec.satisfies("@:9.8"):
                options.extend(
                    [
                        f"WANNIER90_CPPFLAGS=-I{spec['wannier90'].prefix.modules}",
                        f"WANNIER90_LIBS=-L{spec['wannier90'].prefix.lib} -lwannier",
                    ]
                )
            else:
                options.extend(
                    [
                        f"WANNIER90_CPPFLAGS=-I{spec['wannier90'].prefix.modules}",
                        f"WANNIER90_LIBS=-L{spec['wannier90'].prefix.lib}"
                        "WANNIER90_LDFLAGS=-lwannier",
                    ]
                )
        else:
            if "@:9.8" in spec:
                oapp(f"--with-fftw={spec['fftw-api'].prefix}")
                oapp(f"--with-hdf5={spec['hdf5'].prefix}")

            if "@:8" in spec:
                oapp("--with-dft-flavor=atompaw+libxc")
            else:
                "--without-wannier90",

        if "+mpi" in spec:
            oapp(f"CC={spec['mpi'].mpicc}")
            oapp(f"CXX={spec['mpi'].mpicxx}")
            if spec.satisfies("@9.8:"):
                oapp(f"F90={spec['mpi'].mpifc}")
            else:
                oapp(f"FC={spec['mpi'].mpifc}")

            # MPI version:
            # let the configure script auto-detect MPI support from mpi_prefix
            if "@:8" in spec:
                oapp("--enable-mpi=yes")
            else:
                oapp("--with-mpi")
        else:
            if "@:8" in spec:
                oapp("--enable-mpi=no")
            else:
                oapp("--without-mpi")

        # Activate OpenMP in Abinit Fortran code.
        if "+openmp" in spec:
            oapp("--enable-openmp=yes")
        else:
            oapp("--enable-openmp=no")

        # BLAS/LAPACK/SCALAPACK-ELPA
        linalg = spec["lapack"].libs + spec["blas"].libs
        is_using_intel_libraries = spec["lapack"].name in INTEL_MATH_LIBRARIES
        if is_using_intel_libraries:
            linalg_flavor = "mkl"
        elif "@9:" in spec and "^openblas" in spec:
            linalg_flavor = "openblas"
        elif "@9:" in spec and "^fujitsu-ssl2" in spec:
            linalg_flavor = "openblas"
        else:
            linalg_flavor = "custom"

        if "+scalapack" in spec:
            linalg = spec["scalapack"].libs + linalg
            if "@:8" in spec:
                linalg_flavor = f"scalapack+{linalg_flavor}"

        if "@:8" in spec:
            oapp(f"--with-linalg-libs={linalg.ld_flags}")
        else:
            oapp(f"LINALG_LIBS={linalg.ld_flags}")

        oapp(f"--with-linalg-flavor={linalg_flavor}")

        if is_using_intel_libraries:
            fftflavor = "dfti"
        else:
            if "+openmp" in spec:
                fftflavor, fftlibs = "fftw3-threads", "-lfftw3_omp -lfftw3 -lfftw3f"
            else:
                fftflavor, fftlibs = "fftw3", "-lfftw3 -lfftw3f"

        oapp(f"--with-fft-flavor={fftflavor}")

        if "@:8" in spec:
            if is_using_intel_libraries:
                oapp(f"--with-fft-incs={spec['fftw-api'].headers.cpp_flags}")
                oapp(f"--with-fft-libs={spec['fftw-api'].libs.ld_flags}")
            else:
                options.extend(
                    [
                        f"--with-fft-incs={spec['fftw-api'].headers.cpp_flags}",
                        f"--with-fft-libs=-L{spec['fftw-api'].prefix.lib} {fftlibs}",
                    ]
                )
        else:
            if is_using_intel_libraries:
                options.extend(
                    [
                        f"FFT_CPPFLAGS={spec['fftw-api'].headers.cpp_flags}",
                        f"FFT_LIBs={spec['fftw-api'].libs.ld_flags}",
                    ]
                )
            else:
                options.extend(
                    [
                        f"FFTW3_CPPFLAGS={spec['fftw-api'].headers.cpp_flags}",
                        f"FFTW3_LIBS=-L{spec['fftw-api'].prefix.lib} {fftlibs}",
                    ]
                )

        # LibXC library
        libxc = spec["libxc:fortran"]
        if "@:8" in spec:
            options.extend(
                [
                    f"--with-libxc-incs={libxc.headers.cpp_flags}",
                    f"--with-libxc-libs={libxc.libs.ld_flags + ' -lm'}",
                ]
            )
        else:
            oapp(f"--with-libxc={libxc.prefix}")

        # Netcdf4/HDF5
        hdf5 = spec["hdf5:hl"]
        netcdfc = spec["netcdf-c"]
        netcdff = spec["netcdf-fortran:shared"]
        if "@:8" in spec:
            oapp("--with-trio-flavor=netcdf")
            # Since version 8, Abinit started to use netcdf4 + hdf5 and we have
            # to link with the high level HDF5 library
            options.extend(
                [
                    "--with-netcdf-incs={}".format(
                        netcdfc.headers.cpp_flags + " " + netcdff.headers.cpp_flags
                    ),
                    "--with-netcdf-libs={}".format(
                        netcdff.libs.ld_flags + " " + hdf5.libs.ld_flags
                    ),
                ]
            )
        else:
            options.extend(
                [f"--with-netcdf={netcdfc.prefix}", f"--with-netcdf-fortran={netcdff.prefix}"]
            )

        if self.spec.satisfies("%fj"):
            oapp(f"FCFLAGS_MODDIR=-M{join_path(self.stage.source_path, 'src/mods')}")

        return options

    def check(self):
        """This method is called after the build phase if tests have been
        explicitly activated by user.
        """
        make("check")

        # the tests directly execute abinit. thus failing with MPI
        # TODO: run tests in tests/ via the builtin runtests.py
        #       requires Python with numpy, pyyaml, pandas
        if "~mpi" in self.spec:
            make("tests_in")

    def install(self, spec, prefix):
        make("install")
        if "+install-tests" in spec:
            install_tree("tests", spec.prefix.tests)
