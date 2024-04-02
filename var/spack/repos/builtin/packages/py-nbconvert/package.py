# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbconvert(PythonPackage):
    """Jupyter Notebook Conversion"""

    homepage = "https://github.com/jupyter/nbconvert"
    pypi = "nbconvert/nbconvert-6.0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "7.14.1",
        sha256="aa83e3dd27ea38d0c1d908e3ce9518d15fa908dd30521b6d5040bd23f33fffb0",
        url="https://pypi.org/packages/17/d3/7d08470a59e591f73afbc685d910886f96a38be86df3ca95398c491b8d23/nbconvert-7.14.1-py3-none-any.whl",
    )
    version(
        "7.4.0",
        sha256="af5064a9db524f9f12f4e8be7f0799524bd5b14c1adea37e34e83c95127cc818",
        url="https://pypi.org/packages/2f/90/79bf16b584f5150550b0c175ca7a6e88334226e9275cf16db13785105d73/nbconvert-7.4.0-py3-none-any.whl",
    )
    version(
        "7.0.0",
        sha256="26843ae233167e8aae31c20e3e1d91f431f04c9f34363bbe2dd0d247f772641c",
        url="https://pypi.org/packages/b9/66/67e0a0f9e9cb0172d0d92686166418f69ec702ff7db2acca8c8caf325d0d/nbconvert-7.0.0-py3-none-any.whl",
    )
    version(
        "6.5.1",
        sha256="0a3e224ee753ac4dceeb0257c4a315c069dcc6f9f4ae0ad15c5ea84713d15e28",
        url="https://pypi.org/packages/54/d1/c3cc6a8144e9a0b25e2c66ac09a57fb05c01ad2d5f03b671fbe50d8aed81/nbconvert-6.5.1-py3-none-any.whl",
    )
    version(
        "6.5.0",
        sha256="c56dd0b8978a1811a5654f74c727ff16ca87dd5a43abd435a1c49b840fcd8360",
        url="https://pypi.org/packages/e8/f9/2de57146b8995d7f1b68d6fd0b4751d68c23f52e6f4ad926a7274184e8f2/nbconvert-6.5.0-py3-none-any.whl",
    )
    version(
        "6.4.2",
        sha256="7b006ae9979af56200e7fa3db39d9d12c99e811e8843b05dbe518e5b754bcb2e",
        url="https://pypi.org/packages/ac/e0/28f63b4dd05fa751b4b10e54f8a7cb15a5086320baad8700be41dc96eac0/nbconvert-6.4.2-py3-none-any.whl",
    )
    version(
        "6.3.0",
        sha256="8f23fbeabda4a500685d788ee091bf22cf34119304314304fb39f16e2fc32f37",
        url="https://pypi.org/packages/95/45/8d349273c93ca07e433eb561bf03e0d7ae8e0303904371eee2e0fbe0b037/nbconvert-6.3.0-py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="b1b9dc4f1ff6cafae0e6d91f42fb9046fdc32e6beb6d7e2fa2cd7191ad535240",
        url="https://pypi.org/packages/19/c7/f7d49d1347b87a6c9324688ead2f02e1c119b20e0cc0474e69edfe63ff11/nbconvert-6.2.0-py3-none-any.whl",
    )
    version(
        "6.0.1",
        sha256="970122eaf3a3ddcfe4e03514b219df4be4af09e70c748faf6ba96f51a25fd09b",
        url="https://pypi.org/packages/e3/7f/ecd2d1f370c55c09b46deb6d400a0619582e4391e16993fd43487963c916/nbconvert-6.0.1-py3-none-any.whl",
    )
    version(
        "5.6.0",
        sha256="48d3c342057a2cf21e8df820d49ff27ab9f25fc72b8f15606bd47967333b2709",
        url="https://pypi.org/packages/f9/df/4505c0a7fea624cac461d0f41051f33456ae656753f65cee8c2f43121cb2/nbconvert-5.6.0-py2.py3-none-any.whl",
    )
    version(
        "5.5.0",
        sha256="4a978548d8383f6b2cfca4a3b0543afb77bc7cb5a96e8b424337ab58c12da9bc",
        url="https://pypi.org/packages/35/e7/f46c9d65f149271e47fca6ab084ef5c6e4cb1870f4c5cce6690feac55231/nbconvert-5.5.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="fde887f769d8a727f3496999aa388b07355220b5a7c0479840f41b0c9f0be77f",
        url="https://pypi.org/packages/55/76/7989c6958ac939324ccc1589cfed0bb1f5cd984e604a24a8ea525b97b7c2/nbconvert-4.2.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="18542116114f4340bbde64204cfb542612dfb6a6dcade3caedf13909834e27b5",
        url="https://pypi.org/packages/26/98/39e08d99ba3a514203973d2d1c9098f1db5e95652951670962bb6f8e7514/nbconvert-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="8fbbc2739ce3dd0d893ba2ffd30e719407057e742ecaf0ba260e42f4a9b54c4e",
        url="https://pypi.org/packages/50/14/eedaf095daeb4bf13c14748c0522aeb5a4989ad67cf42ae56e41ed79086c/nbconvert-4.0.0-py2.py3-none-any.whl",
    )

    variant("serve", default=True, description="Include a webserver")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@7.7:")
        depends_on("python@3.7:", when="@6.1:7.6")
        depends_on("py-beautifulsoup4", when="@6.4.4:")
        depends_on("py-bleach@:4,5.0.1:", when="@7.5:")
        depends_on("py-bleach", when="@5:7.4")
        depends_on("py-defusedxml", when="@5.4:")
        depends_on("py-entrypoints@0.2.2:", when="@5.0.0:7.0.0-rc1")
        depends_on("py-entrypoints", when="@4.2:5.0.0-beta1")
        depends_on("py-importlib-metadata@3.6:", when="@7.0.0-rc2: ^python@:3.9")
        depends_on("py-jinja2@3.0.0:", when="@6.5:")
        depends_on("py-jinja2@2.4:", when="@5.5:6.4")
        depends_on("py-jinja2", when="@4.2:5.4")
        depends_on("py-jupyter-core@4.7.0:", when="@6.5:")
        depends_on("py-jupyter-core", when="@4.2:6.4")
        depends_on("py-jupyterlab-pygments", when="@6:")
        depends_on("py-lxml", when="@6.5.1:6,7.0.0:7.0")
        depends_on("py-markupsafe@2.0.0:", when="@6.4.5:")
        depends_on("py-mistune@2.0.3:", when="@7.6:")
        depends_on("py-mistune@2.0.3:2", when="@7.0.0:7.5")
        depends_on("py-mistune@0.8.1:0", when="@5.6:6")
        depends_on("py-mistune@0.8.1:", when="@5.4:5.5")
        depends_on("py-mistune@:0.5,0.7:", when="@4.2:5.2")
        depends_on("py-nbclient@0.5:", when="@6.5:")
        depends_on("py-nbclient@0.5", when="@6.0.0-rc0:6.4")
        depends_on("py-nbformat@5.7:", when="@7.5:")
        depends_on("py-nbformat@5.1:", when="@6.5:7.4")
        depends_on("py-nbformat@4.4:", when="@5.3:6.4")
        depends_on("py-nbformat", when="@4.2:5.2")
        depends_on("py-packaging", when="@6.5:")
        depends_on("py-pandocfilters@1.4.1:", when="@5.0.0:")
        depends_on("py-pygments@2.4.1:", when="@6:")
        depends_on("py-pygments", when="@4.2:5")
        depends_on("py-testpath", when="@5.0.0:6.4")
        depends_on("py-tinycss2", when="@6.5:")
        depends_on("py-tornado@6.1:", when="@6.5:+serve")
        depends_on("py-tornado@4:", when="@5:6.4+serve")
        depends_on("py-tornado", when="@4.2:4+serve")
        depends_on("py-traitlets@5.1:", when="@7.5:")
        depends_on("py-traitlets@5.0.0:", when="@6.1:7.4")
        depends_on("py-traitlets@4.2:", when="@5:6.0")
        depends_on("py-traitlets", when="@4.2:4")

    # https://bugs.gentoo.org/720870
    # https://github.com/jupyter/nbconvert/pull/937

    # Historical dependencies

    conflicts("^bleach@5.0.0")

    resource(
        name="index.css",
        url="https://unpkg.com/@jupyterlab/nbconvert-css@4.0.2/style/index.css",
        sha256="917ff47850a7cc08fd0658026fda7672a85220aaab258e8849e891b37426f947",
        placement="resource_index.css",
        when="@6:",
        expand=False,
    )
    resource(
        name="theme-light.css",
        url="https://unpkg.com/@jupyterlab/theme-light-extension@4.0.2/style/variables.css",
        sha256="11bf3558fd3ed353a4c1401ac0c1730d01df073f6436d357c5bbf02a03bd6962",
        placement="resource_theme-light.css",
        when="@6:",
        expand=False,
    )
    resource(
        name="theme-dark.css",
        url="https://unpkg.com/@jupyterlab/theme-dark-extension@4.0.2/style/variables.css",
        sha256="795f2d5069737cbeb5cba01e6b5c7cadbde227c909e43004c5a60f58d5160aec",
        placement="resource_theme-dark.css",
        when="@6:",
        expand=False,
    )
    resource(
        name="style.css",
        url="https://cdn.jupyter.org/notebook/5.4.0/style/style.min.css",
        sha256="5865a609f4437b0464bc121cd567b619074e540a0515a3b82f222f764eb51e01",
        placement="resource_style.css",
        when="@6:",
        expand=False,
    )

    def setup_run_environment(self, env):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)
