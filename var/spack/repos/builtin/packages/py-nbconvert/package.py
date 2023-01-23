# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbconvert(PythonPackage):
    """Jupyter Notebook Conversion"""

    homepage = "https://github.com/jupyter/nbconvert"
    pypi = "nbconvert/nbconvert-6.0.1.tar.gz"

    version("7.0.0", sha256="fd1e361da30e30e4c5a5ae89f7cae95ca2a4d4407389672473312249a7ba0060")
    version("6.5.1", sha256="2c01f3f518fee736c3d3f999dd20e0a16febba17a0d60a3b0fd28fbdec14115d")
    version("6.5.0", sha256="223e46e27abe8596b8aed54301fadbba433b7ffea8196a68fd7b1ff509eee99d")
    version("6.4.2", sha256="eb2803db18f6facce6bf3b01b684fe47907994bd156d15eaccdf011e3d7f8164")
    version("6.3.0", sha256="5e77d6203854944520105e38f2563a813a4a3708e8563aa598928a3b5ee1081a")
    version("6.2.0", sha256="16ceecd0afaa8fd26c245fa32e2c52066c02f13aa73387fffafd84750baea863")
    version("6.0.1", sha256="db94117fbac29153834447e31b30cda337d4450e46e0bdb1a36eafbbf4435156")
    version("5.6.0", sha256="427a468ec26e7d68a529b95f578d5cbf018cb4c1f889e897681c2b6d11897695")
    version("5.5.0", sha256="138381baa41d83584459b5cfecfc38c800ccf1f37d9ddd0bd440783346a4c39c")
    version("4.2.0", sha256="55946d7522741294fcdd50799bd1777d16673ce721fecca0610cdb86749863c6")
    version("4.1.0", sha256="e0296e45293dd127d028f678e3b6aba3f1db3283a134178bdb49eea402d4cf1c")
    version("4.0.0", sha256="472ad15d1a71f1ef00c4094c11bb93638858fc89fb2c5838b3aa6b67d981b437")

    variant("serve", default=True, description="Include a webserver")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@5:", type=("build", "run"))
    depends_on("python@3.6:", when="@6:", type=("build", "run"))
    depends_on("python@3.7:", when="@6.2.0:", type=("build", "run"))
    depends_on("py-setuptools", when="@5:6", type=("build", "run"))
    depends_on("py-setuptools@60:", when="@6.5:6", type=("build", "run"))
    depends_on("py-hatchling@0.25:", when="@7:", type="build")
    depends_on("py-lxml", when="@6.5.1:", type=("build", "run"))
    depends_on("py-beautifulsoup4", when="@6.4.4:", type=("build", "run"))
    depends_on("py-bleach", when="@5:", type=("build", "run"))
    depends_on("py-defusedxml", when="@5:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", when="@7: ^python@:3.9", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jinja2@2.4:", when="@5:", type=("build", "run"))
    depends_on("py-jinja2@3:", when="@6.5:", type=("build", "run"))
    depends_on("py-jupyter-core", type=("build", "run"))
    depends_on("py-jupyter-core@4.7:", when="@6.5:", type=("build", "run"))
    depends_on("py-jupyterlab-pygments", when="@6:", type=("build", "run"))
    depends_on("py-markupsafe@2:", when="@6.4.5:", type=("build", "run"))
    depends_on("py-mistune@0.8.1:1", when="@:6", type=("build", "run"))
    depends_on("py-mistune@2.0.3:2", when="@7:", type=("build", "run"))
    depends_on("py-nbclient@0.5", when="@6:6.4", type=("build", "run"))
    depends_on("py-nbclient@0.5:", when="@6.5:", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-nbformat@4.4:", when="@5:", type=("build", "run"))
    depends_on("py-nbformat@5.1:", when="@6.5:", type=("build", "run"))
    depends_on("py-packaging", when="@6.5:", type=("build", "run"))
    depends_on("py-pandocfilters@1.4.1:", when="@5:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-pygments@2.4.1:", when="@6:", type=("build", "run"))
    depends_on("py-tinycss2", when="@6.5:", type=("build", "run"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("py-traitlets@4.2:", when="@5:", type=("build", "run"))
    depends_on("py-traitlets@5:", when="@6.2.0:", type=("build", "run"))
    depends_on("py-entrypoints", when="@:6", type=("build", "run"))
    depends_on("py-entrypoints@0.2.2:", when="@5:6", type=("build", "run"))
    depends_on("py-testpath", when="@5:6.4", type=("build", "run"))

    # https://bugs.gentoo.org/720870
    # https://github.com/jupyter/nbconvert/pull/937
    depends_on("py-tornado@6.1:", when="@6.5: +serve", type=("build", "run"))
    depends_on("py-tornado@4.0:", when="@5.4.1: +serve", type=("build", "run"))
    depends_on("py-tornado@4.0:5", when="@:5.4.0 +serve", type=("build", "run"))

    def patch(self):
        # We bundle this with the spack package so that the installer
        # doesn't try to download it.
        install(
            join_path(self.package_dir, "style.min.css"),
            join_path("nbconvert", "resources", "style.min.css"),
        )

    def setup_run_environment(self, env):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)
