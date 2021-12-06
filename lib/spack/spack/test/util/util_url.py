# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's URL handling utility functions."""
import os
import os.path

import pytest

import spack.paths
import spack.util.url as url_util


def test_url_parse():
    parsed = url_util.parse('/path/to/resource')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    assert(parsed.path == '/path/to/resource')

    parsed = url_util.parse('/path/to/resource', scheme='fake')
    assert(parsed.scheme == 'fake')
    assert(parsed.netloc == '')
    assert(parsed.path == '/path/to/resource')

    parsed = url_util.parse('file:///path/to/resource')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    assert(parsed.path == '/path/to/resource')

    parsed = url_util.parse('file:///path/to/resource', scheme='fake')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    assert(parsed.path == '/path/to/resource')

    parsed = url_util.parse('file://path/to/resource')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    expected = os.path.abspath(os.path.join('path', 'to', 'resource'))
    assert(parsed.path == expected)

    parsed = url_util.parse('https://path/to/resource')
    assert(parsed.scheme == 'https')
    assert(parsed.netloc == 'path')
    assert(parsed.path == '/to/resource')

    spack_root = spack.paths.spack_root
    parsed = url_util.parse('$spack')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    assert(parsed.path == spack_root)

    parsed = url_util.parse('/a/b/c/$spack')
    assert(parsed.scheme == 'file')
    assert(parsed.netloc == '')
    expected = os.path.abspath(os.path.join(
        '/', 'a', 'b', 'c', './' + spack_root))
    assert(parsed.path == expected)


def test_url_local_file_path():
    spack_root = spack.paths.spack_root

    lfp = url_util.local_file_path('/a/b/c.txt')
    assert(lfp == '/a/b/c.txt')

    lfp = url_util.local_file_path('file:///a/b/c.txt')
    assert(lfp == '/a/b/c.txt')

    lfp = url_util.local_file_path('file://a/b/c.txt')
    expected = os.path.abspath(os.path.join('a', 'b', 'c.txt'))
    assert(lfp == expected)

    lfp = url_util.local_file_path('$spack/a/b/c.txt')
    expected = os.path.abspath(os.path.join(spack_root, 'a', 'b', 'c.txt'))
    assert(lfp == expected)

    lfp = url_util.local_file_path('file:///$spack/a/b/c.txt')
    expected = os.path.abspath(os.path.join(spack_root, 'a', 'b', 'c.txt'))
    assert(lfp == expected)

    lfp = url_util.local_file_path('file://$spack/a/b/c.txt')
    expected = os.path.abspath(os.path.join(spack_root, 'a', 'b', 'c.txt'))
    assert(lfp == expected)

    # not a file:// URL - so no local file path
    lfp = url_util.local_file_path('http:///a/b/c.txt')
    assert(lfp is None)

    lfp = url_util.local_file_path('http://a/b/c.txt')
    assert(lfp is None)

    lfp = url_util.local_file_path('http:///$spack/a/b/c.txt')
    assert(lfp is None)

    lfp = url_util.local_file_path('http://$spack/a/b/c.txt')
    assert(lfp is None)


def test_url_join_local_paths():
    # Resolve local link against page URL

    # wrong:
    assert(
        url_util.join(
            's3://bucket/index.html',
            '../other-bucket/document.txt')
        ==
        's3://bucket/other-bucket/document.txt')

    # correct - need to specify resolve_href=True:
    assert(
        url_util.join(
            's3://bucket/index.html',
            '../other-bucket/document.txt',
            resolve_href=True)
        ==
        's3://other-bucket/document.txt')

    # same as above: make sure several components are joined together correctly
    assert(
        url_util.join(
            # with resolve_href=True, first arg is the base url; can not be
            # broken up
            's3://bucket/index.html',

            # with resolve_href=True, remaining arguments are the components of
            # the local href that needs to be resolved
            '..', 'other-bucket', 'document.txt',
            resolve_href=True)
        ==
        's3://other-bucket/document.txt')

    # Append local path components to prefix URL

    # wrong:
    assert(
        url_util.join(
            'https://mirror.spack.io/build_cache',
            'my-package',
            resolve_href=True)
        ==
        'https://mirror.spack.io/my-package')

    # correct - Need to specify resolve_href=False:
    assert(
        url_util.join(
            'https://mirror.spack.io/build_cache',
            'my-package',
            resolve_href=False)
        ==
        'https://mirror.spack.io/build_cache/my-package')

    # same as above; make sure resolve_href=False is default
    assert(
        url_util.join(
            'https://mirror.spack.io/build_cache',
            'my-package')
        ==
        'https://mirror.spack.io/build_cache/my-package')

    # same as above: make sure several components are joined together correctly
    assert(
        url_util.join(
            # with resolve_href=False, first arg is just a prefix. No
            # resolution is done.  So, there should be no difference between
            # join('/a/b/c', 'd/e'),
            # join('/a/b', 'c', 'd/e'),
            # join('/a', 'b/c', 'd', 'e'), etc.
            'https://mirror.spack.io',
            'build_cache',
            'my-package')
        ==
        'https://mirror.spack.io/build_cache/my-package')

    # file:// URL path components are *NOT* canonicalized
    spack_root = spack.paths.spack_root

    join_result = url_util.join('/a/b/c', '$spack')
    assert(join_result == 'file:///a/b/c/$spack')  # not canonicalized
    format_result = url_util.format(join_result)
    # canoncalize by hand
    expected = url_util.format(os.path.abspath(os.path.join(
        '/', 'a', 'b', 'c', '.' + spack_root)))
    assert(format_result == expected)

    # see test_url_join_absolute_paths() for more on absolute path components
    join_result = url_util.join('/a/b/c', '/$spack')
    assert(join_result == 'file:///$spack')  # not canonicalized
    format_result = url_util.format(join_result)
    expected = url_util.format(spack_root)
    assert(format_result == expected)

    # For s3:// URLs, the "netloc" (bucket) is considered part of the path.
    # Make sure join() can cross bucket boundaries in this case.
    args = ['s3://bucket/a/b', 'new-bucket', 'c']
    assert(url_util.join(*args) == 's3://bucket/a/b/new-bucket/c')

    args.insert(1, '..')
    assert(url_util.join(*args) == 's3://bucket/a/new-bucket/c')

    args.insert(1, '..')
    assert(url_util.join(*args) == 's3://bucket/new-bucket/c')

    # new-bucket is now the "netloc" (bucket name)
    args.insert(1, '..')
    assert(url_util.join(*args) == 's3://new-bucket/c')


def test_url_join_absolute_paths():
    # Handling absolute path components is a little tricky.  To this end, we
    # distinguish "absolute path components", from the more-familiar concept of
    # "absolute paths" as they are understood for local filesystem paths.
    #
    # - All absolute paths are absolute path components.  Joining a URL with
    #   these components has the effect of completely replacing the path of the
    #   URL with the absolute path.  These components do not specify a URL
    #   scheme, so the scheme of the URL procuced when joining them depend on
    #   those provided by components that came before it (file:// assumed if no
    #   such scheme is provided).

    # For eaxmple:
    p = '/path/to/resource'
    # ...is an absolute path

    # http:// URL
    assert(
        url_util.join('http://example.com/a/b/c', p)
        == 'http://example.com/path/to/resource')

    # s3:// URL
    # also notice how the netloc is treated as part of the path for s3:// URLs
    assert(
        url_util.join('s3://example.com/a/b/c', p)
        == 's3://path/to/resource')

    # - URL components that specify a scheme are always absolute path
    #   components.  Joining a base URL with these components effectively
    #   discards the base URL and "resets" the joining logic starting at the
    #   component in question and using it as the new base URL.

    # For eaxmple:
    p = 'http://example.com/path/to'
    # ...is an http:// URL

    join_result = url_util.join(p, 'resource')
    assert(join_result == 'http://example.com/path/to/resource')

    # works as if everything before the http:// URL was left out
    assert(
        url_util.join(
            'literally', 'does', 'not', 'matter',
            p, 'resource')
        == join_result)

    # It's important to keep in mind that this logic applies even if the
    # component's path is not an absolute path!

    # For eaxmple:
    p = './d'
    # ...is *NOT* an absolute path
    # ...is also *NOT* an absolute path component

    u = 'file://./d'
    # ...is a URL
    #     The path of this URL is *NOT* an absolute path
    #     HOWEVER, the URL, itself, *is* an absolute path component

    # (We just need...
    cwd = os.getcwd()
    # ...to work out what resource it points to)

    # So, even though parse() assumes "file://" URL, the scheme is still
    # significant in URL path components passed to join(), even if the base
    # is a file:// URL.

    path_join_result = 'file:///a/b/c/d'
    assert(url_util.join('/a/b/c', p) == path_join_result)
    assert(url_util.join('file:///a/b/c', p) == path_join_result)

    url_join_result = 'file://{CWD}/d'.format(CWD=cwd)
    assert(url_util.join('/a/b/c', u) == url_join_result)
    assert(url_util.join('file:///a/b/c', u) == url_join_result)

    # Finally, resolve_href should have no effect for how absolute path
    # components are handled because local hrefs can not be absolute path
    # components.
    args = ['s3://does', 'not', 'matter',
            'http://example.com',
            'also', 'does', 'not', 'matter',
            '/path']

    expected = 'http://example.com/path'
    assert(url_util.join(*args, resolve_href=True) == expected)
    assert(url_util.join(*args, resolve_href=False) == expected)

    # resolve_href only matters for the local path components at the end of the
    # argument list.
    args[-1] = '/path/to/page'
    args.extend(('..', '..', 'resource'))

    assert(url_util.join(*args, resolve_href=True) ==
           'http://example.com/resource')

    assert(url_util.join(*args, resolve_href=False) ==
           'http://example.com/path/resource')


@pytest.mark.parametrize("url,parts", [
    ("ssh://user@host.xz:500/path/to/repo.git/",
     ("ssh", "user", "host.xz", 500, "/path/to/repo.git")),
    ("ssh://user@host.xz/path/to/repo.git/",
     ("ssh", "user", "host.xz", None, "/path/to/repo.git")),
    ("ssh://host.xz:500/path/to/repo.git/",
     ("ssh", None, "host.xz", 500, "/path/to/repo.git")),
    ("ssh://host.xz/path/to/repo.git/",
     ("ssh", None, "host.xz", None, "/path/to/repo.git")),
    ("ssh://user@host.xz/path/to/repo.git/",
     ("ssh", "user", "host.xz", None, "/path/to/repo.git")),
    ("ssh://host.xz/path/to/repo.git/",
     ("ssh", None, "host.xz", None, "/path/to/repo.git")),
    ("ssh://user@host.xz/~user/path/to/repo.git/",
     ("ssh", "user", "host.xz", None, "~user/path/to/repo.git")),
    ("ssh://host.xz/~user/path/to/repo.git/",
     ("ssh", None, "host.xz", None, "~user/path/to/repo.git")),
    ("ssh://user@host.xz/~/path/to/repo.git",
     ("ssh", "user", "host.xz", None, "~/path/to/repo.git")),
    ("ssh://host.xz/~/path/to/repo.git",
     ("ssh", None, "host.xz", None, "~/path/to/repo.git")),
    ("git@github.com:spack/spack.git",
     (None, "git", "github.com", None, "spack/spack.git")),
    ("user@host.xz:/path/to/repo.git/",
     (None, "user", "host.xz", None, "/path/to/repo.git")),
    ("host.xz:/path/to/repo.git/",
     (None, None, "host.xz", None, "/path/to/repo.git")),
    ("user@host.xz:~user/path/to/repo.git/",
     (None, "user", "host.xz", None, "~user/path/to/repo.git")),
    ("host.xz:~user/path/to/repo.git/",
     (None, None, "host.xz", None, "~user/path/to/repo.git")),
    ("user@host.xz:path/to/repo.git",
     (None, "user", "host.xz", None, "path/to/repo.git")),
    ("host.xz:path/to/repo.git",
     (None, None, "host.xz", None, "path/to/repo.git")),
    ("rsync://host.xz/path/to/repo.git/",
     ("rsync", None, "host.xz", None, "/path/to/repo.git")),
    ("git://host.xz/path/to/repo.git/",
     ("git", None, "host.xz", None, "/path/to/repo.git")),
    ("git://host.xz/~user/path/to/repo.git/",
     ("git", None, "host.xz", None, "~user/path/to/repo.git")),
    ("http://host.xz/path/to/repo.git/",
     ("http", None, "host.xz", None, "/path/to/repo.git")),
    ("https://host.xz/path/to/repo.git/",
     ("https", None, "host.xz", None, "/path/to/repo.git")),
    ("https://github.com/spack/spack",
     ("https", None, "github.com", None, "/spack/spack")),
    ("https://github.com/spack/spack/",
     ("https", None, "github.com", None, "/spack/spack")),
    ("file:///path/to/repo.git/",
     ("file", None, None, None, "/path/to/repo.git")),
    ("file://~/path/to/repo.git/",
     ("file", None, None, None, "~/path/to/repo.git")),
    # bad ports should give us None
    ("ssh://host.xz:port/path/to/repo.git/", None),
    # bad ports should give us None
    ("ssh://host-foo.xz:port/path/to/repo.git/", None),
    # regular file paths should give us None
    ("/path/to/repo.git/", None),
    ("path/to/repo.git/", None),
    ("~/path/to/repo.git", None),
])
def test_git_url_parse(url, parts):
    if parts is None:
        with pytest.raises(ValueError):
            url_util.parse_git_url(url)
    else:
        assert parts == url_util.parse_git_url(url)
