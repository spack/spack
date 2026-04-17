# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Ruff(Package):
    """Package containing ``PEP8`` violations.

    Ruff check + format handle most errors robustly and those that
    cannot be handled directly are infrequent enough we can noqa them

    This file contains a number of errors ruff should be able to reformat
    and pass style over

    """

    # Used to tell whether or not the package has been modified
    state = "unmodified"

    # Make sure pre-existing noqa is not interfered with
    # note that black can sometimes fix shorter assignment statements by sticking them in
    # parens and adding line breaks, e.g.:
    #
    # foo = (
    #     "too-long-string"
    # )
    #
    # but the one below can't even be fixed that way -- you have to add noqa, or break
    # it up inside parens yourself.
    blatant_violation = "line-that-has-absolutely-no-execuse-for-being-over-99-characters-and-that-black-cannot-fix-with-parens"  # noqa: E501

    # All URL strings are exempt from line-length checks.
    #
    # ruff will not complain about these
    hg = "https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-not-ignore-by-default"
    list_url = "https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-not-ignore-by-default"
    git = "ssh://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-not-ignore-by-default"

    # directives with URLs are exempt as well
    version(
        "1.0",
        url="https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-not-ignore-by-default",
    )

    #
    # Also test URL comments (though ruff will ignore these by default anyway)
    #
    # http://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-ignore-by-default
    # https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-ignore-by-default
    # ftp://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-ignore-by-default
    # ssh://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-ignore-by-default
    # file://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-ruff-will-ignore-by-default

    def install(self, spec, prefix):
        # Make sure lines with '# noqa' work as expected. Don't just
        # remove them entirely. This will mess up the indentation of
        # the following lines.
        if (
            "really-long-if-statement"
            != "this-string-is-so-long-that-it-is-over-the-line-limit-and-black-will-not-split-it-so-it-requires-noqa"  # noqa: E501
        ):
            pass

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    # '@when' decorated functions are exempt from redefinition errors
    @when("@2.0")
    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)
