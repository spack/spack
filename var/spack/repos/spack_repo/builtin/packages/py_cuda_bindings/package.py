# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
from spack.package import *

_versions = [
    {
        "sha256": "7167b0c4d872a7c0935a2ee4025eb1669702815366c2f0fb4c938fbd3dac09c7",
        "url": "https://files.pythonhosted.org/packages/f9/c4/0dac1eb970f94c5d180d724eac69394b5fdcb60f986f77d86030b0f510e5/cuda_bindings-12.8.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "33182c8aadf1c4ecf5e2672b5f0023f3be06011c22c916663eae6f33b1af90ff",
        "url": "https://files.pythonhosted.org/packages/9a/cc/27485aa29bbaadcc9eca07aaea1198807d7c2171550c290533a039d4efee/cuda_bindings-12.8.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "e0e6a889c87238e6cd55e9b25ce4fd1d90fe2d4169982860fed5f0bc3230795e",
        "url": "https://files.pythonhosted.org/packages/59/11/aee1afd60a5d6af67994dd88697912be22366a6e548e52e6cd2defdbe678/cuda_bindings-12.8.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "099f27e79e754346fa51517168787cda395fb437b31fbf20771c002f30adc0c9",
        "url": "https://files.pythonhosted.org/packages/78/f2/b5c3f07f743e74c1f5c42bb2fc6e735f3adac8b526f60ef731d861663dd9/cuda_bindings-12.8.0-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "df5929d82056891477bf1818241098b6289df6f43499f8683a40b9c220505a6b",
        "url": "https://files.pythonhosted.org/packages/85/29/862fa4541adf2cc96f87977116f9e71d3d8ee4dff0a3552117dc6ab7d0f6/cuda_bindings-12.8.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "050e82a8d1ee4d8ac04fc56cf6f98cfea72225447f4a57e477fd455484b88818",
        "url": "https://files.pythonhosted.org/packages/03/30/f5f2da321f72c23af9bb9df947ef5f53a1efe536d8ec4ccdacdfac25174d/cuda_bindings-12.9.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "f543acf44f1d119c148c49937810451541a8618b054cc779fb1fa21ab46da64c",
        "url": "https://files.pythonhosted.org/packages/49/0d/82de160bd477c1a51195a49476dd7e3b538432c8717fd636bffc9c806076/cuda_bindings-12.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "ff0e28d1e34758654b9c961e1f55e4786e49aee6a4dbceaf3cc24c46c672df7e",
        "url": "https://files.pythonhosted.org/packages/e3/03/40fc1488727a8d72ecc35f58f9df4939277892a837614339c3366d520426/cuda_bindings-12.9.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "f6d7314b2e5db025bb88ddba4df6db2127cc39610ccf4f74c0e1ead05241da29",
        "url": "https://files.pythonhosted.org/packages/01/fd/1c30778265488c6797c6c17a69c09ba5636df6dc6b0ebfc96d950be2f9e7/cuda_bindings-12.9.0-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
    {
        "sha256": "98391b6c811dd6565a23b89dcd3d5a530c0d1557a37d3c915670931b6578052b",
        "url": "https://files.pythonhosted.org/packages/1a/47/9c16b088a9ed1d7f9b2c5a73866df41fe61eb460222bb75281a1159491fd/cuda_bindings-12.9.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    },
]


class PyCudaBindings(PythonPackage):
    """cuda.bindings is a standard set of low-level interfaces, providing full coverage of and access to the CUDA host APIs from Python."""

    homepage = "https://pypi.org/project/cuda-bindings/"

    for entry in _versions:
        url = entry["url"]
        sha256 = entry["sha256"]

        match = re.search(r"cuda_bindings-(\d+\.\d+\.\d+)-cp(\d)(\d+)", url)
        if not match:
            raise ValueError(f"Failed to parse version info from {url}")

        package_version = match.group(1)
        python_version = f"{match.group(2)}.{match.group(3)}"
        cuda_version = ".".join(package_version.split(".")[:2])  # drop patch

        full_version = f"{package_version}-py{python_version.replace('.', '')}"
        version_args = {"sha256": sha256, "url": url}

        if cuda_version == "12.8":
            version_args["preferred"] = True

        version(full_version, **version_args)
        depends_on(f"python@{python_version}", when=f"@{full_version}")
        depends_on(f"cuda@{cuda_version}", when=f"@{full_version}")

    conflicts("target=ppc64le:", msg="py-cuda-bindings is only available for x86_64")
    conflicts("target=aarch64:", msg="py-cuda-bindings is only available for x86_64")
