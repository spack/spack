# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *
import glob

class PyPolars(PythonPackage):
    """Blazingly fast DataFrame library."""

    homepage = "https://www.pola.rs/"
    pypi = "polars/polars-0.20.5.tar.gz"

    license("MIT")

    version("1.29.0", sha256="d2acb71fce1ff0ea76db5f648abd91a7a6c460fafabce9a2e8175184efa00d02")
    version("0.20.5", sha256="fa4abc22cee024b5872961ddcd8a13a0a76150df345e21ce4308c2b1a36b47aa")

    # README.md
    depends_on("rust@1.71:", type="build", when="@0.20")

    # requires select_unpredictable and stable builds are not supported
    # https://doc.rust-lang.org/nightly/core/hint/fn.select_unpredictable.html
    # https://github.com/pola-rs/polars/issues/13653#issuecomment-2041619141
    depends_on("rust@nightly", type="build", when="@1.29:")

    # pyproject.toml
    depends_on("py-maturin@1.3.2:", type="build")

    # Interop
    depends_on("py-numpy@1.16.0:", type=("build","run"))
    depends_on("py-pandas", type=("build","run"))
    depends_on("py-pyarrow@7.0.0:", type=("build","run"))
    depends_on("py-pydantic")

    # Other
    depends_on("py-cloudpickle", type=("build","run"))
    depends_on("py-matplotlib", type=("build","run"))
    depends_on("py-altair@0.7.1:", type=("build","run"))
    depends_on("py-gevent", type=("build","run"))
    # depends_on("py-great-tables@0.8.0:", type=("build","run"))

    # def patch(self):
        # for filename in glob.glob('**/build.rs', recursive=True):
        #     filter_file(".*println!\(\"cargo:rustc-cfg=feature.*",
        #      '', filename)

        # filter_file('channel.*', f'channel="{self.spec["rust"].version}"', "rust-toolchain.toml")
        # filter_file('channel.*', f'channel="{self.spec["rust"].version}"', "py-polars/rust-toolchain.toml")
