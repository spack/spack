# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDatatrove(PythonPackage):
    """Data processing and machine learning toolkit from Hugging Face."""

    homepage = "https://github.com/huggingface/datatrove"
    pypi = "datatrove/datatrove-0.4.0.tar.gz"

    maintainers("thomas-bouvier")

    license("Apache-2.0")

    version("0.5.0", sha256="b1fb13324e86126dace2de2dcaa7aeab53facfc1628f5f6e0ecf5789c78649ad")
    version("0.4.0", sha256="c29a873a12ed8d3b089d9adbc80078db3ec45de94ca9e9bf851e0a5c5ce474c3")

    # Python version requirement
    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-dill@0.3.0:", type=("build", "run"))
    depends_on("py-fsspec@2023.12.2:", type=("build", "run"))
    depends_on("py-huggingface-hub@0.17.0:", type=("build", "run"))
    depends_on("py-humanize", type=("build", "run"))
    depends_on("py-loguru@0.7.0:", type=("build", "run"))
    depends_on("py-multiprocess", type=("build", "run"))
    depends_on("py-numpy@2:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))

    variant("io", default=True, description="Enable IO features")
    variant("processing", default=True, description="Enable advanced processing features")

    with when("+io"):
        depends_on("py-faust-cchardet", type=("build", "run"))
        depends_on("py-pyarrow", type=("build", "run"))
        depends_on("py-python-magic", type=("build", "run"))
        depends_on("py-warcio", type=("build", "run"))
        depends_on("py-datasets@3.1.0:", type=("build", "run"))
        depends_on("py-orjson", type=("build", "run"))
        depends_on("py-zstandard", type=("build", "run"))

    with when("+processing"):
        depends_on("py-fasttext-numpy2", type=("build", "run"))
        depends_on("py-nltk", type=("build", "run"))
        depends_on("py-inscriptis", type=("build", "run"))
        depends_on("py-tldextract", type=("build", "run"))
        depends_on("py-trafilatura@1.8.0:1.11", type=("build", "run"))
        depends_on("py-tokenizers", type=("build", "run"))
        depends_on("py-ftfy", type=("build", "run"))
        depends_on("py-fasteners", type=("build", "run"))
        depends_on("py-regex", type=("build", "run"))
        depends_on("py-xxhash", type=("build", "run"))
        depends_on("kenlm +python", type=("build", "run"))
        depends_on("py-pyahocorasick", type=("build", "run"))
