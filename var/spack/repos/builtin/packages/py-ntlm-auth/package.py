# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNtlmAuth(PythonPackage):
    """Creates NTLM authentication structures."""

    homepage = "https://github.com/jborean93/ntlm-auth"
    pypi = "ntlm-auth/ntlm-auth-1.5.0.tar.gz"

    license("MIT")

    version(
        "1.5.0",
        sha256="f1527c581dbf149349134fc2d789d50af2a400e193206956fa0ab456ccc5a8ba",
        url="https://pypi.org/packages/ff/84/97c550164b54942b0e908c31ef09d9469f3ba4cd7332a671e2125732f63b/ntlm_auth-1.5.0-py2.py3-none-any.whl",
    )
