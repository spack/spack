# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidsValidator(PythonPackage):
    """Validator for the Brain Imaging Data Structure"""

    homepage = "https://github.com/bids-standard/bids-validator"
    pypi = "bids-validator/bids-validator-1.7.2.tar.gz"

    version(
        "1.13.1",
        sha256="da6edf5e76ef86c8a63b3fcee1dbfb039a16a9ef63cb0d2d05312c200d4607f7",
        url="https://pypi.org/packages/f4/a1/248c9394ab59679fd35ac2a4b7d4adec2be55ad5e3b1cf5b12b791918338/bids_validator-1.13.1-py2.py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="d2fd8943510453eb2f9fed28fba8e063f280a7bbed8152880783631fd4109f1a",
        url="https://pypi.org/packages/87/9e/722ca2a2dcacedb8133bec1d226ed62ba775c628c108d20f774002fea767/bids_validator-1.11.0-py2.py3-none-any.whl",
    )
    version(
        "1.9.8",
        sha256="8bc1b74bf6dbc277826b60bed6818e70b0fda3ae944c146ff6907a7a1e079b05",
        url="https://pypi.org/packages/36/55/0f47886b11ee2b7e154d0163814dde6a77b4611bad070deb1a25ca8e0dd2/bids_validator-1.9.8-py2.py3-none-any.whl",
    )
    version(
        "1.9.4",
        sha256="5bee401d55fb039ac1dd9b97f326c6a538f1d25789abc00d5d2b3350c757756b",
        url="https://pypi.org/packages/86/39/c50befdf65a28cf8e69efddeb6622fd1f10f436ce28a157d2025d96a270b/bids_validator-1.9.4-py2.py3-none-any.whl",
    )
    version(
        "1.8.9",
        sha256="b2def483d9d88b9240e44e340687159d7561d6a0eb6ca52afed47becc49582bb",
        url="https://pypi.org/packages/ab/7e/ac413b12f659c714118b7132ac760fb8e951a55133e42d140def278a9b5f/bids_validator-1.8.9-py2.py3-none-any.whl",
    )
    version(
        "1.8.4",
        sha256="ce6de214e48051300a738aaf7226b5585c4268646ee890c491ee011e7415fbbf",
        url="https://pypi.org/packages/89/3b/cdb1ba8648636a897c9108c36ebb4c2d5dab01443693dea27d06a6cefe19/bids_validator-1.8.4-py2.py3-none-any.whl",
    )
    version(
        "1.7.2",
        sha256="854f56177a4b93cbf2202947b0821646a5af629bbefe796d8114bcad6de9559e",
        url="https://pypi.org/packages/26/d3/49a2c0ed2af7560baac349befde5f80df61b415cc7c0d577a85ab3142e3f/bids_validator-1.7.2-py2.py3-none-any.whl",
    )
