# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPip(Package, PythonExtension):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pip.pypa.io/"
    url = "https://files.pythonhosted.org/packages/py3/p/pip/pip-20.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pip/"

    # Requires railroad
    skip_modules = ["pip._vendor"]

    tags = ["build-tools"]

    maintainers("adamjstewart", "pradyunsg")

    license("MIT")

    version(
        "24.0",
        sha256="ba0d021a166865d2265246961bec0152ff124de910c5cc39f1156ce3fa7c69dc",
        url="https://pypi.org/packages/8a/6a/19e9fe04fca059ccf770861c7d5721ab4c2aebc539889e97c7977528a53b/pip-24.0-py3-none-any.whl",
    )
    version(
        "23.3.2",
        sha256="5052d7889c1f9d05224cd41741acb7c5d6fa735ab34e339624a614eaaa7e7d76",
        url="https://pypi.org/packages/15/aa/3f4c7bcee2057a76562a5b33ecbd199be08cdb4443a02e26bd2c3cf6fc39/pip-23.3.2-py3-none-any.whl",
    )
    version(
        "23.3.1",
        sha256="55eb67bb6171d37447e82213be585b75fe2b12b359e993773aca4de9247a052b",
        url="https://pypi.org/packages/47/6a/453160888fab7c6a432a6e25f8afe6256d0d9f2cbd25971021da6491d899/pip-23.3.1-py3-none-any.whl",
    )
    version(
        "23.3",
        sha256="bc38bb52bc286514f8f7cb3a1ba5ed100b76aaef29b521d48574329331c5ae7b",
        url="https://pypi.org/packages/e0/63/b428aaca15fcd98c39b07ca7149e24bc14205ad0f1c80ba2b01835aedde1/pip-23.3-py3-none-any.whl",
    )
    version(
        "23.2.1",
        sha256="7ccf472345f20d35bdc9d1841ff5f313260c2c33fe417f48c30ac46cccabf5be",
        url="https://pypi.org/packages/50/c2/e06851e8cc28dcad7c155f4753da8833ac06a5c704c109313b8d5a62968a/pip-23.2.1-py3-none-any.whl",
    )
    version(
        "23.2",
        sha256="78e5353a9dda374b462f2054f83a7b63f3f065c98236a68361845c1b0ee7e35f",
        url="https://pypi.org/packages/02/65/f15431ddee78562355ccb39097bf9160a1689f2db40dc418754be98806a1/pip-23.2-py3-none-any.whl",
    )
    version(
        "23.1.2",
        sha256="3ef6ac33239e4027d9a5598a381b9d30880a1477e50039db2eac6e8a8f6d1b18",
        url="https://pypi.org/packages/08/e3/57d4c24a050aa0bcca46b2920bff40847db79535dc78141eb83581a52eb8/pip-23.1.2-py3-none-any.whl",
    )
    version(
        "23.1.1",
        sha256="3d8d72fa0714e93c9d3c2a0ede91e898c64596e0fa7d4523f72dd95728efc418",
        url="https://pypi.org/packages/f8/f8/17bd3f7c13515523d811ce4104410c16c03e3c6830f9276612e2f4b28382/pip-23.1.1-py3-none-any.whl",
    )
    version(
        "23.1",
        sha256="64b1d4528e491aa835ec6ece0c1ac40ce6ab6d886e60740f6519db44b2e9634d",
        url="https://pypi.org/packages/ae/db/a8821cdac455a1740580c92de3ed7b7f257cfdbad8b1ba8864e6abe58a08/pip-23.1-py3-none-any.whl",
    )
    version(
        "23.0.1",
        sha256="236bcb61156d76c4b8a05821b988c7b8c35bf0da28a4b614e8d6ab5212c25c6f",
        url="https://pypi.org/packages/07/51/2c0959c5adf988c44d9e1e0d940f5b074516ecc87e96b1af25f59de9ba38/pip-23.0.1-py3-none-any.whl",
    )
    version(
        "20.2.4",
        sha256="51f1c7514530bd5c145d8f13ed936ad6b8bfcb8cf74e10403d0890bc986f0033",
        url="https://pypi.org/packages/cb/28/91f26bd088ce8e22169032100d4260614fc3da435025ff389ef1d396a433/pip-20.2.4-py2.py3-none-any.whl",
    )
    version(
        "20.2.3",
        sha256="0f35d63b7245205f4060efe1982f5ea2196aa6e5b26c07669adcf800e2542026",
        url="https://pypi.org/packages/4e/5f/528232275f6509b1fff703c9280e58951a81abe24640905de621c9f81839/pip-20.2.3-py2.py3-none-any.whl",
    )
    version(
        "20.2.2",
        sha256="5244e51494f5d1dfbb89da492d4250cb07f9246644736d10ed6c45deb1a48500",
        url="https://pypi.org/packages/5a/4a/39400ff9b36e719bdf8f31c99fe1fa7842a42fa77432e584f707a5080063/pip-20.2.2-py2.py3-none-any.whl",
    )
    version(
        "20.2.1",
        sha256="7792c1a4f60fca3a9d674e7dee62c24e21a32df1f47d308524d3507455784f29",
        url="https://pypi.org/packages/bd/b1/56a834acdbe23b486dea16aaf4c27ed28eb292695b90d01dff96c96597de/pip-20.2.1-py2.py3-none-any.whl",
    )
    version(
        "20.2",
        sha256="d75f1fc98262dabf74656245c509213a5d0f52137e40e8f8ed5cc256ddd02923",
        url="https://pypi.org/packages/36/74/38c2410d688ac7b48afa07d413674afc1f903c1c1f854de51dc8eb2367a5/pip-20.2-py2.py3-none-any.whl",
    )
    version(
        "20.1.1",
        sha256="b27c4dedae8c41aa59108f2fa38bf78e0890e590545bc8ece7cdceb4ba60f6e4",
        url="https://pypi.org/packages/43/84/23ed6a1796480a6f1a2d38f2802901d078266bda38388954d01d3f2e821d/pip-20.1.1-py2.py3-none-any.whl",
    )
    version(
        "20.1",
        sha256="4fdc7fd2db7636777d28d2e1432e2876e30c2b790d461f135716577f73104369",
        url="https://pypi.org/packages/54/2e/df11ea7e23e7e761d484ed3740285a34e38548cf2bad2bed3dd5768ec8b9/pip-20.1-py2.py3-none-any.whl",
    )
    version(
        "20.0.2",
        sha256="4ae14a42d8adba3205ebeb38aa68cfc0b6c346e1ae2e699a0b3bad4da19cef5c",
        url="https://pypi.org/packages/54/0c/d01aa759fdc501a58f431eb594a17495f15b88da142ce14b5845662c13f3/pip-20.0.2-py2.py3-none-any.whl",
    )
    version(
        "20.0.1",
        sha256="b7110a319790ae17e8105ecd6fe07dbcc098a280c6d27b6dd7a20174927c24d7",
        url="https://pypi.org/packages/57/36/67f809c135c17ec9b8276466cc57f35b98c240f55c780689ea29fa32f512/pip-20.0.1-py2.py3-none-any.whl",
    )
    version(
        "20.0",
        sha256="eea07b449d969dbc8c062c157852cf8ed2ad1b8b5ac965a6b819e62929e41703",
        url="https://pypi.org/packages/60/65/16487a7c4e0f95bb3fc89c2e377be331fd496b7a9b08fd3077de7f3ae2cf/pip-20.0-py2.py3-none-any.whl",
    )
    version(
        "19.3.1",
        sha256="6917c65fc3769ecdc61405d3dfd97afdedd75808d200b2838d7d961cebc0c2c7",
        url="https://pypi.org/packages/00/b6/9cfa56b4081ad13874b0c6f96af8ce16cfbc1cb06bedf8e9164ce5551ec1/pip-19.3.1-py2.py3-none-any.whl",
    )
    version(
        "19.3",
        sha256="e100a7eccf085f0720b4478d3bb838e1c179b1e128ec01c0403f84e86e0e2dfb",
        url="https://pypi.org/packages/4a/08/6ca123073af4ebc4c5488a5bc8a010ac57aa39ce4d3c8a931ad504de4185/pip-19.3-py2.py3-none-any.whl",
    )
    version(
        "19.2.3",
        sha256="340a0ba40fdeb16413914c0fcd8e0b4ebb0bf39a900ec80e11c05d836c05103f",
        url="https://pypi.org/packages/30/db/9e38760b32e3e7f40cce46dd5fb107b8c73840df38f0046d8e6514e675a1/pip-19.2.3-py2.py3-none-any.whl",
    )
    version(
        "19.2.2",
        sha256="4b956bd8b7b481fc5fa222637ff6d0823a327e5118178f1ec47618a480e61997",
        url="https://pypi.org/packages/8d/07/f7d7ced2f97ca3098c16565efbe6b15fafcba53e8d9bdb431e09140514b0/pip-19.2.2-py2.py3-none-any.whl",
    )
    version(
        "19.2.1",
        sha256="80d7452630a67c1e7763b5f0a515690f2c1e9ad06dda48e0ae85b7fdf2f59d97",
        url="https://pypi.org/packages/62/ca/94d32a6516ed197a491d17d46595ce58a83cbb2fca280414e57cd86b84dc/pip-19.2.1-py2.py3-none-any.whl",
    )
    version(
        "19.2",
        sha256="468c67b0b1120cd0329dc72972cf0651310783a922e7609f3102bd5fb4acbf17",
        url="https://pypi.org/packages/3a/6f/35de4f49ae5c7fdb2b64097ab195020fb48faa8ad3a85386ece6953c11b1/pip-19.2-py2.py3-none-any.whl",
    )
    version(
        "19.1.1",
        sha256="993134f0475471b91452ca029d4390dc8f298ac63a712814f101cd1b6db46676",
        url="https://pypi.org/packages/5c/e0/be401c003291b56efc55aeba6a80ab790d3d4cece2778288d65323009420/pip-19.1.1-py2.py3-none-any.whl",
    )

    extends("python")

    # Uses collections.MutableMapping

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/p/pip/pip-{1}-{0}-none-any.whl"
        if version >= Version("21"):
            python_tag = "py3"
        else:
            python_tag = "py2.py3"
        return url.format(python_tag, version)

    def install(self, spec, prefix):
        # To build and install pip from source, you need setuptools, wheel, and pip
        # already installed. We get around this by using a pre-built wheel to install
        # itself, see:
        # https://discuss.python.org/t/bootstrapping-a-specific-version-of-pip/12306
        whl = self.stage.archive_file
        args = [os.path.join(whl, "pip")] + std_pip_args + ["--prefix=" + prefix, whl]
        python(*args)

    def setup_dependent_package(self, module, dependent_spec):
        pip = dependent_spec["python"].command
        pip.add_default_arg("-m", "pip")
        setattr(module, "pip", pip)
