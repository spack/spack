# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchgeo(PythonPackage):
    """TorchGeo: datasets, samplers, transforms, and pre-trained models for geospatial data.

    TorchGeo is a PyTorch domain library, similar to torchvision, providing datasets, samplers,
    transforms, and pre-trained models specific to geospatial data.
    """

    homepage = "https://github.com/microsoft/torchgeo"
    pypi = "torchgeo/torchgeo-0.1.0.tar.gz"
    git = "https://github.com/microsoft/torchgeo.git"

    maintainers("adamjstewart", "calebrob6")

    version("main", branch="main")
    version("0.4.0", sha256="a0812487205aa2db7bc92119d896ae4bf4f1014e6fdc0ce0f75bcb24fada6613")
    version("0.3.1", sha256="ba7a716843575d173abab383c6cc2d5fc8faf5834472f16a4abe1b932040ece5")
    version("0.3.0", sha256="3d98fd58e6678555592a596bd079ed5a8b4959996ff7718d7caa48d47815b6b0")
    version("0.2.1", sha256="218bd5aed7680244688dbf0f1398f5251ad243267eb19a6a7332668ac779a1cc")
    version("0.2.0", sha256="968c4bf68c7e487bf495f2f306d8bb0f5824eb67e24b26772a510e753e04ba4c")
    version("0.1.1", sha256="6e28132f75e9d8cb3a3a0e8b443aba3cde26c8f3140b9426139ee6e8f8058b26")
    version("0.1.0", sha256="44eb3cf10ab2ac63ff95e92fcd3807096bac3dcb9bdfe15a8edac9d440d2f323")

    variant("datasets", default=False, description="Install optional dataset dependencies")
    variant("docs", default=False, description="Install documentation dependencies")
    variant("style", default=False, description="Install style checking tools")
    variant("tests", default=False, description="Install testing tools")

    # Required dependencies
    depends_on("python@3.7:3+bz2", when="@0.3:", type=("build", "run"))
    depends_on("python@3.6:3+bz2", when="@:0.2", type=("build", "run"))
    depends_on("py-setuptools@42:66", when="@0.4:", type="build")
    depends_on("py-setuptools@42:65", when="@0.3.1", type="build")
    depends_on("py-setuptools@42:63", when="@:0.3.0", type="build")
    depends_on("py-einops@0.3:0.6", when="@0.4:", type=("build", "run"))
    depends_on("py-einops@0.3:0.4", when="@:0.3", type=("build", "run"))
    depends_on("py-fiona@1.8:2", when="@0.4:", type=("build", "run"))
    depends_on("py-fiona@1.8:1", when="@0.3", type=("build", "run"))
    depends_on("py-fiona@1.5:1", when="@:0.2", type=("build", "run"))
    depends_on("py-kornia@0.6.5:0.6", when="@0.4.1:", type=("build", "run"))
    depends_on("py-kornia@0.6.5:0.6.9", when="@0.4.0", type=("build", "run"))
    depends_on("py-kornia@0.6.4:0.6.9", when="@0.3", type=("build", "run"))
    depends_on("py-kornia@0.5.11:0.6.9", when="@0.2", type=("build", "run"))
    depends_on("py-kornia@0.5.4:0.6.9", when="@0.1", type=("build", "run"))
    depends_on("py-matplotlib@3.3:3", type=("build", "run"))
    depends_on("py-numpy@1.17.2:1", type=("build", "run"))
    depends_on("py-omegaconf@2.1:2", type=("build", "run"))
    depends_on("py-packaging@17:21", when="@0.3", type=("build", "run"))
    depends_on("pil@6.2:9+zlib+jpeg+tiff", type=("build", "run"))
    depends_on("py-pyproj@2.2:3", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.5.1:1+extra", when="@0.4:", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.5.1:1", when="@0.3.1", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.5.1:1.8", when="@0.3.0", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.3:1.8", when="@:0.2", type=("build", "run"))
    depends_on("py-rasterio@1.0.20:1", when="@0.3:", type=("build", "run"))
    depends_on("py-rasterio@1.0.16:1", when="@:0.2", type=("build", "run"))
    depends_on("py-rtree@1", when="@0.3:", type=("build", "run"))
    depends_on("py-rtree@0.9.4:1", when="@0.2.1", type=("build", "run"))
    depends_on("py-rtree@0.5:1", when="@:0.2.0", type=("build", "run"))
    depends_on("py-scikit-learn@0.21:1", when="@0.3:", type=("build", "run"))
    depends_on("py-scikit-learn@0.18:1", when="@:0.2", type=("build", "run"))
    depends_on("py-segmentation-models-pytorch@0.2:0.3", when="@0.3.1:", type=("build", "run"))
    depends_on("py-segmentation-models-pytorch@0.2", when="@:0.3.0", type=("build", "run"))
    depends_on("py-shapely@1.3:2", when="@0.4:", type=("build", "run"))
    depends_on("py-shapely@1.3:1", when="@:0.3", type=("build", "run"))
    depends_on("py-timm@0.4.12:0.6", when="@0.4:", type=("build", "run"))
    depends_on("py-timm@0.4.12:0.4", when="@:0.3", type=("build", "run"))
    depends_on("py-torch@1.12:1", when="@0.4:", type=("build", "run"))
    depends_on("py-torch@1.9:1", when="@0.2:0.3", type=("build", "run"))
    depends_on("py-torch@1.7:1", when="@0.1", type=("build", "run"))
    depends_on("py-torchmetrics@0.10:0.11", when="@0.4:", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:0.9", when="@0.3", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:0.8", when="@0.2.1", type=("build", "run"))
    depends_on("py-torchmetrics@0.7", when="@:0.2.0", type=("build", "run"))
    depends_on("py-torchvision@0.13:0.14", when="@0.4:", type=("build", "run"))
    depends_on("py-torchvision@0.10:0.13", when="@0.3", type=("build", "run"))
    depends_on("py-torchvision@0.10:0.12", when="@0.2", type=("build", "run"))
    depends_on("py-torchvision@0.3:0.12", when="@0.1", type=("build", "run"))

    # Optional dependencies
    with when("+datasets"):
        depends_on("py-h5py@2.6:3", type="run")
        depends_on("py-laspy@2", when="@0.2:", type="run")
        depends_on("gdal+openjpeg", when="@0.3.1:", type="run")
        depends_on("libtiff+jpeg+zlib", type="run")
        depends_on("open3d@0.11.2:0.14+python", when="@0.2:0.3", type="run")
        depends_on("opencv@3.4.2.17:4+python3+imgcodecs+tiff+jpeg+png", type="run")
        depends_on("py-pandas@0.23.2:1", when="@0.3:", type="run")
        depends_on("py-pandas@0.19.1:1", when="@0.2", type="run")
        depends_on("py-pycocotools@2", type="run")
        depends_on("py-pyvista@0.20:0.37", when="@0.4:", type="run")
        depends_on("py-radiant-mlhub@0.2.1:0.4", type="run")
        depends_on("py-rarfile@3:4", type="run")
        depends_on("py-scipy@1.6.2:1", when="@0.4:", type="run")
        depends_on("py-scipy@1.2:1", when="@0.3", type="run")
        depends_on("py-scipy@0.9:1", when="@:0.2", type="run")
        depends_on("py-zipfile-deflate64@0.2", when="@0.2.1:", type="run")

    with when("+docs"):
        depends_on("py-ipywidgets@7:8", when="@0.3.1:", type="run")
        depends_on("py-ipywidgets@7", when="@:0.3.0", type="run")
        depends_on("py-nbsphinx@0.8.5:0.8", type="run")
        depends_on("py-pytorch-sphinx-theme", type="run")
        depends_on("py-sphinx@4:6", when="@0.4:", type="run")
        depends_on("py-sphinx@4:5", when="@:0.3", type="run")

    with when("+style"):
        depends_on("py-black@21.8:22+jupyter", when="@0.3:", type="run")
        depends_on("py-black@21:22", when="@:0.2", type="run")
        depends_on("py-flake8@3.8:6", when="@0.4:", type="run")
        depends_on("py-flake8@3.8:5", when="@0.3.1", type="run")
        depends_on("py-flake8@3.8:4", when="@:0.3.0", type="run")
        depends_on("py-isort@5.8:5+colors", type="run")
        depends_on("py-pydocstyle@6.1:6+toml", type="run")
        depends_on("py-pyupgrade@1.24:3", when="@0.4:", type="run")
        depends_on("py-pyupgrade@1.24:2", when="@0.3", type="run")

    with when("+tests"):
        depends_on("py-mypy@0.900:0.991", when="@0.4:", type="run")
        depends_on("py-mypy@0.900:0.971", when="@0.3.1", type="run")
        depends_on("py-mypy@0.900:0.961", when="@:0.3.0", type="run")
        depends_on("py-nbmake@0.1:1", when="@0.3.1:", type="run")
        depends_on("py-nbmake@0.1:1.1", when="@:0.3.0", type="run")
        depends_on("py-pytest@6.1.2:7", type="run")
        depends_on("py-pytest-cov@2.4:4", when="@0.4:", type="run")
        depends_on("py-pytest-cov@2.4:3", when="@:0.3", type="run")
