# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitsOdes(PythonPackage):
    """Odes is a scikit toolkit for scipy to add extra ode solvers.
    Specifically it interfaces the Sundials solvers cvode, cvodes, ida and
    idas.  It this way it provides extra modern ode and dae solvers you can
    use, extending the capabilities offered in scipy.integrade.ode."""

    homepage = "https://github.com/bmcage/odes"

    pypi = "scikits.odes/scikits.odes-2.7.0.tar.gz"
    git = "https://github.com/bmcage/odes.git"

    maintainers("omsai")

    version("2.7.0", sha256="a71e19e1485893754ae8c050668232fcc694f17b83602e75fbebf7bf9f975e1e")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("py-setuptools@:64.0.0", type="build")

    # Upstream incorrectly only lists py-numpy only as a build dependency even
    # though it is directly imported.
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-cython@:2", type="build")
    # Although upstream's documentation claims support for sundials@5.1:
    # py-scikit-odes@2.7.0 requires the header sundials/sundials_context.h
    # which wasn't added until sundials@6
    depends_on("sundials@6:")

    depends_on("py-pytest", type="test")

    # Remove numpy test runner imports to be compatible with py-numpy@1.25:
    patch(
        "https://github.com/bmcage/odes/commit/57466a97a278f687a6b0a92343b767c495834b31.patch?full_index=1",
        sha256="2316c08d2003d857a8b1e21df736a0fdf37a6d4595f1efa7a56e854b4a377d66",
    )

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("SUNDIALS_INST", self.spec["sundials"].prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            pytest = which("pytest")
            pytest(join_path(python_purelib, "scikits", "odes", "tests"))
