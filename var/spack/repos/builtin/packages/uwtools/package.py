# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install uwtools-2-5-1-py-0
#
# You can edit this file again by typing:
#
#     spack edit uwtools-2-5-1-py-0
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *

class UwTools(PythonPackage):
    """UW Tools is a modern, open-source Python package that helps
    automate common tasks needed for many standard numerical weather
    prediction (NWP) workflows. It also provides drivers to automate
    the configuration and execution of Unified Forecast System (UFS)
    components, providing flexibility, interoperability, and
    usability to various UFS Applications."""

    homepage = "https://uwtools.readthedocs.io/en/stable/"
    url = "https://anaconda.org/ufs-community/uwtools/2.5.1/download/noarch/uwtools-2.5.1-py_0.tar.bz2"
    git = "https://github.com/ufs-community/uwtools.git"

    maintainers(
            "NaureenBharwaniNOAA",
            "christinaholtNOAA",
            "elcarpenterNOAA",
            "maddenp-noaa"
    )

    version("develop", branch="develop", submodules=False)
    version(
            "2.5.1",
            tag="2.5.1"
            commit="319c4a45b5f8a9fb9bbddf6050bc7033bff89007"
            submodules=False,
    )

    depends_on("py-pip")
    depends_on("python@3.9")
    depends_on("py-setuptools")
    depends_on("py-f90nml@1.4")
    depends_on("py-jinja2@3.1")
    depends_on("iotaa@1.1.6")
    depends_on("py-jsonschema@4.18")
    depends_on("py-lxml@5.2")
    depends_on("py-pyyaml@6.0")
    depends_on("py-requests@2.32")

    license("GPL-2.0-or-later", checked_by="WeirAE")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            python(
                # Using the spack default python package install options
                "-m",
                "pip",
                f"--prefix={prefix}",
                f"uwtools/{self.version)/download/noarch/uwtools-{self.version)-py_0.tar.bz2",
                "install",
                "--no-deps",
            )