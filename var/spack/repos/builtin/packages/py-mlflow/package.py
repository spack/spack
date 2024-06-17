# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlflow(PythonPackage):
    """MLflow: A Platform for ML Development and Productionization."""

    homepage = "https://pypi.org/project/mlflow/"
    pypi = "mlflow/mlflow-2.0.1.tar.gz"

    license("Apache-2.0")

    version("2.13.2", sha256="8f1cf42a24aee26e527a86ec1c5265119d17a97528e729d4a96e781d37d50a2d")
    version("2.13.1", sha256="ece1b0baef69da5ff03e4687009417481790544ec64a3821bdcc1cc1513b12d3")
    version("2.13.0", sha256="5ac62430d4dc863b3bafdf7b59cfc9a31ab18878c1c0ff687d8783fdc08a0659")
    version("2.12.2", sha256="d712f1af9d44f1eb9e1baee8ca64f7311e185b7572fc3c1e0a83a4c8ceff6aad")
    version("2.12.1", sha256="aa92aebb2379a9c5484cbe901cdf779d5408ac96a641e4b1f8a2d1ff974db7c9")
    version("2.12.0", sha256="3e8f432d5494f08b341b249d7b721f4f688a4b1efe22c26118ee22bbdf24a462")
    version("2.11.4", sha256="6c23b15a95c5a1e55ecddf014a226b6d8a8904138172c04ba716398dea76cea1")
    version("2.11.3", sha256="621b7e311e890b79719c2e7777286d8e08d38dd04d5ab080966990bd4a55febb")
    version("2.11.2", sha256="8d29c0a57ec9c8aceede5d47df8ca3741ee0808eb0723840f57b83556a623434")
    version("2.11.1", sha256="a2ec29ee862f19955208fb8e05e51e5e9d2edc7175e37cf136d943b981a824e9")
    version("2.11.0", sha256="5fc6046a94e4269564dbeb748bb791ccb5c671a9c5c2b91ef3713c16aa614595")
    version("2.10.2", sha256="3ddf32ba2c01dac79e4d077d4bb9ed46d82a082dc99223207d562c7ee6bee671")
    version("2.10.1", sha256="d534e658a979517f56478fc7f0b1a19451700078a725242e789fe63c87d46815")
    version("2.10.0", sha256="9a97abceae240b9831080a16afc3eb668b339b9ca4382fb3bd6a7a2fc7bd0951")
    version("2.9.2", sha256="25f2ad3d0b0e78bd32296058fb4c315dff4379515cd669ac6137f39507b9dfe9")
    version("2.9.1", sha256="1e863fd6fe2f9aa0b2dee09f72c4d0131ecb70e24bbc6e3ebc4321802397d0c8")
    version("2.9.0", sha256="937ef806f46d5ad5a0e32367954ec86eb0d301c3dccb4b3ef01d7156274f73b8")
    version("2.8.1", sha256="e4e5bdd2d9efb0b386ecbce2df7e43f04c46a32080208414dc53b5fd71559678")
    version("2.8.0", sha256="75bdc7768ba950aa5c98dd4792a74ec372a4ac2b86d714ee565af18ebede4524")
    version("2.7.1", sha256="853b2038496fb8f85cad205943dede877f65ab86e856f296587885dafcef643d")
    version("2.7.0", sha256="deaf0f5f27608e9526d69fffcca70c822ac90ea290a6f3e4bb3dfa1b209b0111")
    version("2.6.0", sha256="fd569232e65d69c0cb7006847b1a1bd80831bf0e19378052a44ee5c0ae349182")
    version("2.5.0", sha256="f992ae8ea9c73502344baf48c4ec447aa9efbfa8965bc090868e6163234f4eb0")
    version("2.4.2", sha256="0b1a71b0ff4679dce8ff2ae9733e996ec0b6c106db93412e0df8606f791867c8")
    version("2.4.1", sha256="6598f78f7ece59a9480573af57b09708a3283ece88f196e5d172c2040cec323f")
    version("2.4.0", sha256="ecd5258b688a4cb1ef5282b19da6d6832b9c0d66a827a4dcf5779d90a0dff247")
    version("2.3.2", sha256="6d2b0ffc09fe58c9b523d5ea7b1fd4ab64664e2616d2d2040d9e96796df6eb6d")
    version("2.3.1", sha256="63439397b2718ce5747288ef5475f46b3716b370a517be3e3c67b799a247a186")
    version("2.3.0", sha256="2a7ba60a2c790c7ea742f486838706d586fab701fec308ea4c732f4bbadd8409")
    version("2.2.2", sha256="3ef2c2ee20c9a7adedff34e756c6edac62cf4d905765ad0e8074bc9daa0c580c")
    version("2.2.1", sha256="85a19929292aafa08cc5c8d297c1d0e666ace775a59a414c5f67cb65967fe967")
    version("2.2.0", sha256="ad7a2c4fa561fe0c852f296c2cd3739083825ac44c48d44358433abe397e306b")
    version("2.1.1", sha256="a116b3cd45bbfb509a1723bfd4388bdb566a3e5045e3cde5390e667f591498a6")
    version("2.0.1", sha256="7ce6caf3c6acb022d6f5ce8a0995a92be1db524ae16aade1f83da661cdf993de")
    version("1.17.0", sha256="4898c58899e3101e09e2b37cf5bee7db04c5d73389a56942d3ef5a5e4396799e")

    depends_on("python@3.6:", type=("build", "run"), when="@1.17.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@1.24.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@2.0.1:")
    depends_on("py-setuptools", type="build")

    depends_on("py-click@7.0:8", type=("build", "run"))
    depends_on("py-cloudpickle@:2", type=("build", "run"))
    depends_on("py-databricks-cli@0.8.7:0", type=("build", "run"))
    depends_on("py-entrypoints@:0", type=("build", "run"))
    depends_on("py-gitpython@2.1.0:3", type=("build", "run"))
    depends_on("py-pyyaml@5.1:6", type=("build", "run"))
    depends_on("py-protobuf@3.12.0:4", type=("build", "run"))
    depends_on("py-pytz@:2022", type=("build", "run"))
    depends_on("py-requests@2.17.3:2", type=("build", "run"))
    depends_on("py-packaging@:21", type=("build", "run"))
    depends_on("py-importlib-metadata@3.7:4.6,4.7.1:5", type=("build", "run"))
    depends_on("py-sqlparse@0.4.0:0", type=("build", "run"))

    depends_on("py-alembic@:1", type=("build", "run"))
    depends_on("py-docker@4.0.0:6", type=("build", "run"))
    depends_on("py-flask@:2", type=("build", "run"))
    depends_on("py-numpy@:1", type=("build", "run"))
    depends_on("py-scipy@:1", type=("build", "run"))
    depends_on("py-pandas@:1", type=("build", "run"))
    depends_on("py-querystring-parser@:1", type=("build", "run"))
    depends_on("py-sqlalchemy@1.4.0:1", type=("build", "run"))
    for platform in ["linux", "darwin"]:
        depends_on("py-gunicorn@:20", type=("build", "run"), when=f"platform={platform}")
    depends_on("py-waitress@:2", type=("build", "run"), when="platform=windows")
    depends_on("py-scikit-learn@:1", type=("build", "run"))
    depends_on("py-pyarrow@4.0.0:10", type=("build", "run"))
    depends_on("py-shap@0.40:0", type=("build", "run"))
    depends_on("py-markdown@3.3:3", type=("build", "run"))
    for platform in ["linux", "darwin"]:
        depends_on("py-jinja2@2.11:3", type=("build", "run"), when=f"platform={platform}")
    depends_on("py-jinja2@3.0:3", type=("build", "run"), when="platform=windows")
    depends_on("py-matplotlib@:3", type=("build", "run"))
