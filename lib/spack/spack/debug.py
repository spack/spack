# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A module to help debug Spack (including package.py methods)"""
from contextlib import contextmanager

import llnl.util.tty.log

_pdb = False


class nooplog:
    def __init__(self):
        # This passes all output, so the effect is the same as to echo
        self.echo = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @contextmanager
    def force_echo(self):
        yield


def log_output(*args, **kwargs):
    global _pdb
    if _pdb:
        return nooplog()
    else:
        return llnl.util.tty.log.log_output(*args, **kwargs)
