# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinx(PythonPackage):
    """Sphinx Documentation Generator."""

    homepage = "https://www.sphinx-doc.org/en/master/"
    pypi = "Sphinx/Sphinx-3.2.0.tar.gz"

    maintainers("adamjstewart")

    version("6.0.0", sha256="58c140ecd9aa0abbc8ff6da48a266648eac9e5bfc8e49576efd2979bf46f5961")

    version("5.3.0", sha256="51026de0a9ff9fc13c05d74913ad66047e104f56a129ff73e174eb5c3ee794b5")
    version("5.2.3", sha256="5b10cb1022dac8c035f75767799c39217a05fc0fe2d6fe5597560d38e44f0363")
    version("5.2.2", sha256="7225c104dc06169eb73b061582c4bc84a9594042acae6c1582564de274b7df2f")
    version("5.2.1", sha256="c009bb2e9ac5db487bcf53f015504005a330ff7c631bb6ab2604e0d65bae8b54")
    version("5.2.0", sha256="1790c2098937dcfa7871c9d102c24eccd4a8b883b67c5c1e26892fb52d102542")
    version("5.1.1", sha256="ba3224a4e206e1fbdecf98a4fae4992ef9b24b85ebf7b584bb340156eaf08d89")
    version("5.1.0", sha256="7893d10d9d852c16673f9b1b7e9eda1606b420b7810270294d6e4b44c0accacc")
    version("5.0.2", sha256="b18e978ea7565720f26019c702cd85c84376e948370f1cd43d60265010e1c7b0")
    version("5.0.1", sha256="f4da1187785a5bc7312cc271b0e867a93946c319d106363e102936a3d9857306")
    version("5.0.0", sha256="464d9c1bd5613bcebe76b46658763f3f3dbb184da7406e632a84596d3cd8ee90")

    version("4.5.0", sha256="7bf8ca9637a4ee15af412d1a1d9689fec70523a68ca9bb9127c2f3eeb344e2e6")
    version("4.4.0", sha256="6caad9786055cb1fa22b4a365c1775816b876f91966481765d7d50e9f0dd35cc")
    version("4.3.2", sha256="0a8836751a68306b3fe97ecbe44db786f8479c3bf4b80e3a7f5c838657b4698c")
    version("4.3.1", sha256="32a5b3e9a1b176cc25ed048557d4d3d01af635e6b76c5bc7a43b0a34447fbd45")
    version("4.3.0", sha256="6d051ab6e0d06cba786c4656b0fe67ba259fe058410f49e95bee6e49c4052cbf")
    version("4.2.0", sha256="94078db9184491e15bce0a56d9186e0aec95f16ac20b12d00e06d4e36f1058a6")
    version("4.1.2", sha256="3092d929cd807926d846018f2ace47ba2f3b671b309c7a89cd3306e80c826b13")
    version("4.1.1", sha256="23c846a1841af998cb736218539bb86d16f5eb95f5760b1966abcd2d584e62b8")
    version("4.1.0", sha256="4219f14258ca5612a0c85ed9b7222d54da69724d7e9dd92d1819ad1bf65e1ad2")
    version("4.0.3", sha256="dff357e6a208eb7edb2002714733ac21a9fe597e73609ff417ab8cf0c6b4fbb8")
    version("4.0.2", sha256="b5c2ae4120bf00c799ba9b3699bc895816d272d120080fbc967292f29b52b48c")
    version("4.0.1", sha256="cf5104777571b2b7f06fa88ee08fade24563f4a0594cf4bd17d31c47b8740b4c")
    version("4.0.0", sha256="b246ebd74f5fb966d7e90086bbda5ed74ee4d30b4c3cbefddc1fb5210aa317c7")

    version("3.5.4", sha256="19010b7b9fa0dc7756a6e105b2aacd3a80f798af3c25c273be64d7beeb482cb1")
    version("3.4.1", sha256="e450cb205ff8924611085183bf1353da26802ae73d9251a8fcdf220a8f8712ef")
    version("3.2.0", sha256="cf2d5bc3c6c930ab0a1fbef3ad8a82994b1bf4ae923f8098a05c7e5516f07177")
    version("3.0.0", sha256="6a099e6faffdc3ceba99ca8c2d09982d43022245e409249375edf111caf79ed3")

    version("2.4.4", sha256="b4c750d546ab6d7e05bdff6ac24db8ae3e8b8253a3569b754e445110a0a12b66")
    version("2.2.0", sha256="0d586b0f8c2fc3cc6559c5e8fd6124628110514fda0e5d7c82e682d749d2e845")

    version("1.8.5", sha256="c7658aab75c920288a8cf6f09f244c6cfdae30d82d803ac1634d9f223a80ca08")
    version("1.8.4", sha256="c1c00fc4f6e8b101a0d037065043460dffc2d507257f2f11acaed71fd2b0c83c")
    version("1.8.2", sha256="120732cbddb1b2364471c3d9f8bfd4b0c5b550862f99a65736c77f970b142aea")
    version("1.7.4", sha256="e9b1a75a3eae05dded19c80eb17325be675e0698975baae976df603b6ed1eb10")
    version("1.6.3", sha256="af8bdb8c714552b77d01d4536e3d6d2879d6cb9d25423d29163d5788e27046e6")
    version("1.6.1", sha256="7581d82c3f206f0ac380edeeba890a2e2d2be011e5abe94684ceb0df4b6acc3f")
    version("1.5.5", sha256="4064ea6c56feeb268838cb8fbbee507d0c3d5d92fa63a7df935a916b52c9e2f5")
    version("1.4.5", sha256="c5df65d97a58365cbf4ea10212186a9a45d89c61ed2c071de6090cdf9ddb4028")
    version("1.3.1", sha256="1a6e5130c2b42d2de301693c299f78cc4bd3501e78b610c08e45efc70e2b5114")

    extends("python", ignore="bin/(pybabel|pygmentize)")

    depends_on("py-flit-core@3.7:", when="@5.2:", type="build")
    depends_on("py-setuptools", when="@4.4:5.1", type="build")
    depends_on("py-setuptools", when="@:4.3", type=("build", "run"))

    depends_on("python@3.8:", when="@6:", type=("build", "run"))

    depends_on("py-sphinxcontrib-applehelp", when="@2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-devhelp", when="@2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-jsmath", when="@2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-htmlhelp@2:", when="@4.1.1:", type=("build", "run"))
    depends_on("py-sphinxcontrib-htmlhelp", when="@2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-serializinghtml@1.1.5:", when="@4.1.1:", type=("build", "run"))
    depends_on("py-sphinxcontrib-serializinghtml", when="@2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-qthelp", when="@2:", type=("build", "run"))
    depends_on("py-jinja2@3:", when="@5.2:", type=("build", "run"))
    depends_on("py-jinja2@2.3:2", when="@:4.0.1", type=("build", "run"))
    depends_on("py-jinja2@2.3:", type=("build", "run"))
    depends_on("py-pygments@2.12:", when="@5.2:", type=("build", "run"))
    depends_on("py-pygments@2:", type=("build", "run"))
    depends_on("py-docutils@0.18:0.19", when="@6:", type=("build", "run"))
    depends_on("py-docutils@0.14:0.19", when="@5.1:5", type=("build", "run"))
    depends_on("py-docutils@0.14:0.18", when="@5.0", type=("build", "run"))
    depends_on("py-docutils@0.14:0.17", when="@4", type=("build", "run"))
    depends_on("py-docutils@0.12:0.16", when="@:3", type=("build", "run"))
    depends_on("py-snowballstemmer@2:", when="@5.2:", type=("build", "run"))
    depends_on("py-snowballstemmer@1.1:", type=("build", "run"))
    depends_on("py-babel@2.9:", when="@5.2:", type=("build", "run"))
    depends_on("py-babel@1.3:", type=("build", "run"))
    depends_on("py-alabaster@0.7", type=("build", "run"))
    depends_on("py-imagesize@1.3:", when="@5.2:", type=("build", "run"))
    depends_on("py-imagesize", when="@1.4:", type=("build", "run"))
    depends_on("py-requests@2.25:", when="@6:", type=("build", "run"))
    depends_on("py-requests@2.5:", when="@2:", type=("build", "run"))
    depends_on("py-requests@2.4:", when="@1.5.2:", type=("build", "run"))
    depends_on("py-packaging@21:", when="@5.2:", type=("build", "run"))
    depends_on("py-packaging", when="@1.7:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8:", when="@5.2: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata@4.4:", when="@4.4: ^python@:3.9", type=("build", "run"))
    depends_on("py-colorama@0.4.5:", when="@5.2: platform=windows", type=("build", "run"))
    depends_on("py-colorama@0.3.5:", when="platform=windows", type=("build", "run"))

    depends_on("py-sphinxcontrib-websupport", when="@1.6:1", type=("build", "run"))
    depends_on("py-six@1.5:", when="@:1", type=("build", "run"))
    depends_on("py-sphinx-rtd-theme@0.1:", when="@:1.3", type=("build", "run"))
