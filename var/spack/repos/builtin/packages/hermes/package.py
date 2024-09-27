# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hermes(CMakePackage):
    """
    Hermes is a heterogeneous-aware, multi-tiered, dynamic, and distributed
    I/O buffering system that aims to significantly accelerate I/O performance.
    """

    homepage = "https://grc.iit.edu/research/projects/hermes"
    git = "https://github.com/HDFGroup/hermes.git"

    maintainers("lukemartinlogan", "hyoklee")

    version("master", branch="master", submodules=True)

    version(
        "1.2.1",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.2.1.tar.gz",
        sha256="d60ee5d6856dc1a1f389fb08f61252cc7736d1c38d3049043749640897fe3b6d",
    )
    version(
        "1.2.0",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.2.0.tar.gz",
        sha256="280379f393695462279c1af11371995d134f33998596812bd960d6f44a86c339",
    )
    version(
        "1.1.0",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.1.0.tar.gz",
        sha256="022df20d9e394754f6126dfcedd845afde879fcb2738d763f53657e59e058c1e",
    )
    version(
        "1.0.5-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.0.5-beta.tar.gz",
        sha256="1f3ba51a8beda4bc1314d6541b800de1525f5e233a6f498fcde6dc43562ddcb7",
    )
    version(
        "1.0.0-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.0.0-beta.tar.gz",
        sha256="301084cced32aa00532ab4bebd638c31b0512c881ffab20bf5da4b7739defac2",
    )
    version(
        "0.9.9-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.9-beta.tar.gz",
        sha256="d2e0025a9bd7a3f05d3ab608c727ed15d86ed30cf582549fe996875daf6cb649",
    )
    version(
        "0.9.8-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.8-beta.tar.gz",
        sha256="68e9a977c25c53dcab7d7f6ef0df96b2ba4a09a06aa7c4a490c67faa2a78f077",
    )
    version(
        "0.9.5-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.5-beta.tar.gz",
        sha256="f48d15591a6596e8e54897362ec2591bc71e5de92933651f4768145e256336ca",
    )
    version(
        "0.9.0-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.0-beta.tar.gz",
        sha256="abf258a52fa79729dfeb28559957abf8945f3ad37cadefb3bc685227c5f057a8",
    )

    variant("adios", default=False, description="Build Adios tests")
    variant("ares", default=False, description="Enable full libfabric install")
    variant("compress", default=False, description="Enable compression")
    variant("encrypt", default=False, description="Enable encryption")
    variant("mpiio", default=True, description="Enable MPI I/O adapter")
    variant("python", default=False, description="Build Python Wrapper")
    variant("stdio", default=True, description="Enable STDIO adapter")
    variant("vfd", default=False, description="Enable HDF5 VFD")
    variant("zmq", default=False, description="Build ZeroMQ tests")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("libelf")

    depends_on("hermes-shm@master+boost+cereal+mochi")

    depends_on("hermes-shm+adios", when="+adios")
    depends_on("hermes-shm+ares", when="+ares")
    depends_on("hermes-shm+compress", when="+compress")
    depends_on("hermes-shm+encrypt", when="+encrypt")
    depends_on("hermes-shm+mpiio", when="+mpiio")
    depends_on("hermes-shm+vfd", when="+vfd")
    depends_on("hermes-shm+zmq", when="+zmq")
    
    depends_on("py-jarvis-util", type="test")

    def cmake_args(self):
        args = []
        if "+mpiio" in self.spec:
            args.append("-DHERMES_ENABLE_MPIIO_ADAPTER=ON")
            if "openmpi" in self.spec:
                args.append("-DHERMES_OPENMPI=ON")
            elif "mpich" in self.spec:
                args.append("-DHERMES_MPICH=ON")
        if "+stdio" in self.spec:
            args.append("-DHERMES_ENABLE_STDIO_ADAPTER=ON")
        if "+vfd" in self.spec:
            args.append("-DHERMES_ENABLE_VFD=ON")
        if "+compress" in self.spec:
            args.append(self.define("HERMES_ENABLE_COMPRESSION", "ON"))
        if "+encrypt" in self.spec:
            args.append(self.define("HERMES_ENABLE_ENCRYPTION", "ON"))
        if "+adios" in self.spec:
            args.append(self.define("HERMES_ENABLE_ADIOS", "ON"))
        if "+python" in self.spec:
            args.append(self.define("HERMES_ENABLE_PYTHON", "ON"))
        return args

    def set_include(self, env, path):
        env.append_flags("CFLAGS", "-I{}".format(path))
        env.append_flags("CXXFLAGS", "-I{}".format(path))
        env.prepend_path("INCLUDE", "{}".format(path))
        env.prepend_path("CPATH", "{}".format(path))

    def set_lib(self, env, path):
        env.prepend_path("LIBRARY_PATH", path)
        env.prepend_path("LD_LIBRARY_PATH", path)
        env.append_flags("LDFLAGS", "-L{}".format(path))
        env.prepend_path("PYTHONPATH", "{}".format(path))

    def set_flags(self, env):
        self.set_include(env, "{}/include".format(self.prefix))
        self.set_include(env, "{}/include".format(self.prefix))
        self.set_lib(env, "{}/lib".format(self.prefix))
        self.set_lib(env, "{}/lib64".format(self.prefix))
        env.prepend_path("CMAKE_PREFIX_PATH", "{}/cmake".format(self.prefix))
        env.prepend_path("CMAKE_MODULE_PATH", "{}/cmake".format(self.prefix))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        self.set_flags(spack_env)

    def setup_run_environment(self, env):
        self.set_flags(env)
