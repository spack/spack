# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTroveClassifiers(PythonPackage):
    """The trove-classifiers pacakge is the canonical source for classifiers
    on PyPI. Classifiers categorize projects per PEP 301."""

    homepage = "https://github.com/pypa/trove-classifiers"
    pypi = "trove_classifiers/trove_classifiers-2024.5.17.tar.gz"

    license("Apache-2.0")

    version(
        "2025.4.11.15", sha256="634728aa6698dc1ae3db161da94d9e4c7597a9a5da2c4410211b36f15fed60fc"
    )
    version("2023.8.7", sha256="c9f2a0a85d545e5362e967e4f069f56fddfd91215e22ffa48c66fb283521319a")
    version("2023.3.9", sha256="ee42f2f8c1d4bcfe35f746e472f07633570d485fab45407effc0379270a3bb03")

    depends_on("py-setuptools", type="build")
    depends_on("py-calver", type="build")

    def url_for_version(self, version):
        if version >= Version("2024.5.17"):
            sep = "_"
        else:
            sep = "-"

        return f"https://files.pythonhosted.org/packages/source/t/trove{sep}classifiers/trove{sep}classifiers-{version}.tar.gz"
