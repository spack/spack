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

    # README.md
    depends_on("rust@1.71:", type="build", when="@0.20")

    depends_on("rust@1.80:", type="build", when="@1.29:")

    # pyproject.toml
    depends_on("py-maturin@1.3.2:", type="build")

    # Interop
    depends_on("py-numpy@1.16.0:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyarrow@7.0.0:", type=("build", "run"))
    depends_on("py-pydantic")

    # Other
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-altair@0.7.1:", type=("build", "run"))
    depends_on("py-gevent", type=("build", "run"))
    # depends_on("py-great-tables@0.8.0:", type=("build","run"))

    def patch(self):
        # polars seems to require a nightly rust
        # https://github.com/pola-rs/polars/issues/13653#issuecomment-2041619141
        # these patches turn of the nightly code paths

        # ensure the toolchain is for stable
        filter_file("channel.*", 'channel="stable"', "rust-toolchain.toml")
        filter_file("channel.*", 'channel="stable"', "py-polars/rust-toolchain.toml")

        # only use non-nightly features of depedency crates
        filter_file(
            r"default = \[\"all\", \"nightly\"\]", 'default = ["all"]', "py-polars/Cargo.toml"
        )
