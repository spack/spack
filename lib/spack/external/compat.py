# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import multiprocessing
import sys

from ordereddict_backport import OrderedDict

if sys.version_info < (3, 0):
    from itertools import ifilter as filter
    from itertools import imap as map
    from itertools import izip as zip
    from itertools import izip_longest as zip_longest
    from urllib import urlopen as urlopen, urlencode as urlencode
else:
    filter = filter
    map = map
    zip = zip
    from itertools import zip_longest as zip_longest   # novm
    from urllib.request import urlopen as urlopen      # novm
    from urllib.parse import urlencode as urlencode    # novm

if sys.version_info >= (3, 3):
    from collections.abc import Hashable as Hashable                # novm
    from collections.abc import Iterable as Iterable                # novm
    from collections.abc import Mapping as Mapping                  # novm
    from collections.abc import MutableMapping as MutableMapping    # novm
    from collections.abc import MutableSet as MutableSet            # novm
    from collections.abc import MutableSequence as MutableSequence  # novm
    from collections.abc import Sequence as Sequence                # novm
else:
    from collections import Hashable as Hashable
    from collections import Iterable as Iterable
    from collections import Mapping as Mapping
    from collections import MutableMapping as MutableMapping
    from collections import MutableSequence as MutableSequence
    from collections import MutableSet as MutableSet
    from collections import Sequence as Sequence

# On macOS, Python 3.8 multiprocessing now defaults to the 'spawn' start
# method. Spack cannot currently handle this, so force the process to start
# using the 'fork' start method.
#
# TODO: This solution is not ideal, as the 'fork' start method can lead to
# crashes of the subprocess. Figure out how to make 'spawn' work.
#
# See:
# * https://github.com/spack/spack/pull/18124
# * https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods  # noqa: E501
# * https://bugs.python.org/issue33725
if sys.version_info >= (3,):
    fork_context = multiprocessing.get_context('fork')
else:
    fork_context = multiprocessing
