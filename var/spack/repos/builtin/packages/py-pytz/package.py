# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytz(PythonPackage):
    """World timezone definitions, modern and historical."""

    homepage = "https://pythonhosted.org/pytz"
    pypi = "pytz/pytz-2019.3.tar.gz"
    git = "https://github.com/stub42/pytz.git"

    license("MIT")

    version(
        "2023.3",
        sha256="a151b3abb88eda1d4e34a9814df37de2a80e301e68ba0fd856fb9b46bfbbbffb",
        url="https://pypi.org/packages/7f/99/ad6bd37e748257dd70d6f85d916cafe79c0b0f5e2e95b11f7fbc82bf3110/pytz-2023.3-py2.py3-none-any.whl",
    )
    version(
        "2022.2.1",
        sha256="220f481bdafa09c3955dfbdddb7b57780e9a94f5127e35456a48589b9e0c0197",
        url="https://pypi.org/packages/d5/50/54451e88e3da4616286029a3a17fc377de817f66a0f50e1faaee90161724/pytz-2022.2.1-py2.py3-none-any.whl",
    )
    version(
        "2021.3",
        sha256="3672058bc3453457b622aab7a1c3bfd5ab0bdae451512f6cf25f64ed37f5b87c",
        url="https://pypi.org/packages/d3/e3/d9f046b5d1c94a3aeab15f1f867aa414f8ee9d196fae6865f1d6a0ee1a0b/pytz-2021.3-py2.py3-none-any.whl",
    )
    version(
        "2021.1",
        sha256="eb10ce3e7736052ed3623d49975ce333bcd712c7bb19a58b9e2089d4057d0798",
        url="https://pypi.org/packages/70/94/784178ca5dd892a98f113cdd923372024dc04b8d40abe77ca76b5fb90ca6/pytz-2021.1-py2.py3-none-any.whl",
    )
    version(
        "2020.1",
        sha256="a494d53b6d39c3c6e44c3bec237336e14305e4f29bbf800b599253057fbb79ed",
        url="https://pypi.org/packages/4f/a4/879454d49688e2fad93e59d7d4efda580b783c745fd2ec2a3adf87b0808d/pytz-2020.1-py2.py3-none-any.whl",
    )
    version(
        "2019.3",
        sha256="1c557d7d0e871de1f5ccd5833f60fb2550652da6be2693c1e02300743d21500d",
        url="https://pypi.org/packages/e7/f9/f0b53f88060247251bf481fa6ea62cd0d25bf1b11a87888e53ce5b7c8ad2/pytz-2019.3-py2.py3-none-any.whl",
    )
    version(
        "2019.1",
        sha256="303879e36b721603cc54604edcac9d20401bdbe31e1e4fdee5b9f98d5d31dfda",
        url="https://pypi.org/packages/3d/73/fe30c2daaaa0713420d0382b16fbb761409f532c56bdcc514bf7b6262bb6/pytz-2019.1-py2.py3-none-any.whl",
    )
    version(
        "2018.4",
        sha256="65ae0c8101309c45772196b21b74c46b2e5d11b6275c45d251b150d5da334555",
        url="https://pypi.org/packages/dc/83/15f7833b70d3e067ca91467ca245bae0f6fe56ddc7451aa0dc5606b120f2/pytz-2018.4-py2.py3-none-any.whl",
    )
    version(
        "2016.10",
        sha256="a1ea35e87a63c7825846d5b5c81d23d668e8a102d3b1b465ce95afe1b3a2e065",
        url="https://pypi.org/packages/f5/fa/4a9aefc206aa49a4b5e0a72f013df1f471b4714cdbe6d78f0134feeeecdb/pytz-2016.10-py2.py3-none-any.whl",
    )
    version(
        "2016.6.1",
        sha256="7833bf559800232d3965b70e69642ebdadc76f7988f8d0a1440e072193ecd949",
        url="https://pypi.org/packages/ba/c7/3d54cad4fb6cf7bf375d39771e67680ec779a541c68459210fcfdc3ba952/pytz-2016.6.1-py2.py3-none-any.whl",
    )
    version(
        "2016.3",
        sha256="2e4859a1c1b5c77bdc247013332ae1edbd5b3a7fb3737e33c5f26efcf5e150fb",
        url="https://pypi.org/packages/e2/87/e774b15dd6468889e5268ebbc00040c9f9da546c462099c4d43e14697e04/pytz-2016.3-py2.py3-none-any.whl",
    )
    version(
        "2015.4",
        sha256="4d64ed1b9e0e73095f5cfa87f0e97ddb4c840049e8efeb7e63b46118ba1d623a",
        url="https://pypi.org/packages/2d/cb/c9b0c9e4cf54bc3517b2d52904c9f328be2e88cf07392fea51ee0c3c4b28/pytz-2015.4-py2.py3-none-any.whl",
    )
    version(
        "2014.10",
        sha256="5438d749e923c914741fe2a410b528abe27053000fbf878bc437428d08ae0ab1",
        url="https://pypi.org/packages/c5/bc/995a7472f9ca49980ce07ca7a68b0b7c01bc87fc7f9f09707cbfde282a8f/pytz-2014.10-py2.py3-none-any.whl",
    )
    version(
        "2014.9",
        sha256="431c78bcf827c92a19d7829cd9ae7902d52d6dfcb23d98904fc807ddea1ec076",
        url="https://pypi.org/packages/2a/de/7c55dffb7464509aee814047f50490886925226846bcb8c622677619f15e/pytz-2014.9-py2.py3-none-any.whl",
    )
