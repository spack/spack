# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter


class PyZfit(PythonPackage):
    """
    scalable pythonic model fitting for high energy physics
    """

    homepage = "https://github.com/zfit/zfit"
    pypi = "zfit/zfit-0.15.5.tar.gz"

    version("0.18.0", sha256="21d9479480f74945c67707b715780693bd4e94062c551bf41fe04a2eddb47fab")
    version("0.17.0", sha256="cd60dfc360c82666af4e8dddd78edb0ab95a095b9dd0868457f0981dc03afa5a")
    version("0.16.0", sha256="b3b170af23b61d7e265d6fb1bab1d052003f3fb41b3c537527cc1e5a1066dc10")
    version('0.15.5', sha256='00a1138429e8a7f830c9e229b9c0bcd6071b95dadd8c87eb81191079fb679225')
    version('0.14.1', sha256='66d1e349403f1d6c6350138d0f2b422046bcbdfb34fd95453dadae29a8b0c98a')
    version('0.13.2', sha256='4935304c458e9e01fe4b931e5f6281f7d232397c9e3b76981c1800abc9b2f359')
    version('0.12.1', sha256='2c51a618b4658b06a94f5f2bb24586fdbd81fa06cf5baa65dd8ebbd1778f8029')
    version('0.11.1', sha256='6d2880cb4358796fa77473d29ced180e72e824fba2a88f534ea7c6814ab5d280')

    # depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    
    # depends_on('py-setuptools', type='build')
