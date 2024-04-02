# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNatsort(PythonPackage):
    """Simple yet flexible natural sorting in Python."""

    homepage = "https://github.com/SethMMorton/natsort"
    url = "https://github.com/SethMMorton/natsort/archive/5.2.0.zip"

    license("MIT")

    version(
        "8.4.0",
        sha256="4732914fb471f56b5cce04d7bae6f164a592c7712e1c85f9ef585e197299521c",
        url="https://pypi.org/packages/ef/82/7a9d0550484a62c6da82858ee9419f3dd1ccc9aa1c26a1e43da3ecd20b0d/natsort-8.4.0-py3-none-any.whl",
    )
    version(
        "8.2.0",
        sha256="04fe18fdd2b9e5957f19f687eb117f102ef8dde6b574764e536e91194bed4f5f",
        url="https://pypi.org/packages/3e/58/61c4b4fd9e597affdcd3347d5991fa5be404af26f19932d3116b67e133da/natsort-8.2.0-py3-none-any.whl",
    )
    version(
        "7.1.1",
        sha256="d0f4fc06ca163fa4a5ef638d9bf111c67f65eedcc7920f98dec08e489045b67e",
        url="https://pypi.org/packages/63/23/8b6acd2e9c0b427802dd45aacf0b2a0250893c3b26c7b1340589a588cc2a/natsort-7.1.1-py3-none-any.whl",
    )
    version(
        "7.1.0",
        sha256="161dfaa30a820a4a274d4eab1f693300990a1be05ae5724af0cc6d3b530fc979",
        url="https://pypi.org/packages/f0/c3/d16e6abfa2aa3ef339fbe0a5ca785f5cf5209b6f5ba5d18e3115e6e64ce5/natsort-7.1.0-py3-none-any.whl",
    )
    version(
        "7.0.1",
        sha256="d3fd728a3ceb7c78a59aa8539692a75e37cbfd9b261d4d702e8016639820f90a",
        url="https://pypi.org/packages/0f/65/81883897f4aaa1e53deaa65137318cfe80b36ce013c2e86f8fd0843cfa02/natsort-7.0.1-py3-none-any.whl",
    )
    version(
        "7.0.0",
        sha256="41c9e0b5fb168d849656b3ea4d455385ec1036451167a9d977f94e63cb07a3d4",
        url="https://pypi.org/packages/e5/d1/3e509d47e393f16ef3b469cae76daf5eca0a4089b13ff41d7c378ba8179f/natsort-7.0.0-py3-none-any.whl",
    )
    version(
        "6.2.1",
        sha256="daae7b2e22ef21305bf6921e49f6ad25d0e29f924e96e3bb447449e11446c726",
        url="https://pypi.org/packages/4a/4e/ead3dd6b7c3b6011c04ed9e526b53a2e2b96f1205fb207f73374cb015810/natsort-6.2.1-py2.py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="4f0de45639f1fa43dede43ae1919bcab66e0a6fc19b68ea24f0a250814b4f176",
        url="https://pypi.org/packages/81/27/db2ee290a962a7c876409c91f12982a699c8956eb9485e4bfb00d1b799b1/natsort-6.2.0-py2.py3-none-any.whl",
    )
    version(
        "6.1.0",
        sha256="4fe33a96eec07e92736c5374db776a2fa489a4116ab4be90d3fc3a95c45d0c8c",
        url="https://pypi.org/packages/3d/e9/b543580583bb84de1a844d5de57fae0b17db7c50e60beedb483cf0e2e7d6/natsort-6.1.0-py2.py3-none-any.whl",
    )
    version(
        "6.0.0",
        sha256="83a8c36b1b2321705d4d7814a7aaf91d0e1bcb7bff119a6ebfe5c9ce3b332d0e",
        url="https://pypi.org/packages/e7/13/a66bfa0ebf00e17778ca0319d081be686a33384d1f612fc8e0fc542ac5d8/natsort-6.0.0-py2.py3-none-any.whl",
    )
    version(
        "5.5.0",
        sha256="e1ad0618d3aa0cc43dfc3298ffcdbfeb47dfff1d875359dc81c72434ae8c62bf",
        url="https://pypi.org/packages/d8/67/9f795649f1173b18851941e288035695386ee44c33bb0960832550f8a236/natsort-5.5.0-py2.py3-none-any.whl",
    )
    version(
        "5.4.1",
        sha256="ea0bbac61fbc2511607f667a3e1adead7e65f75dd59bf8a429298d56c506db34",
        url="https://pypi.org/packages/e3/31/b937f858addee2e1a62f15842f0f3f07e9277aa87fb67fe9b9e28ac90d50/natsort-5.4.1-py2.py3-none-any.whl",
    )
    version(
        "5.2.0",
        sha256="a9156f61336a8d743f67a8c9f336b1287529f67a07fe6001c7d4b5673a42308e",
        url="https://pypi.org/packages/dd/0f/02359ee61e2b7ace625618ad87c336cbfa11b0e7b4f7a3ed9fc7b71cce6e/natsort-5.2.0-py2.py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="ee2f7715bf45a65cc1ab1d80360b00299102c7bf9d87757a27e14ddaafa57d0e",
        url="https://pypi.org/packages/a8/e2/517a124d94855fb68a13c53bb40fdef4b75bc1827215349f7e57b653651f/natsort-5.1.1-py2.py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="64b702ee943144beea9cc58f4b2893da3bc3dfa9bd31cd216f8bfd6dce6edf57",
        url="https://pypi.org/packages/bc/e7/163948f0bd24298d86bdd47d4934bf9fd564716dea73e19690080de985e1/natsort-5.1.0-py2.py3-none-any.whl",
    )
    version(
        "5.0.3",
        sha256="e479b3951cba4e7946086fb416920fd93ae8aa17180e0c31ef671de13a83111f",
        url="https://pypi.org/packages/3b/04/b1df20d65cbe724329fc416ca43f87c5df75b4608fb73b3eb5d974859636/natsort-5.0.3-py2.py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="b6b018412a7f6ccd80c2d892947c93eae9c1c4c6948382dbcc21a69939c5a408",
        url="https://pypi.org/packages/09/6c/1ec71a9cd37d334d7f50c59a9d9de02370bd22b49f59534a136d2080f6da/natsort-5.0.2-py2.py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="ad35be68ef6db20a9b0ae6c81df8ea1c6166f924e92de967b9adca97912acec6",
        url="https://pypi.org/packages/21/47/0a52ba175b01206493f1ad7f09a13c27f33e898739340fb500180c53b43e/natsort-5.0.1-py2.py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="076546e61864d4a095cad453d301db5c8fdd1e5d340a3f92e3eef5caebdb7c8c",
        url="https://pypi.org/packages/98/c8/9fdc4c9122bb0c7da63b28f165d323188597e795d2d52f884c5e0a33bec0/natsort-5.0.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.4",
        sha256="fbb31f9807c6b356a7f127a592bd62445aaac3ae2b41db32cc2b7a52f4684ff5",
        url="https://pypi.org/packages/8e/63/92a8efe593e991da44afbd9a3e50c719aa4cede001cdcd39ae162a9720a6/natsort-4.0.4-py2.py3-none-any.whl",
    )
    version(
        "4.0.3",
        sha256="025a002e74af7b25af22d03c21427cf4911e404a1b6ef65c52a73f9fa1e51007",
        url="https://pypi.org/packages/53/de/32729d48426eb7196e0f066e11d8f4f739dea6a64d175d286acea3980d37/natsort-4.0.3-py2.py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="fd18f797cecc0267c24fcaa9c06b386abf54452d0f20b88f312c9591b5a76443",
        url="https://pypi.org/packages/c5/69/c2e5d9f982f5564cb4f99ae25fff486c62819fecc7226efdb88642e2c7a7/natsort-4.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@8.3:")
