# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Commented-out versions don't have a corresponding LLVM entry in Spack.
_versions = [
    # ("17.0.6", "50f082840d2e013160355ed63add4502884344371dda5af12ec0abe68cbc5a36"),
    # ("17.0.5", "8fc4ef6ad1b6ad11f5903069f34a661699bb187288c09f643990a42ee41df47e"),
    ("17.0.4", "b8513e927c8e0caaba83be8d065f8100ad94415cd1cb2945127debe7bb368de0"),
    ("17.0.3", "763a3f276e579d5e304527229420b1e0c9aa12318675a21c0107f9373e918ab1"),
    ("17.0.2", "70c52185946d7ffca8901412778ac03b2a935a8009f01599fe1ae530c68a49e2"),
    ("17.0.1", "ed017015563d5195de2edc0e99ad7e10040cb724057b4968705778e8dfff068f"),
    ("16.0.6", "6805f45a90fd7085b08fe917dddf8ace5e957c03bbacf43d09ca8312a1d981e5"),
    ("16.0.5", "59a1df466bec1fbfb6fc022ad3c03a3f98965f530d440bf0318a110617078e4b"),
    ("16.0.4", "97d1478ce52e403aa54165ba47df919327378e3ede2a7af322ea2e06a34b5d15"),
    ("16.0.3", "62b9bf91c8ebc6dff32e261e2e1e8483eff58c1cf43607706e235e5cc89c7f3c"),
    ("16.0.2", "772cffe40b97872ed74e1cf83c7401340a87bd2c1228da6bdd81ffb30c753e8a"),
    ("16.0.1", "e099be756ea229b2332324a5e17e96c2bbd2e3601c96a06d7265a2bc1ea81b52"),
    ("16.0.0", "f8dd028e10e1fe18d3598fcdf04b265d46c07d695c43504ea2fba9e74287766e"),
    ("15.0.7", "60954c571394354200912e72ce10454b96016af879771df39d09d605ceaec035"),
    ("15.0.6", "09dc33e84130191b6d84a90f17eb1908d66ed017996286cd73f8bc8644ebcaa3"),
    ("15.0.4", "29ec4c30226398cc4c78417cca380d5d2f9bfd3aa234eb9d6fe2c9bc605183cb"),
    ("14.0.6", "d5c96b500d7f8b5d2db5b75ac035be387512850ad589cdc3019666b861382136"),
    ("14.0.5", "d83a7e4b3c50f2e8f75a7cb5bf52073819a0b6ab940874d822a9309a339a3058"),
    ("14.0.4", "4092fb4d0908d82f9bcc4a772f44c3a2ad1e80b7cb0260d198d5ed5aa90d4683"),
    ("14.0.3", "73bc0bd21eacdee30b85e1315a6cff5685531d89905c3411de91816fc7cbce75"),
    ("14.0.1", "9966930f6951c3ce64e24a8abae1c130df07feb6da2d132de62e1e3077bcbc54"),
    ("14.0.0", "60c631c990bb1fa2a20fb60c581560dec9c37ffb575e616fe9c05d45bdd3b407"),
    # ("13.0.1.1", "ccd9a570bfa1cd1d4a7eb30ea8736ff7f13b6ec234e671dbdf3ecd9eb3a736bf"),
    ("13.0.1", "deb131bee8716aead66f0bbf64126cb9e18499d18ea75801dda86ff842320142"),
    ("13.0.0", "cc0c5e791f180ad5141d800834f6041862ef6179213b6bd7fcd5296719490ac0"),
    # ("12.0.1.2", "ed8e9ba912f458a259fa0e0ff7fc8c15caf8a7adb61f2d5a5c60eccb575d6e10"),
    # ("12.0.1.1", "6bdc9f70f9e384bb5e238f2f6859e0719dcc5caf1cb6c7e61b9670fc42727297"),
    ("12.0.1", "b687687ea47f7b236edf8b436d126e944d5d27ae0d45e14184a54d890bf4242e"),
    # ("11.1.0.2", "62b21d3f5e476914480e8c08619a5c7caa257d0364ea8ea5336aa7cc6d677137"),
    # ("11.1.0.1", "0d1ec838fc335d3102888bbbcd0bd0774a0f459ce1af1c233cbd7aefaa055e7d"),
    ("11.1.0", "4f6d9d33bf52a1e23d5eda47b09707591d3eb19f1a2e40de12f924a71f425962"),
    # ("11.0.1.2", "82a9f2584142bdbdc71a5f43a26f6d5ebc1276b134a962b14906cc5d640d074e"),
    # ("11.0.1.1", "b4d073d1809f8aaee9183d5f9843abe4b070784a89a074a7fa5a59739a250f0c"),
    ("11.0.1", "7e62439218c38126f9234bc0fdfa85cb2ef5798219190acc911962f0b0a0abfc"),
    # ("10.0.1.1", "016480cc99ff8fa9342672608b2e68f9eca9310407d248b1e7d8679c22dc6344"),
    ("10.0.1", "beab968d1857e2cb4c2907e8cc6dcd7fb0ee6e9a37bbfaa014fc008b2bb268cc"),
]

class PyClangFormat(PythonPackage):
    """A standalone package for the clang-format utility."""

    homepage = "https://github.com/ssciwr/clang-format-wheel"
    pypi = "clang-format/clang-format-17.0.4.tar.gz"

    maintainers("berquist")

    license("Apache-2.0", checked_by="berquist")

    for ver, sha256 in _versions:
        version(ver, sha256=sha256)
        depends_on("llvm@={} +clang".format(ver), when="@={}".format(ver), type="build")

    patch("use_local_llvm.patch")

    # From pyproject.toml
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
