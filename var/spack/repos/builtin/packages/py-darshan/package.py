# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDarshan(PythonPackage):
    """Python utilities to interact with Darshan log records of HPC applications."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan"
    pypi = "darshan/darshan-3.4.0.1.tar.gz"

    maintainers = ["jeanbez", "shanedsnyder"]

    version("3.4.0.1", sha256="0142fc7c0b12a9e5c22358aa26cca7083d28af42aeea7dfcc5698c56b6aee6b7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cffi", type=("build", "run"))
    # NOTE: SciPy is an indirect dependency needed for interpolate usage in pandas
    #       It will be fixed in the next release
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    # NOTE: matplotlib should be pinned until next release, for details:
    #       https://github.com/darshan-hpc/darshan/issues/742
    depends_on("py-matplotlib@3.4", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-mako", type=("build", "run"))
    depends_on("py-pytest", type="test")
    # NOTE: lxml is test-only indirect dependency via pandas
    #       It will become optional in the next release
    depends_on("py-lxml", type=("test"))

    depends_on("darshan-util", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("./darshan/tests"):
            pytest = which("pytest")
            pytest()
