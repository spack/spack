# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack.package import *


class PerlXmlSax(PerlPackage):
    """XML::SAX is a SAX parser access API for Perl. It includes classes and
    APIs required for implementing SAX drivers, along with a factory class for
    returning any SAX parser installed on the user's system."""

    homepage = "https://metacpan.org/pod/XML::SAX"
    url = "https://cpan.metacpan.org/authors/id/G/GR/GRANTM/XML-SAX-1.02.tar.gz"

    version("1.02", sha256="4506c387043aa6a77b455f00f57409f3720aa7e553495ab2535263b4ed1ea12a")

    depends_on("perl-xml-namespacesupport", type=("build", "run"))
    depends_on("perl-xml-sax-base", type=("build", "run"))


class PerlBuilder(spack.build_systems.perl.PerlBuilder):
    class _WrappedExecutable(Executable):
        def __init__(self, executable):
            super(PerlBuilder._WrappedExecutable, self).__init__(executable.path)

        def __call__(self, *args, **kwargs):
            # Do you want to run external tests?
            config_answers = ["\n"]
            config_answers_filename = "spack-config.in"

            with open(config_answers_filename, "w") as f:
                f.writelines(config_answers)

            with open(config_answers_filename, "r") as f:
                super(PerlBuilder._WrappedExecutable, self).__call__(*args, **kwargs, input=f)

    def configure(self, pkg, spec, prefix):
        perl_safe = inspect.getmodule(self).perl
        inspect.getmodule(self).perl = PerlBuilder._WrappedExecutable(perl_safe)

        try:
            super(PerlBuilder, self).configure(pkg, spec, prefix)
        finally:
            inspect.getmodule(self).perl = perl_safe
