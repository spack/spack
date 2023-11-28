# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDarshan(PythonPackage):
    """Python utilities to interact with Darshan log records of HPC applications."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan"
    pypi = "darshan/darshan-3.4.0.1.tar.gz"

    maintainers("jeanbez", "shanedsnyder")

    version("3.4.4.0", sha256="2d218a1b2a450934698a78148c6603e453c246ec852679432bf217981668e56b")
    version("3.4.3.0", sha256="e0708fc5445f2d491ebd381a253cd67534cef13b963f1d749dd605a10f5c0f8f")
    version("3.4.2.0", sha256="eb00eb758c96899c0d523b71eb00caa3b967509c27fd504c579ac8c9b521845c")
    version("3.4.1.0", sha256="41a033ebac6fcd0ca05b8ccf07e11191286dee923ec334b876a7ec8e8a6add84")
    version("3.4.0.1", sha256="0142fc7c0b12a9e5c22358aa26cca7083d28af42aeea7dfcc5698c56b6aee6b7")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@:63", type="build")
    depends_on("py-pytest-runner", type="build")
    depends_on("py-cffi", type=("build", "run"))
    # NOTE: SciPy is an indirect dependency needed for interpolate usage in pandas
    #       This indirect dependency was dropped starting with v3.4.1.0
    depends_on("py-scipy", when="@3.4.0.1", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-mako", type=("build", "run"))
    depends_on("py-humanize", when="@3.4.3.0:", type=("build", "run"))
    depends_on("py-pytest", type="test")

    # py-darshan depends on specific darshan-util versions corresponding
    # to the first 3 parts of the py-darshan version string
    # (i.e., py-darshan@3.4.3.0 requires darshan-util@3.4.3, etc.)
    for v in ["3.4.0", "3.4.1", "3.4.2", "3.4.3"]:
        depends_on(f"darshan-util@{v}", when=f"@{v}", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("./darshan/tests"):
            pytest = which("pytest")
            pytest()
