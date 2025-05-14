# Copyright Spack Project Developers. See COPYRIGHT file for details.#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# Necessary to pin each version to libmetatensor
VERSION_MAP = {
    "0.1.14": "ee1f87bc045beadafa63cc0ccd0ebcf9c9e9fe8d619529d28775b0c22e0bbe19",
    "0.1.13": "d43dfba8c6092de3e7bbe29dcf8fa3680462abd68947ece809befc9b0f6c1d56",
    "0.1.12": "b0b9c0386117e2ebfeff47e0a607e478cb24aa74337eaa69a528d16e6fd3a217",
    "0.1.11": "d434f51560521b6f693627092323dd95bfdb3532641a01bca37150d83b8fbb7c",
    "0.1.10": "102786b2971544c7ee962549f8f77d77e0be8f65ac7057dc0c4717176c729a2a",
    "0.1.9": "544dec54546070ce0526709db3a245982bb503239eb1bb011dad5c75d58099b2",
    "0.1.8": "6377ce87c60709176c6b6b2d0fda72151775e709973470dfc47ab2df994e8546",
    "0.1.7": "07e143a98b5fe14f64e3f830d925bb7d33a65d6ff97a3b084a5bb87a3109024c",
    "0.1.6": "36912e6ac2c45951a1947b3843cc39a6e5fa50d9e0121695733de92c383a8327",
}


class PyLibmetatensor(PythonPackage):
    """Python bindings for metatensor-core"""

    homepage = "https://docs.metatensor.org"
    pypi = "metatensor-core/metatensor_core-0.1.14.tar.gz"

    import_modules = ["metatensor"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    extends("python")
    depends_on("py-numpy", type=("run"))

    for ver, sha in VERSION_MAP.items():
        version(ver, sha256=sha)
        depends_on(f"libmetatensor@{ver}", when=f"@{ver}")

    # pyproject.toml
    depends_on("py-setuptools@77:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("cmake", type="build")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("METATENSOR_CORE_PYTHON_USE_EXTERNAL_LIB", "ON")
