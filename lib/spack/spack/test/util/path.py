# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import llnl.util.tty as tty

import spack.config
import spack.util.path as sup

#: Some lines with lots of placeholders
padded_lines = [
    "==> [2021-06-23-15:59:05.020387] './configure' '--prefix=/Users/gamblin2/padding-log-test/opt/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_pla/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga",  # noqa: E501
    "/Users/gamblin2/Workspace/spack/lib/spack/env/clang/clang -dynamiclib -install_name /Users/gamblin2/padding-log-test/opt/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_pla/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga/lib/libz.1.dylib -compatibility_version 1 -current_version 1.2.11 -fPIC -O2 -fPIC -DHAVE_HIDDEN -o libz.1.2.11.dylib adler32.lo crc32.lo deflate.lo infback.lo inffast.lo inflate.lo inftrees.lo trees.lo zutil.lo compress.lo uncompr.lo gzclose.lo gzlib.lo gzread.lo gzwrite.lo  -lc",  # noqa: E501
    "rm -f /Users/gamblin2/padding-log-test/opt/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_pla/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga/lib/libz.a",  # noqa: E501
]


#: unpadded versions of padded_lines, with [padded-to-X-chars] replacing the padding
fixed_lines = [
    "==> [2021-06-23-15:59:05.020387] './configure' '--prefix=/Users/gamblin2/padding-log-test/opt/[padded-to-512-chars]/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga",  # noqa: E501
    "/Users/gamblin2/Workspace/spack/lib/spack/env/clang/clang -dynamiclib -install_name /Users/gamblin2/padding-log-test/opt/[padded-to-512-chars]/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga/lib/libz.1.dylib -compatibility_version 1 -current_version 1.2.11 -fPIC -O2 -fPIC -DHAVE_HIDDEN -o libz.1.2.11.dylib adler32.lo crc32.lo deflate.lo infback.lo inffast.lo inflate.lo inftrees.lo trees.lo zutil.lo compress.lo uncompr.lo gzclose.lo gzlib.lo gzread.lo gzwrite.lo  -lc",  # noqa: E501
    "rm -f /Users/gamblin2/padding-log-test/opt/[padded-to-512-chars]/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga/lib/libz.a",  # noqa: E501
]


@pytest.mark.parametrize("padded,fixed", zip(padded_lines, fixed_lines))
def test_padding_substitution(padded, fixed):
    """Ensure that all padded lines are unpadded correctly."""
    assert fixed == sup.padding_filter(padded)


def test_no_substitution():
    """Ensure that a line not containing one full path placeholder is not modified."""
    partial = "--prefix=/Users/gamblin2/padding-log-test/opt/__spack_path_pla/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga'"  # noqa: E501
    assert sup.padding_filter(partial) == partial


def test_short_substitution():
    """Ensure that a single placeholder path component is replaced"""
    short = "--prefix=/Users/gamblin2/padding-log-test/opt/__spack_path_placeholder__/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga'"  # noqa: E501
    short_subst = "--prefix=/Users/gamblin2/padding-log-test/opt/[padded-to-63-chars]/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga'"  # noqa: E501
    assert short_subst == sup.padding_filter(short)


def test_partial_substitution():
    """Ensure that a single placeholder path component is replaced"""
    short = "--prefix=/Users/gamblin2/padding-log-test/opt/__spack_path_placeholder__/__spack_p/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga'"  # noqa: E501
    short_subst = "--prefix=/Users/gamblin2/padding-log-test/opt/[padded-to-73-chars]/darwin-bigsur-skylake/apple-clang-12.0.5/zlib-1.2.11-74mwnxgn6nujehpyyalhwizwojwn5zga'"  # noqa: E501
    assert short_subst == sup.padding_filter(short)


def test_longest_prefix_re():
    """Test that longest_prefix_re generates correct regular expressions."""
    assert "(s(?:t(?:r(?:i(?:ng?)?)?)?)?)" == sup.longest_prefix_re(
        "string", capture=True
    )
    assert "(?:s(?:t(?:r(?:i(?:ng?)?)?)?)?)" == sup.longest_prefix_re(
        "string", capture=False
    )


def test_output_filtering(capfd, install_mockery, mutable_config):
    """Test filtering padding out of tty messages."""
    long_path = "/" + "/".join([sup.SPACK_PATH_PADDING_CHARS] * 200)
    padding_string = "[padded-to-%d-chars]" % len(long_path)

    # test filtering when padding is enabled
    with spack.config.override('config:install_tree', {"padded_length": 256}):
        # tty.msg with filtering on the first argument
        with sup.filter_padding():
            tty.msg("here is a long path: %s/with/a/suffix" % long_path)
        out, err = capfd.readouterr()
        assert padding_string in out

        # tty.msg with filtering on a laterargument
        with sup.filter_padding():
            tty.msg("here is a long path:", "%s/with/a/suffix" % long_path)
        out, err = capfd.readouterr()
        assert padding_string in out

        # tty.error with filtering on the first argument
        with sup.filter_padding():
            tty.error("here is a long path: %s/with/a/suffix" % long_path)
        out, err = capfd.readouterr()
        assert padding_string in err

        # tty.error with filtering on a later argument
        with sup.filter_padding():
            tty.error("here is a long path:", "%s/with/a/suffix" % long_path)
        out, err = capfd.readouterr()
        assert padding_string in err

    # test no filtering
    tty.msg("here is a long path: %s/with/a/suffix" % long_path)
    out, err = capfd.readouterr()
    assert padding_string not in out
