# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoto3(PythonPackage):
    """The AWS SDK for Python."""

    homepage = "https://github.com/boto/boto3"
    pypi = "boto3/boto3-1.10.44.tar.gz"

    version(
        "1.34.44",
        sha256="40f89fb2acee0a0879effe81badffcd801a348e715483227223241ae311c48fc",
        url="https://pypi.org/packages/15/1e/cbec55e05c0577429945d785cce8e16eebf2a8bd9c5ccda2b9c6e2a51ab4/boto3-1.34.44-py3-none-any.whl",
    )
    version(
        "1.26.26",
        sha256="b1d2521bd2239c4d2d8ee2a79d932bc64bf4779521ecc60c1074ae8a5d88adaa",
        url="https://pypi.org/packages/dc/cb/11560a590526f6049389bdfb5a993c4abc11eb20c12448d922909ac641fb/boto3-1.26.26-py3-none-any.whl",
    )
    version(
        "1.25.5",
        sha256="17ce7b6b702f9e844a33ce3ce9612f09d9d73eb7d34aaeffc77353ec036a9615",
        url="https://pypi.org/packages/29/17/8dd2d2c231cdfed1b24e31e49c628b8490c2846fe3116ced9d2fa73de0aa/boto3-1.25.5-py3-none-any.whl",
    )
    version(
        "1.24.96",
        sha256="748c055214c629744c34c7f94bfa888733dfac0b92e1daef9c243e1391ea4f53",
        url="https://pypi.org/packages/e2/53/e9c9f18f97f1565d9194c0ebbfb8bd9bd4bbb93a54569d2e7af256980511/boto3-1.24.96-py3-none-any.whl",
    )
    version(
        "1.23.10",
        sha256="40d08614f17a69075e175c02c5d5aab69a6153fd50e40fa7057b913ac7bf40e7",
        url="https://pypi.org/packages/75/ca/d917b244919f1ebf96f7bbd5a00e4641f7e9191b0d070258f5dc10f5eaad/boto3-1.23.10-py3-none-any.whl",
    )
    version(
        "1.22.13",
        sha256="240931d41341f30d3cc0bba72ede4dbfe9704721bf13ca19bcd31a435c235f8d",
        url="https://pypi.org/packages/e6/9a/0ea77f98a6018ae5a4fcb7fe74dd9369060dbedf2984612249007f08a834/boto3-1.22.13-py3-none-any.whl",
    )
    version(
        "1.21.46",
        sha256="3b13d727854aba9dea900b6c7fa134c52396869d842460d14fab8b85b69645f7",
        url="https://pypi.org/packages/f0/58/911753da74405a538cd81f2f51521a9c8ec0d927d0cfecdf9f58b7363e02/boto3-1.21.46-py3-none-any.whl",
    )
    version(
        "1.20.54",
        sha256="1a272a1dd36414b1626a47bb580425203be0b5a34caa117f38a5e18adf21f918",
        url="https://pypi.org/packages/f7/d7/7ccb6daf350f9b81550e3f2e25ba24672ea45975ee08f0cbca0a573417c0/boto3-1.20.54-py3-none-any.whl",
    )
    version(
        "1.19.12",
        sha256="b9105554477978e80fda1103ff21ecf07502080667730e45383e1d3951c87954",
        url="https://pypi.org/packages/5e/e1/156846b09fca21b9b164c54200011e3bd17f29187cbfc6903a8e0281a304/boto3-1.19.12-py3-none-any.whl",
    )
    version(
        "1.18.65",
        sha256="bbbc3a71949af31c33101ee0daf4db9b11148d67a4e574b6c66cbe35d985b5af",
        url="https://pypi.org/packages/73/42/9f0173f83f8c2717ce102cf98e5668a1858a21eadd28a235e9b3b0824fa4/boto3-1.18.65-py3-none-any.whl",
    )
    version(
        "1.18.12",
        sha256="e5abbb2b5ebe5ad1157a3af8f28c5c944e9c6eff0dd3e778008894e018bc7e09",
        url="https://pypi.org/packages/9d/28/cdb684f0afb4ab3880b5da31ee18aac3990c57ae81bf1345aab8f1afacec/boto3-1.18.12-py3-none-any.whl",
    )
    version(
        "1.17.112",
        sha256="8716465313c50ad9e5c2ac1767642ca0ddf7d1729c3d5c884d82880c1a15a310",
        url="https://pypi.org/packages/5a/fd/d814f9cbefebbea88977628d11b860b5d564ba6f16f64c378e2da2a36405/boto3-1.17.112-py2.py3-none-any.whl",
    )
    version(
        "1.17.27",
        sha256="6758751f1181b9363e4e7559dcbd5ac0fc7147b73f429c976ec5ecd1688c9ec7",
        url="https://pypi.org/packages/7b/3c/92634ca0da72db047a4957bdd3984d72fbcc82fb9dcda04ea628c9a87dba/boto3-1.17.27-py2.py3-none-any.whl",
    )
    version(
        "1.10.50",
        sha256="aa58c8de6aed36211e0897598de2a3d89122ad8cd1450165679720180ab880ef",
        url="https://pypi.org/packages/43/a6/433564e7b241ecb012c67e6580e302ecdc79c8b5189e3f7efb6e7b0fde45/boto3-1.10.50-py2.py3-none-any.whl",
    )
    version(
        "1.10.44",
        sha256="3728506de1be9a3fe0ddc7849abf5d47f768eca68a958303739ad040b5d5f92d",
        url="https://pypi.org/packages/b5/27/d2fce3e49c992b180e7340dd41ed1f098f2b0370f4a0e17d36a76b32a23a/boto3-1.10.44-py2.py3-none-any.whl",
    )
    version(
        "1.10.38",
        sha256="d64ec82b5125d8f8cae00f92d33a338c6c55cb5984967cfc7f4c52cf138126c4",
        url="https://pypi.org/packages/2e/b4/e8fb59efd68d4889528cb0d4227484b5aa511b765d81e05d2cd7d9bb3ca5/boto3-1.10.38-py2.py3-none-any.whl",
    )
    version(
        "1.9.253",
        sha256="839285fbd6f3ab16170af449ae9e33d0eccf97ca22de17d9ff68b8da2310ea06",
        url="https://pypi.org/packages/f6/fa/6397049020b312f71c397fff8d10247c2e49da760e2807af7d21e3c23695/boto3-1.9.253-py2.py3-none-any.whl",
    )
    version(
        "1.9.169",
        sha256="58ae308e4539264754e4e2a21bfec71b2fbffe02e86a77e680077e10b7c0ed54",
        url="https://pypi.org/packages/a6/1f/b272ead5ccc5370717f3c65ebd5092feab90e748db041bd96c565e7d1a72/boto3-1.9.169-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.34:")
        depends_on("python@3.7:", when="@1.24:1.33")
        depends_on("py-botocore@1.34.44:", when="@1.34.44")
        depends_on("py-botocore@1.29.26:1.29", when="@1.26.26")
        depends_on("py-botocore@1.28.5:1.28", when="@1.25.5:1.25")
        depends_on("py-botocore@1.27.96:1.27", when="@1.24.96:1.24")
        depends_on("py-botocore@1.26.10:1.26", when="@1.23.10:1.23")
        depends_on("py-botocore@1.25.13:1.25", when="@1.22.13:1.22")
        depends_on("py-botocore@1.24.46:1.24", when="@1.21.46:1.21")
        depends_on("py-botocore@1.23.54:1.23", when="@1.20.54:1.20")
        depends_on("py-botocore@1.22.12:1.22", when="@1.19.12:1.19")
        depends_on("py-botocore@1.21.65:1.21", when="@1.18.65:1.18")
        depends_on("py-botocore@1.21.12:1.21", when="@1.18.12")
        depends_on("py-botocore@1.20.112:1.20", when="@1.17.112:1.17")
        depends_on("py-botocore@1.20.27:1.20", when="@1.17.27")
        depends_on("py-jmespath@0.7.1:", when="@1.21.21:")
        depends_on("py-jmespath@0.7.1:0", when="@1.14.25:1.21.20")
        depends_on("py-s3transfer@0.10:", when="@1.34.6:")
        depends_on("py-s3transfer@0.6", when="@1.24:1.28.54")
        depends_on("py-s3transfer@0.5", when="@1.18:1.23")
        depends_on("py-s3transfer@0.4", when="@1.17.54:1.17")
        depends_on("py-s3transfer@0.3", when="@1.14.25:1.17.53")
