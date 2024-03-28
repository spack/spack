# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDvc(PythonPackage):
    """Git for data scientists - manage your code and data together."""

    homepage = "https://www.dvc.org"
    pypi = "dvc/dvc-1.11.10.tar.gz"

    license("Apache-2.0")

    version(
        "2.1.0",
        sha256="ad0cf1c4bab09cd91678faacdd2e14479e344b7a4220cfabae6b6b783b497e7d",
        url="https://pypi.org/packages/76/7c/59860666ce6e4d6ccb27474a0babda9d32a943f14bd4e36b30c1b9ec5736/dvc-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.11.10",
        sha256="037ffc5c7fa6f8e42f898659e58823645305e8cf3c76b3fca6be3d5819ee058f",
        url="https://pypi.org/packages/53/1e/2c55b18aca5c8cf54e4a1717b24887ccb4c6e65a4149e8ca4efbebc78070/dvc-1.11.10-py2.py3-none-any.whl",
    )
    version(
        "1.11.6",
        sha256="0a7f84130d0a6df9bcb7feac5a1a956a43060f3c015d695ea63dd63ed8e1e5e4",
        url="https://pypi.org/packages/eb/b6/3cb054942c0b1be32df62bd79a966a73a79a32e5ec460117fdb5a259e56e/dvc-1.11.6-py2.py3-none-any.whl",
    )

    variant("s3", default=False)
    variant("ssh", default=False)

    with default_args(type="run"):
        depends_on("python@3.9:", when="@3.43:")
        depends_on("py-appdirs@1.4.3:", when="@0.22:2.46")
        depends_on("py-boto3@1.9.201:", when="@0.73:2.1+s3")
        depends_on("py-colorama@0.3.9:", when="@0.9:")
        depends_on("py-configobj@5.0.6:", when="@0.9:")
        depends_on("py-dictdiffer@0.8.1:", when="@1.6:2.10")
        depends_on("py-diskcache@5.2:", when="@2.0.0-alpha2:2.10")
        depends_on("py-distro@1.3:", when="@0.20.2:")
        depends_on("py-dpath@2.0.1:", when="@0.91.1:2.7.3")
        depends_on("py-dulwich@0.20.21:", when="@2.0.14:2.1")
        depends_on("py-dulwich@0.20.14:", when="@1.11:1")
        depends_on("py-flatten-dict@0.3:", when="@1.6.6:2.5")
        depends_on("py-flufl-lock@3.2:3", when="@1.1.3:2.8.1")
        depends_on("py-fsspec@0.9:0", when="@2.0.18:2.1")
        depends_on("py-funcy@1.14:", when="@0.73:")
        depends_on("py-gitpython@3.0.1:", when="@0.86.2:2.8")
        depends_on("py-google-cloud-storage@1.19:1.19.0", when="@2.0.0-alpha4:2.0.0")
        depends_on("py-grandalf@:0.6", when="@0.18.1:2.7.2,2.7.4:2.41")
        depends_on("py-jsonpath-ng@1.5.1:", when="@0.88:2.5")
        depends_on("py-nanotime", when="@0.9:2.10")
        depends_on("py-networkx@2.1:2.4", when="@1.1.11:1.11.6")
        depends_on("py-networkx@2.1:", when="@0.19.8:0.62,1.11.7:2.2")
        depends_on("py-packaging@19:", when="@0.60:")
        depends_on("py-paramiko@2.7:+invoke", when="@1.7.6:2.5+ssh")
        depends_on("py-pathspec@0.6:", when="@0.62:2.5")
        depends_on("py-ply@3.9:", when="@0.10.2:2.10.0")
        depends_on("py-psutil@5.8:", when="@2:")
        depends_on("py-pyasn1@0.4:", when="@0.9:2.10.0")
        depends_on("py-pydot@1.2.4:", when="@0.82.7:")
        depends_on("py-pygit2@1.5:", when="@2.0.4:2.8")
        depends_on("py-pygtrie@2.3.2", when="@0.88:2.4.2")
        depends_on("py-pyparsing@2.4.7:2", when="@1.10.2:2.8.2")
        depends_on("py-python-benedict@0.21.1:", when="@1.10:2.7")
        depends_on("py-pywin32@225:", when="@2.6.1:2.7 platform=windows ^python@:3.9")
        depends_on("py-pywin32@225:", when="@0.66.6:2.6.0 platform=windows")
        depends_on("py-requests@2.22:", when="@0.40.3:")
        depends_on("py-rich@10:", when="@2.0.15:2.7")
        depends_on("py-rich@3.0.5:", when="@1.2:1")
        depends_on("py-ruamel-yaml@0.16.1:", when="@0.55:2.6.3")
        depends_on("py-setuptools@34:", when="@0.9:2.8.1")
        depends_on("py-shortuuid@0.5:", when="@0.50:")
        depends_on("py-shtab@1.3.4:", when="@2:")
        depends_on("py-shtab@1.3.2:", when="@1.8.1:1")
        depends_on("py-tabulate@0.8.7:", when="@1.0.0-alpha2:")
        depends_on("py-toml@0.10.1:", when="@1.2.1:2.16")
        depends_on("py-tqdm@4.45:", when="@0.92.1:2.9")
        depends_on("py-typing-extensions@3.7.4:", when="@2.7:2.7.2 ^python@:3.9")
        depends_on("py-typing-extensions@3.7.4:", when="@1.10.2:2.6,2.8:2.45")
        depends_on("py-voluptuous@0.11.7:", when="@0.71:")
        depends_on("py-win-unicode-console@0.5:", when="@0.50:2.8.1 platform=windows")
        depends_on("py-zc-lockfile@1.2.1:", when="@0.9:0.59,0.76:")
