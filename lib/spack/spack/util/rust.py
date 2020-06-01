# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from six import iteritems

from spack.spec import Spec

"""Routines for working with the Rust toolchain"""

# This dictionary maps Rust target architectures to Spack constraints that
# match that target.
rust_archs = {
    'x86_64-unknown-linux-gnu': [
        {'platform': 'linux', 'target': 'x86_64:'},
        {'platform': 'cray', 'target': 'x86_64:'}
    ],
    'powerpc64le-unknown-linux-gnu': [
        {'platform': 'linux', 'target': 'ppc64le:'},
        {'platform': 'cray', 'target': 'ppc64le:'}
    ],
    'aarch64-unknown-linux-gnu': [
        {'platform': 'linux', 'target': 'aarch64:'},
        {'platform': 'cray', 'target': 'aarch64:'}
    ],
    'x86_64-apple-darwin': [
        {'platform': 'darwin', 'target': 'x86_64:'}
    ]
}
