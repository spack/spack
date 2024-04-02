# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    pypi = "notebook/notebook-6.1.4.tar.gz"

    version(
        "6.5.4",
        sha256="dd17e78aefe64c768737b32bf171c1c766666a21cc79a44d37a1700771cab56f",
        url="https://pypi.org/packages/7a/21/0e7683e7c4d51b8f6cc5df9bbd33fb2d1e114b9e5dcddeef96ebd8e86348/notebook-6.5.4-py3-none-any.whl",
    )
    version(
        "6.4.12",
        sha256="8c07a3bb7640e371f8a609bdbb2366a1976c6a2589da8ef917f761a61e3ad8b1",
        url="https://pypi.org/packages/b5/62/229659241aee54be38990e06e684bcfe5c9c8727185f5e39335be8821583/notebook-6.4.12-py3-none-any.whl",
    )
    version(
        "6.4.11",
        sha256="b4a6baf2eba21ce67a0ca11a793d1781b06b8078f34d06c710742e55f3eee505",
        url="https://pypi.org/packages/03/94/b105adc1b0d65608ce5b670a6aec7ed3c33f726cdfa7a61626bf6f80fead/notebook-6.4.11-py3-none-any.whl",
    )
    version(
        "6.4.5",
        sha256="f7b4362698fed34f44038de0517b2e5136c1e7c379797198c1736121d3d597bd",
        url="https://pypi.org/packages/ea/cf/f4d1089d6803ca2abda5983b7ea5c5567072e92115e91acb543b322ea896/notebook-6.4.5-py3-none-any.whl",
    )
    version(
        "6.1.4",
        sha256="07b6e8b8a61aa2f780fe9a97430470485bc71262bc5cae8521f1441b910d2c88",
        url="https://pypi.org/packages/cc/00/0db4005f8410c0c6c598d6beecd650846e00955a3bf800ea09872a9009f1/notebook-6.1.4-py3-none-any.whl",
    )
    version(
        "6.0.3",
        sha256="3edc616c684214292994a3af05eaea4cc043f6b4247d830f3a2f209fa7639a80",
        url="https://pypi.org/packages/b1/f1/0a67f09ef53a342403ffa66646ee39273e0ac79ffa5de5dbe2f3e28b5bdf/notebook-6.0.3-py3-none-any.whl",
    )
    version(
        "6.0.1",
        sha256="b0a290f5cc7792d50a21bec62b3c221dd820bf00efa916ce9aeec4b5354bde20",
        url="https://pypi.org/packages/f3/a1/1e07cedcb554408fefe4a7d32b2a041c86517167aec6ca8251c808ef6c1e/notebook-6.0.1-py3-none-any.whl",
    )
    version(
        "6.0.0",
        sha256="0be97e939cec73cde37fc4d2a606a6f497a9addf3afcf61a09a21b0c35e699c5",
        url="https://pypi.org/packages/4e/b6/a6189ca7146482d93c912dbe6c65db0f264c1c88f707feea3683caa6c1f8/notebook-6.0.0-py3-none-any.whl",
    )
    version(
        "5.7.8",
        sha256="f64fa6624d2323fbef6210a621817d6505a45d0d4a9367f1843b20a38a4666ee",
        url="https://pypi.org/packages/f6/36/89ebfffc9dd8c8dbd81c1ffb53e3d4233ee666414c143959477cb07cc5f5/notebook-5.7.8-py2.py3-none-any.whl",
    )
    version(
        "5.7.6",
        sha256="cc027a62be0f7756e0ef3d2d98458c4d7f4b3566449fb1a05891207f5bd9a1bf",
        url="https://pypi.org/packages/0a/d8/4e9521354ed3d730ba6d8a5af440b66c73245ef46be706e51bead71afc21/notebook-5.7.6-py2.py3-none-any.whl",
    )
    version(
        "5.7.5",
        sha256="9ca7f597ce4f5a24611c589fa320a7af2861f0ca1dc20839129c91ae354453fe",
        url="https://pypi.org/packages/76/e8/50bb66c9ea6d21be89b920fac57dca49c4a5749c5b92b4a48458dd42e659/notebook-5.7.5-py2.py3-none-any.whl",
    )
    version(
        "5.7.4",
        sha256="3ab2db8bc10e6edbd264c3c4b800bee276c99818386ee0c146d98d7e6bcf0a67",
        url="https://pypi.org/packages/f8/a6/dbdf0954d073ab2cf5421cad20334d1e4c780da37205c04522c045298f67/notebook-5.7.4-py2.py3-none-any.whl",
    )
    version(
        "5.7.3",
        sha256="8d7aa1e06fea49d4600afd751c929e9bc7339be92d80fe5e56006ddb1d3bf73b",
        url="https://pypi.org/packages/e7/19/88ab057c8de977873cb30e337204a476b3ca4315d0788c89b91c40ec83dc/notebook-5.7.3-py2.py3-none-any.whl",
    )
    version(
        "5.7.2",
        sha256="661341909008d1e7bfa1541904006f9789fa3de1cbec8379d2879819454cc04b",
        url="https://pypi.org/packages/a2/5d/d1907cd32ac00b5ead56f6e61d9794fa60ef105a22ac5da6e7556011580f/notebook-5.7.2-py2.py3-none-any.whl",
    )
    version(
        "5.7.1",
        sha256="5cff23bf1b6385ede54f130f64ec58b9147a454f43d06d173817e0263005ce18",
        url="https://pypi.org/packages/e1/d9/6d40b38c141dff656ba8b13684c20a97064ba868344da4aa8e94519b12ca/notebook-5.7.1-py2.py3-none-any.whl",
    )
    version(
        "5.7.0",
        sha256="ddb713d15a3205d7d3beab11f7fa9e3b10dbe0a2fff034a7db22ec8a2bc47a8b",
        url="https://pypi.org/packages/44/16/9f108b675828c4117cfe72d8d0f97094163c40584e40c46ec48a1e862693/notebook-5.7.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.3",
        sha256="4ffa49336297898ff8ec35c07eb08ea6b9abfe5afdf3bcb4dccf2a3ee6a69069",
        url="https://pypi.org/packages/09/71/db00a2afe157238a6046659d297b1c5e0b296e6916db3278509c71d6b3bd/notebook-4.2.3-py2.py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="c2a1d43083dd914635091c77249d0b2885b4e0cf311df4a014640a93212ce114",
        url="https://pypi.org/packages/68/e6/ac3b127b36aaf50dfff651f33897b88cf80f3d66f2817294c12bd7da33a5/notebook-4.2.2-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="0d11cda9ce8ef9de189061054b095f1a20bc471c39534e6bb688153734f180f3",
        url="https://pypi.org/packages/ce/24/d0dd761aaddc2efd7a94b00f0e8d9c33660fed5f6f25553d9190a4ccb734/notebook-4.2.1-py2.py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="23b0ccf12b7992b5328085d6a855dd944c9858efdbdea1e732dab5d77811eb69",
        url="https://pypi.org/packages/7f/d8/57a1e73cb8f81322e0b46c53c44d0eaa9202b722744ab741f112ba4835f9/notebook-4.2.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="6b2828548b19c8f1bc9eeb91139d427053633363f1a6538d09a19eb24ca0fd94",
        url="https://pypi.org/packages/d4/08/0a91620361e99d1acd4540b0a3340ba669b06546dbfe56852c905ebe782d/notebook-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.6",
        sha256="afd51c2bb108a90cac63fa2011de112786b1d3485b3fa71a3cd95a39434597df",
        url="https://pypi.org/packages/af/af/87fbc159182390c35d5c04faaf30c10e3f972bcc0567ea0a99cf1eaf2c9f/notebook-4.0.6-py2.py3-none-any.whl",
    )
    version(
        "4.0.4",
        sha256="6e93d83a73ceec2d667ce4e1074be05b738d39012ae91fd9f53236fd47d9012f",
        url="https://pypi.org/packages/28/c0/ef3f8be98623e3632e324b100e3251cc2ed84aece818a26a3a9aa7c18391/notebook-4.0.4-py2.py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="e1a332b61b54153a640a4c040cd9afc19774c7fe7598f3014da04822622616ab",
        url="https://pypi.org/packages/eb/a6/16383171822e1bbda76e4871ea28340a1dff468e205f04ccbe7303bd19e4/notebook-4.0.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@6.4.11:7.0.0-alpha11")
        depends_on("py-argon2-cffi", when="@6.1.0:6")
        depends_on("py-ipykernel", when="@4.1:6")
        depends_on("py-ipython-genutils", when="@4.1:6")
        depends_on("py-jinja2", when="@4.1:5.7.13,6")
        depends_on("py-jupyter-client@5.3.4:", when="@6.0.2:6.5.4")
        depends_on("py-jupyter-client@5.3.1:", when="@6.0.0:6.0.1")
        depends_on("py-jupyter-client@5.2:", when="@5.3:5.7.13,6:6.0.0-rc1")
        depends_on("py-jupyter-client", when="@4.1:5.2")
        depends_on("py-jupyter-core@4.6.1:", when="@6.0.3:6")
        depends_on("py-jupyter-core@4.4:", when="@5.3:6.0.1")
        depends_on("py-jupyter-core", when="@4.1:5.2")
        depends_on("py-nbclassic@0.4.7:", when="@6.5.2:6")
        depends_on("py-nbconvert@5.0.0:", when="@6.4.9:6")
        depends_on("py-nbconvert", when="@4.1:5.7.8,6:6.4.8")
        depends_on("py-nbformat", when="@4.1:6")
        depends_on("py-nest-asyncio@1.5:", when="@6.4.6:6")
        depends_on("py-prometheus-client", when="@5.6:6")
        depends_on("py-pyzmq@17.0.0:", when="@5.5:6.5.4")
        depends_on("py-send2trash@1.8:", when="@6.4.6:6")
        depends_on("py-send2trash@1.5:", when="@6.2:6.4.5")
        depends_on("py-send2trash", when="@5.3:6.1")
        depends_on("py-terminado@0.8.3:", when="@6.1:6")
        depends_on("py-terminado@0.8.1:", when="@5.3:6.0")
        depends_on("py-terminado@0.3.3:", when="@4.1:5.2 platform=linux")
        depends_on("py-terminado@0.3.3:", when="@4.1:5.2 platform=freebsd")
        depends_on("py-terminado@0.3.3:", when="@4.1:5.2 platform=darwin")
        depends_on("py-terminado@0.3.3:", when="@4.1:5.2 platform=cray")
        depends_on("py-tornado@6.1:", when="@6.2:7.0.0-alpha11")
        depends_on("py-tornado@5.0:", when="@6:6.1")
        depends_on("py-tornado@4.1:", when="@5.7.5:5")
        depends_on("py-tornado@4:", when="@4.1:5.7.4")
        depends_on("py-traitlets@4.2.1:", when="@5:6")
        depends_on("py-traitlets", when="@4.1:4")

    # https://github.com/jupyter/notebook/pull/6286
