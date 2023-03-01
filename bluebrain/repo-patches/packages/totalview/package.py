import os

from spack.package import *
from spack.pkg.builtin.totalview import Totalview as BuiltinTotalview


class Totalview(BuiltinTotalview):
    __doc__ = BuiltinTotalview.__doc__

    # new totalview docs suggest this license path
    license_files = ["toolworks/FNP_license/license.dat"]

    version("2022.2.13", sha256="4bf625c760454e532fe66666f2f5479d38f36f569f104bbe3341c0f48cbc8766")

    version("2021.1.16", sha256="4c51c7b6ab6b6afa7635ba2e9fc3b0ef833806f775a0ad0da26b13d6320625dd")

    version("2021.4.10", sha256="c476288ebe1964e0803c7316975c71a957e52f45187b135bc1dc3b65491bb61d")

    resource(
        name="x86_64",
        url="file://{0}/totalview_2022.2.13_linux_x86-64.tar".format(os.getcwd()),
        destination=".",
        sha256="aebd11b837ce18b8200859ea762caa56e2cea346daa114f2841aa0f05a422309",
        when="@2022.2.13 target=x86_64:",
    )

    resource(
        name="x86_64",
        url="file://{0}/totalview_2020.3.11_linux_x86-64.tar".format(os.getcwd()),
        destination=".",
        sha256="129e991d3ce4df9f9f04adbf79b62d3c2706d7732ec305f3d3c97a6b4d1f5a13",
        when="@2021.1.16 target=x86_64:",
    )

    resource(
        name="x86_64",
        url="file://{0}/totalview_2021.4.10_linux_x86-64.tar".format(os.getcwd()),
        destination=".",
        sha256="7e5509b2cfb219100b0032304bdad7d422657c0736c386ba64bdb1bf11d10a1d",
        when="@2021.4.10 target=x86_64:",
    )
