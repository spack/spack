# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class HermesShm(CMakePackage):
    homepage = "https://github.com/lukemartinlogan/hermes_shm/wiki"
    git = "https://github.com/lukemartinlogan/hermes_shm.git"

    maintainers("lukemartinlogan", "hyoklee")

    version("master", branch="master")
    version(
        "1.1.0",
        url="https://github.com/lukemartinlogan/hermes_shm/archive/refs/tags/v1.1.0.tar.gz",
        sha256="080d5361cff22794b670e4544c532926ca8b6d6ec695af25596efe035bfffea5",
    )
    version(
        "1.0.0",
        url="https://github.com/lukemartinlogan/hermes_shm/archive/refs/tags/v1.0.0.tar.gz",
        sha256="a79f01d531ce89985ad59a2f62b41d74c2385e48d929e2f4ad895ae34137573b",
    )

    # Main variants
    variant("debug", default=False, description="Build shared libraries")
    variant("mochi", default=True, description="Build with mochi-thallium support")
    variant("cereal", default=True, description="Build with cereal support")
    variant("boost", default=True, description="Build with boost support")
    variant("mpiio", default=True, description="Build with MPI support")
    variant("vfd", default=False, description="Build with HDF5 support")
    variant("zmq", default=False, description="Build ZeroMQ tests")
    variant("adios", default=False, description="Build Adios support")

    # Required deps
    depends_on("catch2@3.0.1")
    depends_on("yaml-cpp")
    depends_on("doxygen@1.9.3")
    depends_on("libelf")

    # Machine variants
    variant("ares", default=False, description="Build in ares")
    depends_on("libfabric fabrics=sockets,tcp,udp,verbs,mlx,rxm,rxd,shm", when="+ares")

    # Main dependencies
    depends_on("mochi-thallium+cereal@0.10.1", when="+mochi")
    depends_on("cereal", when="+cereal")
    depends_on(
        "boost@1.7: +context +fiber +coroutine +regex +system \
    +filesystem +serialization +pic +math",
        when="+boost",
    )
    depends_on("mpi", when="+mpiio")
    depends_on("hdf5@1.14.0", when="+vfd")
    depends_on("libzmq", "+zmq")
    depends_on("adios2", when="+adios")

    # Compress variant
    variant("compress", default=False, description="Build with compression support")
    depends_on("lzo", when="+compress")
    depends_on("bzip2", when="+compress")
    depends_on("zstd", when="+compress")
    depends_on("lz4", when="+compress")
    depends_on("zlib", when="+compress")
    depends_on("xz", when="+compress")
    depends_on("brotli", when="+compress")
    depends_on("snappy", when="+compress")
    depends_on("c-blosc2", when="+compress")

    # Encryption variant
    variant("encrypt", default=False, description="Build with encryption support")
    depends_on("openssl", when="+encrypt")

    def cmake_args(self):
        args = []
        if "+debug" in self.spec:
            args.append("-DCMAKE_BUILD_TYPE=Debug")
        if "+vfd" in self.spec:
            args.append(self.define("HERMES_ENABLE_VFD", "ON"))
        if "+compress" in self.spec:
            args.append(self.define("HERMES_ENABLE_COMPRESSION", "ON"))
        if "+encrypt" in self.spec:
            args.append(self.define("HERMES_ENABLE_ENCRYPTION", "ON"))
        if "+mochi" in self.spec:
            args.append(self.define("HERMES_RPC_THALLIUM", "ON"))
        if "+zmq" in self.spec:
            args.append(self.define("HERMES_ENABLE_ZMQ_TESTS", "ON"))
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
