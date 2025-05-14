# Copyright Spack Project Developers. See COPYRIGHT file for details.#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibmetatensor(PythonPackage):
    """Python bindings for metatensor-core"""

    homepage = "https://docs.metatensor.org"
    pypi = "metatensor-core/metatensor_core-0.1.14.tar.gz"

    import_modules = ["metatensor"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.1.14", sha256="ee1f87bc045beadafa63cc0ccd0ebcf9c9e9fe8d619529d28775b0c22e0bbe19")
    version("0.1.13", sha256="d43dfba8c6092de3e7bbe29dcf8fa3680462abd68947ece809befc9b0f6c1d56")
    version("0.1.12", sha256="b0b9c0386117e2ebfeff47e0a607e478cb24aa74337eaa69a528d16e6fd3a217")
    version("0.1.11", sha256="d434f51560521b6f693627092323dd95bfdb3532641a01bca37150d83b8fbb7c")
    version("0.1.10", sha256="102786b2971544c7ee962549f8f77d77e0be8f65ac7057dc0c4717176c729a2a")
    version("0.1.9", sha256="544dec54546070ce0526709db3a245982bb503239eb1bb011dad5c75d58099b2")
    version("0.1.8", sha256="6377ce87c60709176c6b6b2d0fda72151775e709973470dfc47ab2df994e8546")
    version("0.1.7", sha256="07e143a98b5fe14f64e3f830d925bb7d33a65d6ff97a3b084a5bb87a3109024c")
    version("0.1.6", sha256="36912e6ac2c45951a1947b3843cc39a6e5fa50d9e0121695733de92c383a8327")

    extends("python")
    depends_on("py-numpy", type=("run"))

    # TODO(HaoZeke): Needs to be done for each version
    depends_on("libmetatensor@0.1.14", when="@0.1.14")

    # pyproject.toml
    depends_on("py-setuptools@77:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("cmake", type="build")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("METATENSOR_CORE_PYTHON_USE_EXTERNAL_LIB", "ON")
