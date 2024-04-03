# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpmdViewer(PythonPackage):
    """Python visualization tools for openPMD files"""

    homepage = "https://www.openPMD.org"
    git = "https://github.com/openPMD/openPMD-viewer.git"
    pypi = "openPMD-viewer/openPMD-viewer-1.2.0.tar.gz"

    maintainers("RemiLehe", "ax3l")

    license("BSD-3-Clause-LBNL")

    version(
        "1.4.0",
        sha256="fef45732c830314a0a6c1d2c44bcaa871124cdbfa8648faa73d773c2903a524a",
        url="https://pypi.org/packages/98/48/b4b67bb6f4ab70c3307a919a25850bf09fc17f8f79ae17f7dbfd64de6033/openPMD_viewer-1.4.0-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="95702c933f6d5796100ede029553ef4e186c918634ee0dbc5702bcdb31532d73",
        url="https://pypi.org/packages/77/df/6380a631fc780a46403bab6f93ae05a37fdb785b249a2fd412947dd566fc/openPMD_viewer-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="334e6f01e44300989974bd420860d1ae25d19de0dd8b101a66f208f3b58b8cdd",
        url="https://pypi.org/packages/eb/de/915a0382906248f92a89e58ce98e1bae32f3ada6196b0a5fdde8271d70ca/openPMD_viewer-1.2.0-py3-none-any.whl",
    )

    variant(
        "backend",
        default="h5py,openpmd-api",
        description="Visualization backend",
        multi=True,
        values=("h5py", "openpmd-api"),
    )
    variant("jupyter", default=False, description="Enable Jupyter Widget GUI")
    variant("numba", default=False, description="Enable accelerated depositions for histograms")
    variant("plot", default=True, description="Enable plotting support")
    variant("tutorials", default=True, description="Enable dependencies for tutorials")

    with default_args(type="run"):
        depends_on("py-h5py@2.8.0:", when="@1.2:")
        depends_on("py-ipympl", when="@1.3:+tutorials")
        depends_on("py-ipywidgets", when="@0.8:+tutorials")
        depends_on("py-matplotlib", when="@0.8:+tutorials")
        depends_on("py-matplotlib", when="+plot")
        depends_on("py-numba", when="@1.3:+numba")
        depends_on("py-numpy@1.15.0:1", when="@1.2:")
        depends_on("py-scipy")
        depends_on("py-tqdm", when="@1:")
        depends_on("py-wget", when="@0.8:+tutorials")

        # missing in Spack:
        # with when('+jupyter'):
        #     depends_on('py-ipympl', type=('build', 'run'))
