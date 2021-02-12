# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHpccm(PythonPackage):
    """HPC Container Maker (HPCCM - pronounced H-P-see-M) is an open source
    tool to make it easier to generate container specification files."""

    homepage = "https://github.com/NVIDIA/hpc-container-maker"
    pypi = "hpccm/hpccm-19.2.0.tar.gz"

    version('21.1.0',  sha256='ffb3fe970dbb098ca97574c21bc317e12c99f3334d7d33fc7b5dfcce99a79945')
    version('20.12.0', sha256='836891f661a1d4858654691af6fad9f8a1bb1c3d241baa4bffbfa8e6c90f2e05')
    version('20.11.0', sha256='33667f924a9c70dea66a9bf928e683e5476eedca1b48b7f4cf0b9301d9af3c6b')
    version('20.10.0', sha256='2b0d37d32a74ba82511622c87fa037a3178c9ef8fc4d1287772afb643b73aac8')
    version('20.9.0',  sha256='d37c5c43ed4d092211359f58fe760136005e9237d136d5764d6207bcff0ac84b')
    version('20.8.0',  sha256='16b2e8a84d7dba38afde61fb4e1d9c8da6d5dcf6b2550eb817d2d3a9d877c3fb')
    version('20.7.0',  sha256='85e4f1e9f05ec848c4a95df18fe55f4e70c7381f797a2f6d915b73bee14f1bb7')
    version('20.6.0',  sha256='e5e6b1d6553165b2a1a5766abf1a405e4b207cc77aa012e092b106975b821e16')
    version('20.5.0',  sha256='93bba358d9c65b5d60d04747464b13d4c5b044ebcd6b6d71885f1cf965e0104d')
    version('20.4.0',  sha256='783644256d927a7a71a82ce2c46e957c8d7ac7a97e944e301b73f45ca59186cc')
    version('20.3.0',  sha256='91ea6e8048f257bb8797eb3387665fa94e2778c8e2ae752716e5926bb8d65f57')
    version('20.2.0',  sha256='16c8e35f35d2cd5ca11757dc188de5c8e90000f8d0c607c9d8ae417f1be6823a')
    version('20.1.0',  sha256='ff2cfe4f4472ae7b5920671b7339c81ae6ad50bb39fab23cb7f20be568ae48d7')
    version('19.12.0', sha256='665d52cc07fb3b13da1fcd038d878725b7e3142bfe452d236bacc37282b2ce03')
    version('19.11.0', sha256='0e873ef0bc645216ff08acaeb1b708acf9f7c5da9f29db9feaa9a110d790f5bb')
    version('19.10.0', sha256='134285772786f81bc01977caab23fed0fa725d78868de3c9008e65581ea9b99b')
    version('19.9.0',  sha256='f630cd3676b155c85fd923322d916ca997ca2c2d99d5592bc5359069d205f02b')
    version('19.8.0',  sha256='3d17d03b309e24701443e3ba1c89bc122203d7ab4bf614ee8e57c6610f25a04e')
    version('19.7.0',  sha256='666d3d91fe6e350a8d2ad3498b6f79349a9c1a4e8c252235b9dbe17fb3f66e00')
    version('19.6.0',  sha256='fa1cdebe9713ea5cf136e996d054ae30f6a1e202c7dffbfcea7178825e1fda92')
    version('19.5.1',  sha256='5d84dda9c1a538e8c01d267fb80625fb1d80375dca961c0dd800e6c6554fe792')
    version('19.5.0',  sha256='1cddf2e66fbf8f529e9f0d97fa2b95bc6775c646af6a1b4c2746f17249246d64')
    version('19.4.0',  sha256='73c31e694566d0b31ec423a243f1701e9d08372be15c3b5f38477dce043c4efd')
    version('19.3.0',  sha256='caf11f7a837d38deb6c0e91d0735e0a69666ae2bd6f7acd2975021840e679941')
    version('19.2.0', sha256='c60eec914a802b0a76596cfd5fdf7122d3f8665fcef06ef928323f5dfb5219a6')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
