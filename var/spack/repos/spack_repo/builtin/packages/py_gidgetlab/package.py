# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGidgetlab(PythonPackage):
    """An asynchronous GitLab API library."""

    homepage = "https://gitlab.com/beenje/gidgetlab"
    pypi = "gidgetlab/gidgetlab-1.1.0.tar.gz"
    git = "https://gitlab.com/beenje/gidgetlab.git"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("main", branch="main")
    version("2.1.0", sha256="60c39516261b788e7643ae12fae106a79329450d908e821c9a591ab6c52ffe95")
    version("2.0.1", sha256="bce8f8553c41823bff330eb9e1f0951f19feb7fc76a9effe3038f780377d984e")
    version("2.0.0", sha256="f109c12a47c4b2cadd5485c6574d003807a07796585d75a21bd9e0d4ecd63c14")
    version("1.1.0", sha256="314ec2cddc898317ec45d99068665dbf33c0fee1f52df6671f28ad35bb51f902")

    variant(
        "aiohttp", default=False, description="Enable aiohttp functionality through dependency."
    )
    depends_on("python@:3.12", type=("build", "run"), when="@:1")

    depends_on("py-setuptools@60:", type=("build", "run"), when="@2.0.0:")
    depends_on("py-setuptools@45:", type=("build", "run"))
    depends_on("py-setuptools-scm@8.0:", type="build", when="@2.0.0:")
    depends_on("py-setuptools-scm@6.2:", type="build")

    depends_on("py-aiohttp", type=("build", "run"), when="+aiohttp")
    depends_on("py-cachetools", type=("build", "run"), when="+aiohttp")
