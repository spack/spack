# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAboutTime(PythonPackage):
    """A cool helper for tracking time and throughput of
    code blocks, with beautiful human friendly renditions."""

    homepage = "https://github.com/rsalmei/about-time"
    pypi = "about-time/about-time-4.1.0.tar.gz"

    license("MIT")

    version(
        "4.2.1",
        sha256="8bbf4c75fe13cbd3d72f49a03b02c5c7dca32169b6d49117c257e7eb3eaee341",
        url="https://pypi.org/packages/fb/cd/7ee00d6aa023b1d0551da0da5fee3bc23c3eeea632fbfc5126d1fec52b7e/about_time-4.2.1-py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="fdf24423c4322ee32fa1338ff4b11f704b649427110290f94bfe4e16ad246f18",
        url="https://pypi.org/packages/fa/fe/d680887c70b9330741fb599bd0106500f9bc438c5995b516cac0d7ebfe50/about_time-4.1.0-py3-none-any.whl",
    )
    version(
        "3.1.1",
        sha256="96841beb3f9b5de1cbb323d2bdb0fa9abdecbc46f2d546b9b3c2483d23daa17a",
        url="https://pypi.org/packages/bc/3e/97d324a2161da150d5d8f979ffce526ebbb938dbaf9536caaf0c4efe3680/about_time-3.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@4:")
