# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurora(PythonPackage):
    """A Python Toolbox for Multimodal Neural Data Representation Analysis."""

    homepage = "https://github.com/ZitongLu1996/NeuroRA"
    pypi = "neurora/neurora-1.1.5.16.tar.gz"

    license("MIT")

    version(
        "1.1.6.10",
        sha256="7fe3cdbc957f15a2e7ccc7d19a53f0e334406a9c34123aa11afaf06e7c879d17",
        url="https://pypi.org/packages/9b/4f/f954d0a7719774d6fff3de75d25745f4f64abdd2e1939ace6ea54f554d4c/neurora-1.1.6.10-py3-none-any.whl",
    )
    version(
        "1.1.6.9",
        sha256="8840fed2058245b02e4f2a6f32207226ebac279098a5417bf45b0911f2f64425",
        url="https://pypi.org/packages/8e/e2/814675b6ba608ca269a37e6bc2fd62082c85258633dd5f301beb39f5a244/neurora-1.1.6.9-py3-none-any.whl",
    )
    version(
        "1.1.6.8",
        sha256="51ee159a81bcecbc2f52c266c9f6cc9dc3cd78773a66012ee83cefdbdcba09bf",
        url="https://pypi.org/packages/5e/80/f076fd8386b64363298b1aa73e47771c8f68332e893b314356b5880cba90/neurora-1.1.6.8-py3-none-any.whl",
    )
    version(
        "1.1.6.1",
        sha256="5e151a960ea28fc70ee28e59367d430312a3454cf78adf3c1fc655ed155caf1a",
        url="https://pypi.org/packages/7b/ab/48368beff11fd4e7aa7841a5a06af28c5f0fbb83e1f63f6fad251afefa87/neurora-1.1.6.1-py3-none-any.whl",
    )
    version(
        "1.1.5.16",
        sha256="f75dbd56d9239ea5863ab12733345b0a010740b0c5630132be719aede36be87e",
        url="https://pypi.org/packages/f5/de/ec348c7cd42ceadad823ccab929a1a6e2df1b509b30ff4e7199f3a4be90c/neurora-1.1.5.16-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-matplotlib")
        depends_on("py-mne")
        depends_on("py-nibabel")
        depends_on("py-nilearn")
        depends_on("py-numpy")
        depends_on("py-scikit-image")
        depends_on("py-scikit-learn")
        depends_on("py-scipy@1.6.2:")
