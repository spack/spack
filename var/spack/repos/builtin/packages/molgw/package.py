# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from subprocess import run, PIPE
from os import getenv


class Molgw(MakefilePackage):
    """MOLGW is a code that implements the many-body perturbation theory (MBPT) to describe the excited electronic states in finite systems (atoms, molecules, clusters).
    MOLGW implements the GW approximation for the self-energy (ionization and affinity) and the Bethe-Salpeter equation for the optical excitations.
    MOLGW also applies the real-time time-dependent density-functional theory (RT-TDDFT).
    MOLGW employs standard Gaussian basis set.
    """

    homepage = "https://github.com/bruneval/molgw"
    url = "https://github.com/bruneval/molgw/archive/v3.2.tar.gz"
    git = "https://github.com/bruneval/molgw.git"

    maintainers("bruneval")

    # version("rolling-release", branch="master")
    version("3.2", sha256="a3f9a99db52d95ce03bc3636b5999e6d92b503ec2f4afca33d030480c3e10242")

    depends_on("blas")
    depends_on("lapack")
    depends_on("libxc@5:")
    depends_on("libcint+pypzpx+coulomb_erf")

    variant("openmp", default=False, description="Build with OpenMP support")

    variant("scalapack", default=False, description="Build with ScaLAPACK support")
    depends_on("scalapack", when="+scalapack")
    depends_on("mpi", when="+scalapack")

    # enforce scalapack capable mkl when asking +scalapack (and using intel-oneapi-mkl)
    depends_on("intel-oneapi-mkl+cluster", when="+scalapack ^intel-oneapi-mkl")
    # enforce threaded openblas when asking +openmp (and using openblas)
    depends_on("openblas threads=openmp", when="+openmp ^openblas")

    # variant('hdf5', default=False, description='Build with HDF5 support')
    # depends_on('hdf5', when='+hdf5')

    def _get_mkl_ld_flags(self, spec):
        mklroot = str(getenv("MKLROOT"))
        command = [mklroot + "/bin/intel64/mkl_link_tool", "-libs", "--quiet"]
        if "%intel" in spec or "%oneapi" in spec:
            command.extend(["-c", "intel_f"])
            if "+openmp" in spec:
                command.extend(["-o", "tbb"])
        elif "%gcc" in spec:
            command.extend(["-c", "gnu_f"])
            if "+openmp" in spec:
                command.extend(["-o", "gomp"])

        if "+scalapack" in spec:
            command.extend(["--cluster_library=scalapack"])
            if "openmpi" in spec:
                command.extend(["-m", "openmpi"])
            elif "mpich" in spec:
                command.extend(["-m", "mpich2"])
            elif "intelmpi" in spec:
                command.extend(["-m", "intelmpi"])
        # only works with recent python3
        # result = run(command,capture_output=True, text=True)
        # return result.stdout.strip()
        result = run(command, stdout=PIPE)
        return result.stdout.decode(encoding="utf-8").strip()

    def edit(self, spec, prefix):
        flags = {}
        flags["PREFIX"] = prefix

        # Set LAPACK and SCALAPACK
        if "^mkl" in spec:
            flags["LAPACK"] = self._get_mkl_ld_flags(spec)
        else:
            flags["LAPACK"] = spec["lapack"].libs.ld_flags
            if "+scalapack" in spec:
                flags["SCALAPACK"] = spec["scalapack"].libs.ld_flags

        # Set FC
        if "+scalapack" in spec:
            flags["FC"] = "{0}".format(spec["mpi"].mpifc)
        else:
            flags["FC"] = self.compiler.fc_names[0]

        # Set FCFLAGS
        if "%intel" in spec or "%oneapi" in spec:
            flags["FCFLAGS"] = "-fpp "
        else:
            flags["FCFLAGS"] = "-cpp "

        if self.compiler.flags.get("fflags") is not None:
            flags["FCFLAGS"] = " ".join(self.compiler.flags.get("fflags"))
        if "+openmp" in spec:
            flags["FCFLAGS"] = flags.get("FCFLAGS", "") + " {0}".format(self.compiler.openmp_flag)

        # Set CPPFLAGS
        if "+scalapack" in spec:
            flags["CPPFLAGS"] = flags.get("CPPFLAGS", "") + "-DHAVE_SCALAPACK -DHAVE_MPI "

        if "^mkl" in spec:
            flags["CPPFLAGS"] = flags.get("CPPFLAGS", "") + "-DHAVE_MKL "

        # Write configuration file
        with open("my_machine.arch", "w") as f:
            for k, v in flags.items():
                f.write(k + "=" + v + "\n")

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")
