# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelMpiBenchmarks(MakefilePackage):
    """Intel MPI Benchmarks provides a set of elementary benchmarks that
    conform to MPI-1, MPI-2, and MPI-3 standard. You can run all of
    the supported benchmarks, or a subset specified in the command
    line using one executable file. Use command-line parameters to
    specify various settings, such as time measurement, message
    lengths, and selection of communicators.

    """

    homepage = "https://software.intel.com/en-us/articles/intel-mpi-benchmarks"
    maintainers = ["carsonwoods"]

    version("2021.3", sha256="9b58a4a7eef7c0c877513152340948402fd87cb06270d2d81308dc2ef740f4c7")
    version("2021.2", sha256="ade3bfe18b4313a31fc09f0bf038e0a6c169c4145089bfc6f1f827687b81be6a")
    version("2021.1", sha256="9089bb81e3091af3481e03b898b339fb2d9fb6574d4ef059adb1f5410112b23a")
    version("2019.6", sha256="1cd0bab9e947228fced4666d907f77c51336291533919896a923cff5fcad62e9")
    version("2019.5", sha256="61f8e872a3c3076af53007a68e4da3a8d66be2ba7a051dc21e626a4e2d26e651")
    version("2019.4", sha256="aeb336be10275c1a2f579b491b6631122876b461ac7148b1d0764f13b7552690")
    version("2019.3", sha256="4f256d11bfed9ca6166548486d61a062e67be61f13dd9f30690232720e185f31")
    version("2019.2", sha256="0bc2224a913073aaa5958f6ae08341e5fcd39cedc6722a09bfd4a3d7591a340b")
    version("2019.1", sha256="fe0d065b9936b6943ea83cb3d00aede43b17565285c6b1791fee8e340853ef79")
    version("2019.0", sha256="1c7d44aa7fd86ca84ac7cae1a69a8426243048d6294582337f1de7b4ffe68d37")
    version("2018.1", sha256="718a4eb155f18cf15a736f6496332407b5837cf1f19831723d4cfe5266c43507")
    version("2018.0", sha256="2e60a9894a686a95791be2227bc569bf81ca3875421b5307df7d83f885b1de88")

    depends_on("mpi")

    # https://github.com/intel/mpi-benchmarks/pull/19
    patch("add_const.patch", when="@2019.1:2019.6")
    # https://github.com/intel/mpi-benchmarks/pull/20
    patch("reorder_benchmark_macros.patch", when="@2019.1:2019.6")

    variant(
        "benchmark",
        default="all",
        values=(
            "mpi1",
            "ext",
            "io",
            "nbc",
            "rma",
            "mt",
            "all",
            conditional("p2p", when="@2019.2:"),
        ),
        multi=False,
        description="Specify which benchmark to build",
    )

    def url_for_version(self, version):
        if version[0] <= 2019 and version[1] <= 1:
            url = "https://github.com/intel/mpi-benchmarks/archive/refs/tags/v{0}.tar.gz"
        else:
            url = "https://github.com/intel/mpi-benchmarks/archive/refs/tags/IMB-v{0}.tar.gz"
        return url.format(version)

    def build(self, spec, prefix):
        env["CC"] = spec["mpi"].mpicc
        env["CXX"] = spec["mpi"].mpicxx

        if "benchmark=mpi1" in spec:
            make("IMB-MPI1")
        elif "benchmark=ext" in spec:
            make("IMB-EXT")
        elif "benchmark=io" in spec:
            make("IMB-IO")
        elif "benchmark=nbc" in spec:
            make("IMB-NBC")
        elif "benchmark=p2p" in spec:
            make("IMB-P2P")
        elif "benchmark=rma" in spec:
            make("IMB-RMA")
        elif "benchmark=mt" in spec:
            make("IMB-MT")
        else:
            make("all")

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        if "benchmark=mpi1" in spec:
            install("IMB-MPI1", prefix.bin)
        elif "benchmark=ext" in spec:
            install("IMB-EXT", prefix.bin)
        elif "benchmark=io" in spec:
            install("IMB-IO", prefix.bin)
        elif "benchmark=nbc" in spec:
            install("IMB-NBC", prefix.bin)
        elif "benchmark=p2p" in spec:
            install("IMB-P2P", prefix.bin)
        elif "benchmark=rma" in spec:
            install("IMB-RMA", prefix.bin)
        elif "benchmark=mt" in spec:
            install("IMB-MT", prefix.bin)
        else:
            install("IMB-EXT", prefix.bin)
            install("IMB-IO", prefix.bin)
            install("IMB-MPI1", prefix.bin)
            install("IMB-MT", prefix.bin)
            install("IMB-NBC", prefix.bin)
            if spec.satisfies("@2019.2:"):
                install("IMB-P2P", prefix.bin)
            install("IMB-RMA", prefix.bin)
