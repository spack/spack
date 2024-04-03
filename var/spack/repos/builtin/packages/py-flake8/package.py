# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    pypi = "flake8/flake8-4.0.1.tar.gz"

    license("MIT")

    version(
        "6.1.0",
        sha256="ffdfce58ea94c6580c77888a86506937f9a1a227dfcd15f245d694ae20a6b6e5",
        url="https://pypi.org/packages/b0/24/bbf7175ffc47cb3d3e1eb523ddb23272968359dfcf2e1294707a2bf12fc4/flake8-6.1.0-py2.py3-none-any.whl",
    )
    version(
        "6.0.0",
        sha256="3833794e27ff64ea4e9cf5d410082a8b97ff1a06c16aa3d2027339cd0f1195c7",
        url="https://pypi.org/packages/d9/6a/bb0122ebe280476c924470779d2595f1403878cafe3c8a343ac56a5a9c0e/flake8-6.0.0-py2.py3-none-any.whl",
    )
    version(
        "5.0.4",
        sha256="7a1cf6b73744f5806ab95e526f6f0d8c01c66d7bbe349562d22dfca20610b248",
        url="https://pypi.org/packages/cf/a0/b881b63a17a59d9d07f5c0cc91a29182c8e8a9aa2bde5b3b2b16519c02f4/flake8-5.0.4-py2.py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="a7926e0b6d23c0991245b60279e774d2596dfecd9b158525d1f8c050a61eae5a",
        url="https://pypi.org/packages/6b/c0/b468ca1fb44acb7c054008e6edc0171e4209dd527bdb4f5836667102f36d/flake8-5.0.2-py2.py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="44e3ecd719bba1cb2ae65d1b54212cc9df4f5db15ac271f8856e5e6c2eebefed",
        url="https://pypi.org/packages/4f/24/5396113ca4621c0bcc924a2e9ceb7bf03e141ebbfcc89c724284f55225c7/flake8-5.0.1-py2.py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="f44e470195849d0596cb488c7bd769086fcbe987c10cc9daae9a13b4136abb24",
        url="https://pypi.org/packages/ad/b5/27d1c9553cfd5282e5f94fe0306b231890d42d86506fb7f623bc638e741e/flake8-5.0.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="479b1304f72536a55948cb40a32dce8bb0ffe3501e26eaf292c7e60eb5e0428d",
        url="https://pypi.org/packages/34/39/cde2c8a227abb4f9ce62fe55586b920f438f1d2903a1a22514d0b982c333/flake8-4.0.1-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="124554bfd067e04d891258c0208a764b512ca3a94c8a3c06bea56af539dd74db",
        url="https://pypi.org/packages/0f/cc/931e8fd88a7730d66ee3b962f954eef1efc9959d618d01574cebf6905dae/flake8-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "3.9.2",
        sha256="bf8fd333346d844f616e8d47905ef3a3384edae6b4e9beb0c5101e25e3110907",
        url="https://pypi.org/packages/fc/80/35a0716e5d5101e643404dabd20f07f5528a21f3ef4032d31a49c913237b/flake8-3.9.2-py2.py3-none-any.whl",
    )
    version(
        "3.8.2",
        sha256="ccaa799ef9893cebe69fdfefed76865aeaefbb94cb8545617b2298786a4de9a5",
        url="https://pypi.org/packages/ea/35/dcf9a3393305bfc61854b764b5aeb79a72493e77991eead133c189d7868e/flake8-3.8.2-py2.py3-none-any.whl",
    )
    version(
        "3.7.8",
        sha256="8e9dfa3cecb2400b3738a42c54c3043e821682b9c840b0448c0503f781130696",
        url="https://pypi.org/packages/26/de/3f815a99d86eb10464ea7bd6059c0172c7ca97d4bdcfca41051b388a653b/flake8-3.7.8-py2.py3-none-any.whl",
    )
    version(
        "3.7.7",
        sha256="a796a115208f5c03b18f332f7c11729812c8c3ded6c46319c59b53efd3819da8",
        url="https://pypi.org/packages/e9/76/b915bd28976068a9843bf836b789794aa4a8eb13338b23581005cd9177c0/flake8-3.7.7-py2.py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="c7841163e2b576d435799169b78703ad6ac1bbb0f199994fc05f700b2a90ea37",
        url="https://pypi.org/packages/b9/dc/14e9d94c770b8c4ef584e906c7583e74864786a58d47de101f2767d50c0b/flake8-3.5.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.4",
        sha256="603a3ae7c8030219fee084728ca02a8bbd3a51829cacf97b445172a46cb04662",
        url="https://pypi.org/packages/70/fd/93266c6af1a23ea4d8b9a557b1fa02e6bdb43702b817c9151da5a3af3aa7/flake8-3.0.4-py2.py3-none-any.whl",
    )
    version(
        "2.6.2",
        sha256="7ac3bbaac27174d95bc4734ed23a07de567ffbcf4fc7e316854b4f3015d4fd15",
        url="https://pypi.org/packages/70/a9/9b66f22d038de51e05f92d5e677fd89d8f9c980db0b8a130621baad052f5/flake8-2.6.2-py2.py3-none-any.whl",
    )
    version(
        "2.5.4",
        sha256="fb5a67af4024622287a76abf6b7fe4fb3cfacf765a790976ce64f52c44c88e4a",
        url="https://pypi.org/packages/e1/16/fba9e558dd7215b9a54abfc65a7032c5239c983cbb4f9eac9abf0e8f399b/flake8-2.5.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@6:")
        depends_on("py-entrypoints@0.3", when="@3.7")
        depends_on("py-importlib-metadata@1.1:4.2", when="@5.0.4:5 ^python@:3.7")
        depends_on("py-importlib-metadata@:4.2", when="@4:5.0.3 ^python@:3.7")
        depends_on("py-importlib-metadata", when="@3.8:3 ^python@:3.7")
        depends_on("py-mccabe@0.7:", when="@5:")
        depends_on("py-mccabe@0.6", when="@3.3:4")
        depends_on("py-mccabe@0.5", when="@3:3.2")
        depends_on("py-mccabe@0.2.1:0.5", when="@2.6:2")
        depends_on("py-mccabe@0.2.1:0.4", when="@2.5.2:2.5")
        depends_on("py-pep8@1.5.7:1.5,1.7:", when="@2.4.1:2.5")
        depends_on("py-pycodestyle@2.11:", when="@6.1:")
        depends_on("py-pycodestyle@2.10", when="@6:6.0")
        depends_on("py-pycodestyle@2.9", when="@5")
        depends_on("py-pycodestyle@2.8", when="@4")
        depends_on("py-pycodestyle@2.7", when="@3.9:3")
        depends_on("py-pycodestyle@2.6", when="@3.8")
        depends_on("py-pycodestyle@2.5", when="@3.7")
        depends_on("py-pycodestyle@2.0.0:2.3", when="@3.3:3.3.0.0,3.4:3.5")
        depends_on("py-pycodestyle@2.0.0:2.0", when="@2.6:3.1.0")
        depends_on("py-pyflakes@3.1", when="@6.1:6")
        depends_on("py-pyflakes@3:3.0", when="@6:6.0")
        depends_on("py-pyflakes@2.5:2", when="@5")
        depends_on("py-pyflakes@2.4", when="@4")
        depends_on("py-pyflakes@2.3", when="@3.9:3")
        depends_on("py-pyflakes@2.2", when="@3.8")
        depends_on("py-pyflakes@2.1", when="@3.7")
        depends_on("py-pyflakes@1.5:1", when="@3.5")
        depends_on("py-pyflakes@0.8.1:1.1,1.2.3:1.2", when="@2.6:3.1.0")
        depends_on("py-pyflakes@0.8.1:1.0", when="@2.5")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.

    # Flake8 uses ranges for its dependencies to enforce a stable list of
    # error codes within each minor release:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    # http://flake8.pycqa.org/en/latest/internal/releases.html#releasing-flake8

    # Flake8 6.1.X

    # Flake8 6.0.X

    # Flake8 5.0.X

    # Flake8 4.0.X

    # Flake8 3.9.X

    # Flake8 3.8.X

    # Flake8 3.7.X

    # Flake8 3.5.X

    # Flake8 3.0.X

    # Flake8 2.5.X

    # Python version-specific backports
