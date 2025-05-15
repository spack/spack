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

class Uwtools(PythonPackage):
    """UW Tools is a modern, open-source Python package that helps
    automate common tasks needed for many standard numerical weather
    prediction (NWP) workflows. It also provides drivers to automate
    the configuration and execution of Unified Forecast System (UFS)
    components, providing flexibility, interoperability, and
    usability to various UFS Applications."""

    homepage = "https://uwtools.readthedocs.io/en/stable/"
    url = "https://anaconda.org/ufs-community/uwtools/2.5.1/download/noarch/uwtools-2.5.1-py_0.tar.bz2"
    list_url = "https://anaconda.org/ufs-community/uwtools/"
    list_depth = 3

    maintainers(
            "NaureenBharwaniNOAA",
            "christinaholtNOAA",
            "elcarpenterNOAA",
            "maddenp-noaa"
    )

    version(
            "2.5.1",
            sha256="fad902bbf543a93408fa277cd59b1c0f",
    )

    depends_on("py-pip", type="build")
    depends_on("python@3.9:3.13")
    depends_on("py-setuptools", type="build")
    depends_on("py-f90nml@1.4")
    depends_on("py-jinja2@3.1")
    depends_on("py-jsonschema@4.18:4.24")
    depends_on("py-lxml@5.2")
    depends_on("py-pyyaml@6.0")
    depends_on("iotaa@0.8:", when="@:2.6")
    depends_on("iotaa@1.1:", when="@2.6:")
    depends_on("py-requests@2.32", when="@2.6:")

    license("GPL-2.0-or-later", checked_by="WeirAE")


    @property
    def ext_name(self):
        ext = "tar.bz2"
        if self.version >= Version("2.6.0"):
            ext = "conda"
        return ext

    def url_for_version(self, version):
        url = "https://anaconda.org/ufs-community/uwtools/{0}/download/noarch/uwtools-{0}-py_0.{1}"
        return url.format(version, self.ext_name)

    def install(self, spec, prefix):
       with working_dir(self.build_directory):
           python(
               # Using the spack default python package install options
               "-m",
               "pip",
               "install",
               "--no-deps",
               f"--prefix={prefix}",
               f"uwtools-{self.version}-py_0.{self.ext_name}",
           )
