# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyWasabi(PythonPackage):
    """wasabi: A lightweight console printing and formatting toolkit."""

    homepage = "https://ines.io/"
    pypi = "wasabi/wasabi-0.6.0.tar.gz"

    version('0.8.2', sha256='b4a36aaa9ca3a151f0c558f269d442afbb3526f0160fd541acd8a0d5e5712054')
    version('0.8.1', sha256='6e5228a51f5550844ef5080e74759e7ecb6e344241989d018686ba968f0b4f5a')
    version('0.8.0', sha256='75fec6db6193c8615d7f398ae4aa2c4ad294e6e3e81c6a6dbbbd3864ee2223c3')
    version('0.7.1', sha256='ee3809f4ce00e1e7f424b1572c753cff0dcaca2ca684e67e31f985033a9f070b')
    version('0.7.0', sha256='e875f11d7126a2796999ff7f092195f24005edbd90b32b2df16dde5d392ecc8c')
    version('0.6.0', sha256='b8dd3e963cd693fde1eb6bfbecf51790171aa3534fa299faf35cf269f2fd6063')

    depends_on('py-setuptools', type='build')
