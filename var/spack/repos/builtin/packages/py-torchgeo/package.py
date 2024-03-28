# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchgeo(PythonPackage):
    """TorchGeo: datasets, samplers, transforms, and pre-trained models for geospatial data."""

    homepage = "https://github.com/microsoft/torchgeo"
    pypi = "torchgeo/torchgeo-0.1.0.tar.gz"
    git = "https://github.com/microsoft/torchgeo.git"

    maintainers("adamjstewart", "calebrob6")

    license("MIT")

    version(
        "0.5.2",
        sha256="74f3e7f8247347a21b90aacb1456b12dcae95666fc89f877062177f06d9fd355",
        url="https://pypi.org/packages/71/79/067a4a656c973824d6f75677aa2be49f57ec460ce7e7c4a83f507d287873/torchgeo-0.5.2-py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="12a0c90a07c3a345d8bb4d8fd315761bb330757264c63248834091f262370e16",
        url="https://pypi.org/packages/27/32/a2610f7c0b3327e25d9cddce16205278250ee4db104c33f818f114c258ab/torchgeo-0.5.1-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="9a4d61e5b198f1dac8fd48e8c5eab1ef2abc32f70a64c0e8bc2614ac916aa6cf",
        url="https://pypi.org/packages/f4/49/21ee9d8e2e1e46a20dff0fb0c8528782a037006d2c33baf76530a417ca0a/torchgeo-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="1bf9ed519c375868f8245ff74edf2978ee6aa8ad904032bc6bca329152300a63",
        url="https://pypi.org/packages/20/01/7428c72aaf3d6c192f7c3d4fe6ec8b756a460595072db9ef75f1f5b288d9/torchgeo-0.4.1-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="eb32a7ac8a3c759c8d8fbb0428cb25bd6eb39064e5b34f25737619955bc086c6",
        url="https://pypi.org/packages/53/81/76495ddf64e89f6a6225107b23478ce3de9a8b2c090b7908bea3be589c43/torchgeo-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="1e4b920d5edfa972e318c3b6cb4c1548e4f70b41b37ddb353a8065cfd661431d",
        url="https://pypi.org/packages/87/2b/ef47cc5067d8a3a776ebb5ff6341dcf11253fa7f6e01a5c449a6b2a30459/torchgeo-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="ed550574a53883b6879bc8af9672f88802021a3093e9cb90ee0449ea78ee6af7",
        url="https://pypi.org/packages/3f/4f/ee48e67796ec455cd7496fd7f37186a02b532b4e62a6200e7cd935ba7d5f/torchgeo-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="80470de172ebc5d602eecf768d391219fda46586a0a86f509b731458a0c69343",
        url="https://pypi.org/packages/ac/42/c8243fb01a6a4236bd68cfbf2a9518fba961a5749fecbbb45dff475b2aa0/torchgeo-0.2.1-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="31562339a20cb2f7ee36c2e8aa789bc960a167df6191a434aad317fc06209178",
        url="https://pypi.org/packages/7c/f0/2c5c94cb49a06a52387a81789fe95239b1771339f5c9f443aa1cd21696a8/torchgeo-0.2.0-py3-none-any.whl",
    )
    version(
        "0.1.1",
        sha256="acbd8e419150344fbecb827571103162a91b01e2b3ce22e52f0792f0d204a1db",
        url="https://pypi.org/packages/a4/6b/dcf09528876dea0649ded3d6de10a26640dc40ed5ec2baa1587d49dc52a3/torchgeo-0.1.1-py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="584b438770793ce266ca58e22f1fd9e42567870a2a57aebb5b7c0f979fbc0f38",
        url="https://pypi.org/packages/fd/53/2afcebd8907debae24c0f05afc9b72fb6b16d79a1f32d539ebb1184236cf/torchgeo-0.1.0-py3-none-any.whl",
    )

    variant("datasets", default=False)
    variant("docs", default=False)
    variant("style", default=False)
    variant("tests", default=False)

    with default_args(type="run"):
        depends_on("python@3.9:", when="@0.5:")
        depends_on("py-black@21.9-beta0:+jupyter", when="@0.5:+style")
        depends_on("py-black@21.9-beta0:23+jupyter", when="@0.4.1:0.4+style")
        depends_on("py-black@21.9-beta0:22+jupyter", when="@0.3:0.4.0+style")
        depends_on("py-black@21:", when="@:0.2+style")
        depends_on("py-einops@0.3:", when="@0.5:")
        depends_on("py-einops@0.3:0.6", when="@0.4")
        depends_on("py-einops@0.3:0.4", when="@0.3")
        depends_on("py-einops", when="@:0.2")
        depends_on("py-fiona@1.8.19:", when="@0.5:")
        depends_on("py-fiona@1.8.0:", when="@0.3:0.4")
        depends_on("py-fiona@1.5:", when="@:0.2")
        depends_on("py-flake8@3.8.0:6", when="@0.4+style")
        depends_on("py-flake8@3.8.0:5", when="@0.3.1:0.3+style")
        depends_on("py-flake8@3.8.0:4", when="@0.3:0.3.0+style")
        depends_on("py-flake8@3.8.0:", when="@:0.2,0.5:+style")
        depends_on("py-h5py@3.0.0:", when="@0.5:+datasets")
        depends_on("py-h5py@2.6:", when="@0.3:0.4+datasets")
        depends_on("py-h5py", when="@:0.2+datasets")
        depends_on("py-ipywidgets@7.0.0:", when="@0.3.1:+docs")
        depends_on("py-ipywidgets@7.0.0:7", when="@0.3:0.3.0+docs")
        depends_on("py-isort@5.8:5+colors", when="@0.3:0.4+style")
        depends_on("py-isort@5.8:+colors", when="@:0.2,0.5:+style")
        depends_on("py-kornia@0.6.9:", when="@0.5:")
        depends_on("py-kornia@0.6.5:0.6", when="@0.4")
        depends_on("py-kornia@0.6.4:0.6", when="@0.3")
        depends_on("py-kornia@0.5.11:", when="@0.2.1:0.2")
        depends_on("py-kornia@0.5.4:", when="@:0.2.0")
        depends_on("py-laspy@2.0.0:", when="@0.2:+datasets")
        depends_on("py-lightly@1.4.4:1.4.25,1.5:", when="@0.5.2:")
        depends_on("py-lightly@1.4.4:", when="@0.5:0.5.1")
        depends_on("py-lightning@2.0.0:+pytorch-extra", when="@0.5:")
        depends_on("py-lightning@1.8.0:1", when="@0.4.1:0.4")
        depends_on("py-matplotlib@3.3.3:", when="@0.5:")
        depends_on("py-matplotlib@3.3.0:", when="@0.3:0.4")
        depends_on("py-matplotlib", when="@:0.2")
        depends_on("py-mypy@0.900:0", when="@0.4:0.4.0+tests")
        depends_on("py-mypy@0.900:0.971", when="@0.3.1:0.3+tests")
        depends_on("py-mypy@0.900:0.961", when="@0.3:0.3.0+tests")
        depends_on("py-mypy@0.900:", when="@:0.2,0.4.1:+tests")
        depends_on("py-nbmake@1.3.3:", when="@0.4.1:+tests")
        depends_on("py-nbmake@0.1:1.1", when="@0.3:0.3.0+tests")
        depends_on("py-nbmake@0.1:", when="@:0.2,0.3.1:0.4.0+tests")
        depends_on("py-nbsphinx@0.8.5:", when="@0.4.1:+docs")
        depends_on("py-nbsphinx@0.8.5:0.8", when="@0.3:0.4.0+docs")
        depends_on("py-numpy@1.19.3:", when="@0.5:")
        depends_on("py-numpy@1.17.2:1", when="@0.3:0.4")
        depends_on("py-numpy", when="@:0.2")
        depends_on("py-omegaconf@2.1.0:2.1.0.0,2.1.1:", when="@0.4.1:0.4+tests")
        depends_on("py-omegaconf@2.1.0:2.1.0.0,2.1.1:", when="@0.1.1:0.4.0")
        depends_on("py-open3d@0.11.2:0.14", when="@0.3+datasets ^python@:3.9")
        depends_on("py-open3d@0.11.2:", when="@0.2+datasets")
        depends_on("py-opencv-python@4.4.0.46:", when="@0.5:+datasets")
        depends_on("py-opencv-python@3.4.2.17:", when="@0.3:0.4+datasets")
        depends_on("py-opencv-python", when="@:0.2+datasets")
        depends_on("py-packaging@17:21", when="@0.3")
        depends_on("py-pandas@1.1.3:", when="@0.5:")
        depends_on("py-pandas@0.23.2:", when="@0.4.1:0.4+datasets")
        depends_on("py-pandas@0.23.2:1", when="@0.3:0.4.0+datasets")
        depends_on("py-pandas@0.19.1:", when="@0.2+datasets")
        depends_on("py-pillow@8:", when="@0.5:")
        depends_on("py-pillow@6.2:9", when="@0.3:0.4")
        depends_on("py-pillow@2.9:", when="@:0.2")
        depends_on("py-pycocotools@2.0.5:", when="@0.5:+datasets")
        depends_on("py-pycocotools", when="@:0.4+datasets")
        depends_on("py-pydocstyle@6.1:+toml", when="+style")
        depends_on("py-pyproj@3.0.0:", when="@0.5:")
        depends_on("py-pyproj@2.2:", when="@:0.4")
        depends_on("py-pytest@7.3:", when="@0.5.1:+tests")
        depends_on("py-pytest@6.2:", when="@0.5:0.5.0+tests")
        depends_on("py-pytest@6.1.2:7", when="@0.3:0.4+tests")
        depends_on("py-pytest@6.0.0:", when="@:0.2+tests")
        depends_on("py-pytest-cov@4:", when="@0.5.1:+tests")
        depends_on("py-pytest-cov@2.4:3", when="@0.3+tests")
        depends_on("py-pytest-cov@2.4:", when="@:0.2,0.4:0.5.0+tests")
        depends_on("py-pytorch-lightning@1.5.1:1+extra", when="@0.4:0.4.0")
        depends_on("py-pytorch-lightning@1.5.1:1", when="@0.3")
        depends_on("py-pytorch-lightning@1.3.0:", when="@:0.2")
        depends_on("py-pytorch-sphinx-theme", when="@0.3:+docs")
        depends_on("py-pyupgrade@2.8:", when="@0.5:+style")
        depends_on("py-pyupgrade@1.24:", when="@0.4+style")
        depends_on("py-pyupgrade@1.24:2", when="@0.3+style")
        depends_on("py-pyvista@0.34.2:", when="@0.5:+datasets")
        depends_on("py-pyvista@:0.38", when="@0.4.1:0.4+datasets")
        depends_on("py-pyvista@:0.37", when="@0.4:0.4.0+datasets")
        depends_on("py-radiant-mlhub@0.3:", when="@0.4.1:+datasets")
        depends_on("py-radiant-mlhub@0.2.1:0.4", when="@0.3.1:0.4.0+datasets")
        depends_on("py-radiant-mlhub@0.2.1:", when="@:0.3.0+datasets")
        depends_on("py-rarfile@4:", when="@0.5:+datasets")
        depends_on("py-rarfile@3:", when="@:0.4+datasets")
        depends_on("py-rasterio@1.2.0:", when="@0.5:")
        depends_on("py-rasterio@1.0.20:", when="@0.3:0.4")
        depends_on("py-rasterio@1.0.16:", when="@:0.2")
        depends_on("py-rtree@1:", when="@0.3:")
        depends_on("py-rtree@0.9.4:", when="@0.2.1:0.2")
        depends_on("py-rtree@0.5:", when="@:0.2.0")
        depends_on("py-scikit-image@0.18.0:", when="@0.5:+datasets")
        depends_on("py-scikit-image@0.18.0:0.20", when="@0.4.1:0.4+datasets")
        depends_on("py-scikit-image@0.18.0:0.19", when="@0.4:0.4.0+datasets")
        depends_on("py-scikit-learn@0.21.0:", when="@0.3:0.4")
        depends_on("py-scikit-learn@0.18:", when="@0.1.1:0.2")
        depends_on("py-scipy@1.6.2:", when="@0.4:+datasets")
        depends_on("py-scipy@1.2.0:", when="@0.3+datasets")
        depends_on("py-scipy@0.9:", when="@:0.2+datasets")
        depends_on("py-segmentation-models-pytorch@0.2", when="@0.3:0.3.0")
        depends_on("py-segmentation-models-pytorch@0.2:", when="@0.1.1:0.2,0.3.1:")
        depends_on("py-shapely@2.0.2:", when="@0.5.2: ^python@3.12:")
        depends_on("py-shapely@1.7.1:", when="@0.5:")
        depends_on("py-shapely@1.3:1", when="@0.3")
        depends_on("py-shapely@1.3:", when="@:0.2,0.4")
        depends_on("py-sphinx@4.0.0:6", when="@0.4:0.4.0+docs")
        depends_on("py-sphinx@4.0.0:5", when="@0.3,0.4.1:+docs")
        depends_on("py-tensorboard@2.9.1:", when="@0.4.1:0.4+tests")
        depends_on("py-timm@0.4.12:", when="@0.5:")
        depends_on("py-timm@0.4.12:0.6", when="@0.4")
        depends_on("py-timm@0.4.12:0.4", when="@0.3")
        depends_on("py-timm@0.2:", when="@0.1.1:0.2")
        depends_on("py-torch@1.12:", when="@0.4.1:")
        depends_on("py-torch@1.12:1", when="@0.4:0.4.0")
        depends_on("py-torch@1.9:1", when="@0.3")
        depends_on("py-torch@1.7:", when="@:0.2")
        depends_on("py-torchmetrics@0.10.0:", when="@0.5:")
        depends_on("py-torchmetrics@0.10.0:0", when="@0.4")
        depends_on("py-torchmetrics@0.7.0:0.9", when="@0.3")
        depends_on("py-torchmetrics@0.7.0:", when="@0.2.1:0.2")
        depends_on("py-torchmetrics", when="@0.1.1:0.2.0")
        depends_on("py-torchvision@0.13:", when="@0.5:")
        depends_on("py-torchvision@0.13:0.15", when="@0.4.1:0.4")
        depends_on("py-torchvision@0.13:0.14", when="@0.4:0.4.0")
        depends_on("py-torchvision@0.10:0.13", when="@0.3")
        depends_on("py-torchvision@0.10:", when="@0.2")
        depends_on("py-torchvision@0.3:", when="@:0.1")
        depends_on("py-zipfile-deflate64@0.2:", when="@0.2.1:+datasets")
