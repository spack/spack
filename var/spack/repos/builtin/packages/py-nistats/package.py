# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNistats(PythonPackage):
    """Modeling and Statistical analysis of fMRI data in Python."""

    homepage = "https://github.com/nilearn/nistats"
    pypi = "nistats/nistats-0.0.1rc0.tar.gz"

    version(
        "0.0.1-rc0",
        sha256="e00be1810862e3a6a8dc81cc6563e8abca109e88ff7f4c2b96b29a769c1e599b",
        url="https://pypi.org/packages/50/57/034f882afce11ee6d61dd3c8e94fac543e5210470bb01fc5c066e1ae30b5/nistats-0.0.1rc0-py2.py3-none-any.whl",
    )
    version(
        "0.0.1-beta2",
        sha256="2864df42b9266999a0674d010ef3691a802fb199077a0c2fd4632b8d1ae8b9fb",
        url="https://pypi.org/packages/b8/0b/e69a4fd42450d46b4216e75ecfcabb4a2feef15ac5e2b3cc0b22d15dbcef/nistats-0.0.1b2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-nibabel@2.0.2:", when="@0.0.1-beta0:")
        depends_on("py-nilearn@0.4:", when="@0.0.1-beta0:")
        depends_on("py-numpy@1.11.0:", when="@0.0.1-beta0:")
        depends_on("py-pandas@0.18:", when="@0.0.1-beta0:")
        depends_on("py-scikit-learn@0.18:", when="@0.0.1-beta0:")
        depends_on("py-scipy@0.17:", when="@0.0.1-beta0:")

    # needs +plotting to avoid ModuleNotFoundError:
    # 'nilearn.plotting.js_plotting_utils' when importing nistats.reporting
    # Functionality has been incorporated into py-nilearn@0.7:
