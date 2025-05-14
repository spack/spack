# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPolars(PythonPackage):
    """Blazingly fast DataFrame library."""

    homepage = "https://www.pola.rs/"
    pypi = "polars/polars-0.20.5.tar.gz"

    license("MIT")

    version("1.29.0", sha256="d2acb71fce1ff0ea76db5f648abd91a7a6c460fafabce9a2e8175184efa00d02")
    version("0.20.5", sha256="fa4abc22cee024b5872961ddcd8a13a0a76150df345e21ce4308c2b1a36b47aa")

    variant(
        "nightly", default=False, description="Enable nightly SIMD paths. Requires nightly rust"
    )

    # README.md
    depends_on("rust@1.71:", type="build", when="@0.20")
    depends_on("rust@1.80:", type="build", when="@1.29:")

    # nightly rust is built without a checksum and will fail with the error
    # URLFetchStrategy with no digest
    # build it with
    #     $ spack install -n rust@nightly
    depends_on("rust@nightly", type="build", when="@1.29: +nightly")

    # pyproject.toml
    depends_on("py-maturin@1.3.2:", type="build")

    # Interop
    depends_on("py-numpy@1.16.0:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow@7.0.0:", type=("build", "run"))
    depends_on("py-pydantic")

    # The following optional dependencies are missing in spack
    # Excel
    # Database
    # Cloud
    # Other I/O

    # Other
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-altair@0.7.1:", type=("build", "run"))
    depends_on("py-gevent", type=("build", "run"))
    # depends_on("py-great-tables@0.8.0:", type=("build","run"))

    @when("~nightly")
    def setup_build_environment(self, env):
        # https://github.com/PyO3/maturin/discussions/1090
        # https://github.com/pola-rs/polars/issues/22708#issuecomment-2872555300
        env.prepend_path("MATURIN_PEP517_ARGS", "--no-default-features --features all")
