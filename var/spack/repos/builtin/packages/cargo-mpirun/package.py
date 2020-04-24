# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CargoMpirun(CargoPackage):
    """`cargo mpirun` allows you to easily build and run your MPI applications
    in a single command. It emulates `cargo run`, allowing you to specify a
    target to be built and run, and cargo takes care of the rest."""

    homepage  = "https://crates.io/crates/cargo-mpirun"
    crates_io = "cargo-mpirun"
    git       = "https://github.com/AndrewGaspar/cargo-mpirun.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.1.8', sha256='18ef8a141344a81cc80e1f889257c78d620a9c958a1c0b0581299c3e194c0eef')
    version('0.1.7', sha256='6708806285344dbb65f57d3d070f8edab54ffff9fdf93f2edd1dcac3ab5bff27')
    version('0.1.6', sha256='e49bfdc4a712054885f69223dc18fa1721129ecaa4c5469750fc97b1c79a1e76')
    version('0.1.5', sha256='98947017401d9d91735eadadecb39c1b26aa26c39fdfa7137f1f3705b3dc6154')
    version('0.1.4', sha256='1f03b0e7fe0c86f30de1de388cbee52009bfed27febb5919fb9d1f050dc12016')
    version('0.1.3', sha256='367207036f9049f18006c8389d2539ac3e230fe93c749ff74d527c678331f795')
    version('0.1.2', sha256='6d73b4ccfb1c88ef4818d7cd477a53436eb184b69e200631170eeed8a536b30f')
    version('0.1.1', sha256='cb5561a3cfb4961cbafe04aadd78a9db3b90f49fa3e05ef5f43a5feebec9f2e8')
    version('0.1.0', sha256='cdab1114b1e120149b3a5695ba1822041081ab8e1e2894685238d96d9498664e')
